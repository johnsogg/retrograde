import os, re, subprocess, sys

class AssignmentBase(object):
    def __init__(self):
        self.assignment = "Unknown Assignment"
        self.lang = "Unknown Language"
        self.build_command = "echo replace this with your build command string"
        self.unit_test_command = "echo replace this with your unit test command"
        self.instructor_files = []
        self.student_files = []
        self.points = {}

    def get_total_points(self):
        return sum(self.points.values())

    def grade(self):
        print "Assignment: " + self.assignment
        print "Language: " + self.lang
        print "Points Possible: " + str(self.get_total_points())
        ok = True;
        result = {}
        errors = ""
        outfile_name = "unit_test_output.txt"

        if (ok):
            for f in self.instructor_files:
                if not os.path.exists(f):
                    print "Error: Instructor File '" + f + "' not found!"
                    ok = False
        if (ok):
            print "Instructor file(s) in place."
        if (ok):
            for f in self.student_files:
                if not os.path.exists(f):
                    print "Error: Student File '" + f + "' not found!"
                    ok = False
        if (ok):
            print "Student file(s) in place."

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
            self.print_results(result)
        else:
            ok = False
        joined = os.path.join('.', outfile_name)
        final_path = os.path.abspath(joined)
        print errors
        print "Output is in the file: " + final_path
        return (ok, result, errors, final_path)

    def parse_for_grade(self, outfile):
        print "Parsing outfile..."
        result = {}
        errors = []
        for line in outfile:
            self.get_test_result(line, result, errors)
        return result, ''.join(errors)

    def check_for_omitted_tests(self, result):
        print "check for ommitted tests in the following list:"
        targetSet = set(self.points.keys())
        inputSet = set(result.keys())
        if (targetSet != inputSet):
            print "\n  ******************************************************************"
            print "  * WARNING: Tests performed were not the same as those prescribed."
            notTested = targetSet.difference(inputSet)
            for thing in notTested:
                print "  *\tmissing: " + thing
            print "  ******************************************************************\n"

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
                    print "ERROR: No points assigned for question '" + question_key + "'"
                    print "       Please contact the instructor about this problem. Other"
                    print "       students will have this issue as well."
                    print ""
                    print "       Here's the list of " + str(len(self.points)) + " known questions:"
                    print "\n       ".join(self.points.keys())
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
        print "\nRunning " + " ".join(args) + "...\n"
        self.flushall()
        ret = 0 is subprocess.call(args, shell=True, stdout=out, stderr=sys.stderr)
        print "\n ... return value: " + str(ret) + "\n"
        self.flushall()
        return ret

    def print_results(self, results):
        print "Printing results..."
        labelf = "{:>30} : "
        numf = "{:>3}"
        sep = "   / "
        total_score = 0
        total_possible_score = 0
        for k in results.keys():
            total_score = total_score + results[k][0]
            p = str(results[k][0])
            max_possible = str(results[k][1])
            total_possible_score = total_possible_score + results[k][1]
            print(labelf.format(k) + numf.format(p) + sep + numf.format(max_possible))
        print("\n" + labelf.format("TOTAL") + numf.format(total_score) + sep + numf.format(total_possible_score) + "\n")

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
