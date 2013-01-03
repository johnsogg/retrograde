import unittest, traceback

from linked_list import *

class RetroTest(unittest.TestCase):
    
    def __init__(self, methodName, outputName):
        super(RetroTest, self).__init__(methodName) # call superconstructor
        self.outputName = outputName

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testReport(self):
        top = init_node(0)
        exp = ""
        output = report(top)
        self.assertIsNotNone(output, "List report method should never return None")
        output = output.strip()
        self.assertEqual(exp, output, "Empty list should report '' or ' '")
        one = init_node(1)
        two = init_node(2)
        top.next = one
        one.next = two
        exp = "1 2"
        output = report(top).strip()
        self.assertEqual(exp, output, "List should report '1 2' or '1 2 '")
        
    def testInitNode(self):
        pass

    def testInsertEmpty(self):
        pass

    def testInsertStart(self):
        pass

    def testInsertEnd(self):
        pass
    
    def testInsertRedundant(self):
        pass

    def testRemove(self):
        pass

# The RetroPrinter class should be moved to a common area, like RetroPrinter.cpp
class RetroPrinter(unittest.TestResult):
    """
        RetroResult will basically be just like this, assuming 'test' is a
        RetroTestCase.
    """

    def give_result(self, name, status):
        print "RetroGrade Result > " + name + ": " + status

    def complain(self, err):
        error_type = str(err[0])
        error_value = str(err[1])
        error_trace = err[2]
        print error_value
        traceback.print_tb(error_trace)

    def addSuccess(self, test):
        self.give_result(test.outputName, "+")

    def addFailure(self, test, err):
        self.give_result(test.outputName, "-")
        self.complain(err)

    def addError(self, test, err):
        self.give_result(test.outputName, "-")
        self.complain(err)


if __name__ == '__main__':
    suite = unittest.TestSuite() 
    tests = [ 
        RetroTest("testReport", "Report"),
        RetroTest("testInitNode", "InitNode"),
        RetroTest("testInsertEmpty", "InsertEmpty"),
        RetroTest("testInsertStart", "InsertStart"),
        RetroTest("testInsertEnd", "InsertEnd"),
        RetroTest("testInsertRedundant", "InsertRedundant"),
        RetroTest("testRemove", "Remove"),
        ]

    for test in tests:
        suite.addTest(test)
    
    result = RetroPrinter()
    print "Running Python test suite..."
    suite.run(result)
    print "... done running Python test suite."

