import os, re, subprocess, sys, json, signal
from django.conf import settings


# this is used to detect long-running scripts
class TakingTooLong(Exception):
    pass

# alarm handler hooked up to signal.SIGALRM to raise
# TakingTooLong when a script takes its sweet time.
# this is infinite-loop avoidance.
def alarm_handler(signum, frame):
    raise TakingTooLong


class Assignment(object):

    FLAMING_ERROR_COMPILE = "Compilation Error"
    FLAMING_ERROR_RUNTIME = "Runtime error or Infinite Loop"

    def __init__(self, descriptor_files):
        self.verbose = []
        dat = self.check_descriptions(descriptor_files)
        self.assignment = dat["assignment"]
        self.lang = dat["lang"]
        self.build_command = dat["build_command"]
        self.unit_test_command = dat["unit_test_command"]
        self.instructor_files = dat["instructor_files"]
        self.student_files = dat["student_files"]
        self.points = dat["points"]
        self.flaming_error = None

    def check_descriptions(self, file_paths):
        main_dict = {}
        print "File paths: " + str(file_paths)
        for f in file_paths:
            self.verbose_log("Description File: " + f)
            try:
                decoded = json.loads(open(f, 'r').read())
                for k in decoded.keys():
                    if k in main_dict:
                        self.verbose_log("Warning: key '%s' duplicated!" % k)
                    main_dict[k] = decoded[k]
            except Exception as e:
                self.verbose_log("Got exception when unpacking JSON descriptor. Stray comma? Missing comma? Gotta watch out for those commas.")
                self.verbose_log("Bad descriptor file: " + str(f))
        return main_dict

    def verbose_log(self, words):
        self.verbose.append(words)

    def get_verbose_log(self):
        return "\n".join(self.verbose)

    def get_total_points(self):
        return sum(self.points.values())

    def grade(self):
        self.verbose_log("Assignment: " + self.assignment)
        self.verbose_log("Language: " + self.lang)
        self.verbose_log("Points Possible: " + str(self.get_total_points()))
        ok = True;
        # 'result' is a dictionary that maps question keys (like 'InsertData')
        # to a tuple. The tuple is (actual_score, maximum_score).
        result = {}
        errors = ""
        outfile_name = "unit_test_output.txt"

        if (ok):
            for f in self.instructor_files:
                if not os.path.exists(f):
                    self.verbose_log("Error: Instructor File '" + f + "' not found!")
                    ok = False
        if (ok):
            self.verbose_log("Instructor file(s) in place.")
        if (ok):
            for f in self.student_files:
                if not os.path.exists(f):
                    self.verbose_log("Error: Student File '" + f + "' not found!")
                    ok = False
        if (ok):
            self.verbose_log("Student file(s) in place.")

        if (ok and self.build_command is not None):
            # run the build command
            print "Running build command:"
            print self.build_command
            return_code = self.run_redirect_output([self.build_command], 
                                                   "build-output", "Build command")
            ok = return_code is 0
        if (not ok):
            self.verbose_log("Build command failed.")
            self.flaming_error = Assignment.FLAMING_ERROR_COMPILE
        else:
            self.verbose_log("Compiled OK")

        if (ok and self.lang != 'txt'):
            # run the unit test
            try:
                outfileW = open(outfile_name, "w")
                errfileW = open("error-text", "w")
                unit_test_result = self.run([self.unit_test_command], 
                                            outfileW, errfileW, "Unit Test command")
                if unit_test_result is not 0:
                    self.verbose_log("Got runtime error or detected infinite loop.")
                    self.flaming_error = Assignment.FLAMING_ERROR_RUNTIME;
                else:
                    self.verbose_log("Unit test completed normally.")
                outfileW.close()
                errfileW.close()
                outfile = open(outfile_name, "r")
                errfile = open("error-text", "r")
                self.verbose_log(errfile.read())
                errfile.close()
                result, errors = self.parse_for_grade(outfile)
                self.check_for_omitted_tests(result)
                self.verbose_log("Completed unit test command.")
                self.verbose_log("result: " + str(result))
                self.verbose_log("errors: " + str(errors))
                self.verbose_log("Done reporting result and errors.")
            except Exception as e:
                self.verbose_log("Got Exception during unit test run: " + str(e))
        if (ok and self.lang == 'txt'):
            result, errors = self.full_credit()

        if len(result) > 0:
            # print_results(result)
            pass
        else:
            ok = False
        joined = os.path.join('.', outfile_name)
        final_path = os.path.abspath(joined)
        # self.verbose_log(errors)
        self.verbose_log("Output is in the file: " + final_path)
        return (ok, result, errors, final_path, self.flaming_error)

    def full_credit(self):
        result = {}
        errors = []
        for k in self.points.keys():
            result[k] = (self.points[k], self.points[k])
        return result, ''.join(errors)

    def parse_for_grade(self, outfile):
        self.verbose_log("Parsing outfile...")
        result = {}
        errors = []
        for line in outfile:
            self.get_test_result(line, result, errors)
        return result, ''.join(errors)

    def check_for_omitted_tests(self, result):
        self.verbose_log("Checking for ommitted tests")
        targetSet = set(self.points.keys())
        inputSet = set(result.keys())
        ok = True
        if (targetSet != inputSet):
            ok = False
            self.verbose_log("\n  ******************************************************************")
            self.verbose_log("  * WARNING: Tests performed were not the same as those prescribed.")
            notTested = targetSet.difference(inputSet)
            for thing in notTested:
                self.verbose_log("  *\tmissing: " + thing)
            self.verbose_log("  ******************************************************************\n")
        if (ok):
            self.verbose_log("No tests omitted.")

    def get_test_result(self, line, result, errors):
        pattern = "RetroGrade Result >\s*(\w.*):\s(.)"
        ignore_pattern = "^RetroGrade"
        m = re.match(pattern, line)
        if (m):
            question_key = m.group(1)
            question_result = m.group(2)
            # print question_key + " " + question_result
            score = 0
            if question_result is '+':
                if question_key in self.points:
                    score = self.points[question_key]
                else:
                    self.verbose_log("ERROR: No points assigned for question '" + question_key + "'")
                    self.verbose_log("       Please contact the instructor about this problem. Other")
                    self.verbose_log("       students will have this issue as well.")
                    self.verbose_log("")
                    self.verbose_log("       Here's the list of " + str(len(self.points)) + " known questions:")
                    self.verbose_log("\n       ".join(self.points.keys()))
            result[question_key] = (score, self.points[question_key])
        elif re.match(ignore_pattern, line):
            pass
        else:
            errors.append(line)

    def flushall(self):
        # is this necessary now that I'm not using separate processes?
        sys.stdout.flush()
        sys.stderr.flush()

    def run_redirect_output(self, args, out, desc):
        outfile = open(out, "w")
        ret = self.run(args, outfile, outfile, desc);
        outfile.close()
        outfileR = open(out, "r")
        self.verbose_log(outfileR.read())
        outfileR.close()
        return ret


    def run(self, args, out, err, desc):
        command = settings.RETROGRADE_RUN_SAFELY_PROG + " " + args[0]
        self.verbose_log("\n************ Running " + command + "...")
        self.flushall()
        # proc = subprocess.Popen(args, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        throwaway = subprocess.Popen(command, stderr=err, stdout=out, shell=True)
        rc = throwaway.wait()
        self.flushall()
        return rc

