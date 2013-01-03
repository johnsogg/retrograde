from AssignmentBase import AssignmentBase

class Assignment(AssignmentBase):
    def __init__(self):
        super(Assignment, self).__init__()
        self.assignment = "Linked Lists"
        self.lang = "java"
        self.build_command = "javac -classpath junit.jar:. LinkedList.java LinkedListTest.java"
        self.unit_test_command = "java -classpath junit.jar:. LinkedListTest"
        self.instructor_files = [
            "RetroPrinter.java",
            "LinkedListInterface.java",
            "LinkedListTest.java",
            "Node.java",
            ]
        self.student_files = [
            "LinkedList.java",
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


