#!/usr/bin/env python

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

    def report_input(self):
        print "Created a RetroGrade instance."
        print "  Assignment:      " + self.assignment
        print "  Student:         " + self.student_id
        print "  Student Files:   " + ", ".join(self.files)

    def determine_language(self):
        ok = False;
        for file in self.files:
            print "File: " + file
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
            print "Could not determine language based on input files."
            print "Source files must end with '.java', '.py', or '.cpp'."
            ok = False
        else:
            print "Determined language = " + self.language
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
        return is_ins_dir_present

    def avoid_file(self, path):
        m = re.match(RetroGrade.AVOID, path);
        return m is not None

    def copy_files(self):
        print "About to copy files to working directory: " + self.working_dir
        ok = True
        try:
            print "Copying Student files..."
            for file in self.files:
                if (not self.avoid_file(file)):
                    print "  ... " + file
                    shutil.copy(file, self.working_dir)
            print "Copied Student files."
            print "Copying Instructor files..."
            instructor_files = glob.glob(os.path.join(self.instructor_dir, "*"))
            for file in instructor_files:
                if (not self.avoid_file(file)):
                    start, end = os.path.split(file)
                    print "  ... " + end 
                    shutil.copy(file, self.working_dir)
            print "Copied Instructor files."
        except Exception, x:
            print (str(x))
            traceback.print_stack()
            ok = False
        if (ok):
            print "Copy files successful "
        else:
            print "One or more files did not copy. See stack trace above."
        return ok

    def invoke_grade_script(self):
        print "Invoking grade script"
        ok_result_tuple = (False, {})
        try:
            print "Changing directory to " + self.working_dir
            os.chdir(self.working_dir)
            print "... successfully changed directory."
            print "Attempting to import and instantiate Assignment..."
            print "Assignment.py exists?" + str(os.path.exists("Assignment.py"))
            print "Appending working dir to sys.path..."
            sys.path.append(self.working_dir)
            print "Working dir appended. Should be able to import Assignment."
            from Assignment import Assignment
            assign = Assignment()
            print "... got assignment instance."
            print "Invoking grade()..."
            ok_result_tuple = assign.grade()

        except Exception, e:
            traceback.print_exc()
        return ok_result_tuple

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


if __name__ == '__main__':
    start()
