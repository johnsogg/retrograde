from AssignmentBase import AssignmentBase

class Assignment(AssignmentBase):
    def __init__(self):
        super(Assignment, self).__init__()
        self.assignment = "Linked Lists"
        self.lang = "py"
        self.build_command = None
        self.unit_test_command = "python linked_list_test.py"
        self.instructor_files = [
            "linked_list_test.py"
            ]
        self.student_files = [
            "linked_list.py"
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
