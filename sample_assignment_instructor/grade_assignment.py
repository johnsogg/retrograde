import os, re, subprocess, sys

ASSIGNMENT = "Linked Lists"
LANG = "cpp"

INSTRUCTOR_FILES = [ 
    "Makefile",
    "RetroPrinter.cpp",
    "RetroPrinter.h",
    "linked_list.h",
    "linked_list_test.cpp"
    ]

STUDENT_FILES = [
    "linked_list.cpp"
]

POINTS = {
    "Report": 1,
    "InitNode" : 1,
    "InsertEmpty" : 1,
    "InsertStart" : 1,
    "InsertEnd" : 1,
    "InsertRedundant" : 1,
    "Remove" : 4,
}

def get_total_points():
    return sum(POINTS.values())

def grade():
    print "Assignment: " + ASSIGNMENT
    print "Language: " + LANG
    print "Points Possible: " + str(get_total_points())
    ok = True;
    result = {}
    outfile_name = "unit_test_output.txt"

    if (ok):
        for f in INSTRUCTOR_FILES:
            if not os.path.exists(f):
                print "Error: Instructor File '" + f + "' not found!"
                ok = False
    if (ok):
        print "Instructor file(s) in place."
    if (ok):
        for f in STUDENT_FILES:
            if not os.path.exists(f):
                print "Error: Student File '" + f + "' not found!"
                ok = False
    if (ok):
        print "Student file(s) in place."

    if (ok):
        # make linked_list
        ok = run(["make"], sys.stdout, sys.stderr)
    
    if (ok):
        # run linked_list_test
        outfileW = open(outfile_name, "w")
        ok = run(["./linked_list_test"], outfileW, sys.stderr)
        outfileW.close()
        outfile = open(outfile_name, "r")
        result = parse_for_grade(outfile) # dictionary of question = score
        print "Got results dictionary: " + str(result)
    if len(result) > 0:
        print_results(result)

    return ok

def parse_for_grade(outfile):
    print "Parsing outfile..."
    result = {}
    for line in outfile:
        get_test_result(line, result)
    return result

def get_test_result(line, result):
    pattern = "RetroGrade Result >\s*(\w.*):\s(.)"
    m = re.match(pattern, line)
    if (m):
        question_key = m.group(1)
        question_result = m.group(2)
        # print question_key + " " + question_result
        score = 0
        if question_result is '+':
            if question_key in POINTS:
                score = POINTS[question_key]
            else:
                print "ERROR: No points assigned for question '" + question_key + "'"
                print "       Please contact the instructor about this problem. Other"
                print "       students will have this issue as well."
        result[question_key] = score
        # print "You get " + str(score) + " points for " + question_key

def flushall():
    sys.stdout.flush()
    sys.stderr.flush()

def run(args, out, err):
    print "\nRunning " + " ".join(args) + "...\n"
    flushall()
    ret = 0 is subprocess.call(args, shell=True, stdout=out, stderr=sys.stderr)
    print "\n ... return value: " + str(ret) + "\n"
    flushall()
    return ret

def print_results(results):
    print "Printing results..."
    labelf = "{:>30} : "
    numf = "{:>3}"
    sep = "   /   "
    total_score = 0
    for k in results.keys():
        total_score = total_score + results[k]
        p = str(results[k])
        max_possible = str(POINTS[k])
        print(labelf.format(k) + numf.format(p) + sep + numf.format(max_possible))
    print("\n" + labelf.format("TOTAL") + numf.format(total_score) + sep + numf.format(get_total_points()) + "\n")

print "grade_assignment loaded"
#if __name__ == '__main__':
#    print "grade_assignment executed as main. running grade()"
#    grade()

