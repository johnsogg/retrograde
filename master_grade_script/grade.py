#!/usr/bin/env python

import assignment # gives access to Assignment class
import argparse
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile
import traceback

class RetroGrade:
    LANG_UNKNOWN = "unknown"
    LANG_JAVA = "java"
    LANG_PYTHON = "py"
    LANG_CPP = "cpp"
    # the AVOID string is a regular expression used to avoid
    # by-product files like compiler output or emacs backups
    AVOID = "|".join([ ".class$",
                       ".o$",
                       ".a$",
                       ".pyc$",
                       "~$",
                       ])

    def __init__(self, instr_dir, assignment, student_id, files):
        try:
            self.verbose = []
            self.test_ok = False
            self.result_map = {}
            self.unit_test_errors = ""
            self.output_path = ""
            self.base_assignment_dir = instr_dir
            self.assignment = assignment
            self.student_id = student_id
            self.files = files
            self.language = RetroGrade.LANG_UNKNOWN
            self.report_input()
            ok = True
            if (ok):
                ok = self.determine_language()
            if (ok):
                ok = self.establish_dirs()
            if (ok):
                ok = self.copy_files()
            if (ok):
                ok_result_tuple = self.invoke_grade_script()
                self.test_ok = ok_result_tuple[0]
                self.result_map = ok_result_tuple[1]
                self.unit_test_errors = ok_result_tuple[2]
                self.output_path = ok_result_tuple[3]
        except:
            print "\n\nGot exception (see above). RetroGrade verbose log:"
            print self.get_verbose_log()

    def __str__(self):
        sb = []
        sb.append("Lang=" + str(self.language))
        sb.append("Test_OK=" + str(self.test_ok))
        sb.append("HW=" + str(self.assignment))
        return " ".join(sb)
            
    def report_input(self):
        self.verbose_log( "Created a RetroGrade instance.")
        self.verbose_log( "  Assignment:      " + self.assignment)
        self.verbose_log( "  Student:         " + self.student_id)
        self.verbose_log( "  Student Files:   " + ", ".join(self.files))

    def determine_language(self):
        ok = False;
        for file in self.files:
            self.verbose_log( "File: " + file)
            if (file.endswith(".java")):
                self.language = RetroGrade.LANG_JAVA
                break
            if (file.endswith(".cpp")):
                self.language = RetroGrade.LANG_CPP
                break
            if (file.endswith(".py")):
                self.language = RetroGrade.LANG_PYTHON
                break
        if (self.language is RetroGrade.LANG_UNKNOWN):
            self.verbose_log( "Could not determine language based on input files.")
            self.verbose_log( "Source files must end with '.java', '.py', or '.cpp'.")
            ok = False
        else:
            self.verbose_log( "Determined language = " + self.language)
            ok = True
        return ok

    def establish_dirs(self):
        self.working_dir = tempfile.mkdtemp()
        # base_assignment_dir := directory with assignment directories in it
        #                        e.g. $FOO/homework
        # base_instructor_dir := dir off assign dir with particular homework
        #                        e.g. $FOO/homework/linked_list
        # instructor_dir      := dir off instructor dir with particular language
        #                        e.g. $FOO/homework/linked_list/cpp
        self.base_instructor_dir = os.path.join(self.base_assignment_dir, 
                                                self.assignment)
        self.instructor_dir = os.path.join(self.base_instructor_dir, self.language)
        is_ins_dir_present = os.path.isdir(self.instructor_dir)
        self.description_files = []
        self.description_files.append(os.path.abspath(os.path.join(self.base_instructor_dir, 'description-common.json')))
        self.description_files.append(os.path.abspath(os.path.join(self.instructor_dir, 'description.json')))
        return is_ins_dir_present

    def avoid_file(self, path):
        m = re.match(RetroGrade.AVOID, path);
        return m is not None

    def copy_files(self):
        self.verbose_log( "About to copy files to working directory: " + self.working_dir)
        ok = True
        try:
            self.verbose_log( "Copying Student files...")
            for file in self.files:
                if (not self.avoid_file(file)):
                    self.verbose_log( "  ... " + file)
                    shutil.copy(file, self.working_dir)
            self.verbose_log( "Copied Student files.")
            self.verbose_log( "Copying Instructor files...")
            instructor_files = glob.glob(os.path.join(self.instructor_dir, "*"))
            for file in instructor_files:
                if (not self.avoid_file(file)):
                    start, end = os.path.split(file)
                    self.verbose_log( "  ... " + end )
                    shutil.copy(file, self.working_dir)
            self.verbose_log( "Copied Instructor files.")
        except Exception, x:
            self.verbose_log( (str(x)))
            traceback.print_stack()
            ok = False
        if (ok):
            self.verbose_log( "Copy files successful ")
        else:
            self.verbose_log( "One or more files did not copy. See stack trace.")
        return ok

    def invoke_grade_script(self):
        self.verbose_log( "Invoking grade script")
        ok_result_tuple = (False, {})
        try:
            self.verbose_log( "Changing directory to " + self.working_dir)
            os.chdir(self.working_dir)
            self.verbose_log( "... successfully changed directory.")
            self.verbose_log("Using description files: " + \
                                 " ".join(self.description_files))
            assign = assignment.Assignment(self.description_files)
            self.verbose_log( "... got assignment instance.")
            self.verbose_log( "Invoking grade()...")
            ok_result_tuple = assign.grade()
            self.verbose_log(assign.get_verbose_log())

        except Exception, e:
            traceback.print_exc()
        return ok_result_tuple


    def verbose_log(self, words):
        self.verbose.append(words)

    def get_verbose_log(self):
        return "\n".join(self.verbose)


def format_results(results):
    sb = []
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
        sb.append(labelf.format(k) + numf.format(p) + sep + numf.format(max_possible) + "\n")
    sb.append("\n" + labelf.format("TOTAL") + numf.format(total_score) + sep + numf.format(total_possible_score) + "\n")
    return "".join(sb)

def extract_score(results):
    """
    Returns an tuple of two integers. The first is the student score,
    the second is the total number of possible points.
    """
    total_score = 0;
    total_possible_score = 0;
    for k in results.keys():
        total_score = total_score + results[k][0]
        total_possible_score = total_possible_score + results[k][1]
    return (total_score, total_possible_score)

def start():
    parser = argparse.ArgumentParser()
    parser.add_argument("instructor_dir",
                        help="top level directory for instructor assignments")
    parser.add_argument("assignment", 
                        help="specify the homework assignment (e.g. 'linked list')")
    parser.add_argument("student_id", 
                        help="specify the student (e.g. '978675643')")
    parser.add_argument("student_file", 
                        help="specify student input files (e.g. 'linked_list.cpp')",
                        metavar="student_file",
                        nargs="+")
                        
    args = parser.parse_args()
    rg = RetroGrade(args.instructor_dir, args.assignment, 
                    args.student_id, args.student_file)
    print rg.get_verbose_log()
    print format_results(rg.result_map)
    
        

if __name__ == '__main__':
    start()
        
