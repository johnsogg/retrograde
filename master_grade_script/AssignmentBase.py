import os, re, subprocess, sys

class AssignmentBase(object):
    def __init__(self):
        self.verbose = []
        self.assignment = "Unknown Assignment"
        self.lang = "Unknown Language"
        self.build_command = "echo replace this with your build command string"
        self.unit_test_command = "echo replace this with your unit test command"
        self.instructor_files = []
        self.student_files = []
        self.points = {}

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
            # make linked_list -- need to think about how to extract this
            ok = self.run([self.build_command], sys.stdout, sys.stderr)

        if (ok):
            # run linked_list_test
            outfileW = open(outfile_name, "w")
            self.run([self.unit_test_command], outfileW, sys.stderr)
            outfileW.close()
            outfile = open(outfile_name, "r")
            result, errors = self.parse_for_grade(outfile)
            self.check_for_omitted_tests(result)

        if len(result) > 0:
            # print_results(result)
            pass
        else:
            ok = False
        joined = os.path.join('.', outfile_name)
        final_path = os.path.abspath(joined)
        self.verbose_log(errors)
        self.verbose_log("Output is in the file: " + final_path)
        return (ok, result, errors, final_path)

    def parse_for_grade(self, outfile):
        self.verbose_log("Parsing outfile...")
        result = {}
        errors = []
        for line in outfile:
            self.get_test_result(line, result, errors)
        return result, ''.join(errors)

    def check_for_omitted_tests(self, result):
        self.verbose_log("check for ommitted tests in the following list:")
        targetSet = set(self.points.keys())
        inputSet = set(result.keys())
        if (targetSet != inputSet):
            self.verbose_log("\n  ******************************************************************")
            self.verbose_log("  * WARNING: Tests performed were not the same as those prescribed.")
            notTested = targetSet.difference(inputSet)
            for thing in notTested:
                self.verbose_log("  *\tmissing: " + thing)
            self.verbose_log("  ******************************************************************\n")

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

    def run(self, args, out, err):
        self.verbose_log("\nRunning " + " ".join(args) + "...\n")
        self.flushall()
        ret = 0 is subprocess.call(args, shell=True, stdout=out, stderr=sys.stderr)
        self.verbose_log("\n ... return value: " + str(ret) + "\n")
        self.flushall()
        return ret


class ExampleAssignment(AssignmentBase):
    def __init__(self):
        super(ExampleAssignment, self).__init__()
        self.assignment = "Example Assignment"
        self.lang = "cpp"
        self.instructor_files = [
            "Makefile",
            "RetroPrinter.cpp",
            "RetroPrinter.h",
            "linked_list.h",
            "linked_list_test.cpp"
            ]
        self.student_files = [
            "linked_list.cpp"
            ]
        self.points = {
            "Report": 1,
            "InitNode" : 1,
            "InsertEmpty" : 1,
            "InsertStart" : 1,
            "InsertEnd" : 1,
            "InsertRedundant" : 1,
            "Remove" : 4,
            }
