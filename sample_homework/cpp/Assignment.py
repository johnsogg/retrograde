from AssignmentBase import AssignmentBase

class Assignment(AssignmentBase):
    def __init__(self):
        super(Assignment, self).__init__()
        self.assignment = "Linked Lists"
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


