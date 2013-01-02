import unittest

from tree import Tree, Node

class TestTree(unittest.TestCase):
    """
        When I pick this up again, this is what should be done:
        
        1. Make a special subclass of TestCase with the __init__ and __str__ 
        functions as below. Call it RetroTestCase All my tests will subclass 
        that one.
        
        2. Make an abstract class 'RetroSuite' that builds and runs the suite.
        
        3. Then, to make a concrete test set, subclass RetroSuite and supply
        it with the RetroTestCase info (as done in the __main__ section below).
    """

    def __init__(self, methodName, humanName, maxPts):
        super(TestTree, self).__init__(methodName) # call superconstructor
        self.methodName = methodName # record method name, e.g. 'testInsert'
        self.humanName = humanName # record user-legible name, e.g. "Insert Data"
        self.maxPts = maxPts # maximum number of points for this test if passed
        self.points = 0 # actual amount awarded (either 0 or maxPts)

    def setUp(self):
        """
            My RetroTestCase subclass will have to implement this.
        """
        self.tree = Tree()

    def testInsert(self):
        """
            My RetroTestCase subclass will implement a bunch of testXYZ functions.
        """
        self.assertEquals(self.tree.size(), 0)
        self.tree.insert(Node(7))
        self.assertEquals(self.tree.size(), 1)
        self.tree.bulk_insert(7,3,4,5,3,4,6,6,2,1,10)
        self.assertEquals(self.tree.size(), 12)
        self.assertEquals(self.tree.size(), 3)

    def testRemove(self):
        pass
    
    def testNothing(self):
        """
            An existence function. RetroTestCase ought to have this one (don't
            leave it to subclass) so students get a point for at least getting
            their homework submitted.
        """
        pass

    def __str__(self):
        """
            RetroTestCase includes this.
        """
        return self.humanName

class SpecialResult(unittest.TestResult):
    """
        RetroResult will basically be just like this, assuming 'test' is a
        RetroTestCase.
    """
    def addSuccess(self, test):
        print ("Test successful: " + str(test))
        test.points = test.maxPts

    def addFailure(self, test, err):
        print ("Test failed: " + str(test) + ": " + str(err))

    def addError(self, test, err):
        print ("Test error: " + str(test) + ": " + str(err))

if __name__ == '__main__':
    """
        This is the controller, RetroSuite. Parts are abstract (so they will be in
        the RetroSuite class) and others are concrete (will be implemented in the
        homework assignment's RetroSuite subclass implementation). They are marked
        accordingly below.
    """
    suite = unittest.TestSuite() # abstract
    tests = [ # concrete. This list is established in the subclass constructor.
             TestTree('testNothing', 'Existence', 1),  # exclude this one, though
             TestTree('testInsert', 'Insert Data', 4), # include this and friends
             TestTree('testRemove', 'Remove Data', 4), 
        ]
    # Everything below here is abstract ---------------------------------
    for test in tests:
        suite.addTest(test)
    
    result = SpecialResult()
    suite.run(result)
    maxPoints = 0
    earnedPoints = 0
    print "\n------------------------------- Line Item Report"
    label = "{:>30} : "
    numf = "{:>3}"
    sep = "   /   "
    for test in tests:
        print(label.format(test.humanName) + numf.format(str(test.points)) + sep + numf.format(str(test.maxPts)))
        maxPoints = maxPoints + test.maxPts
        earnedPoints = earnedPoints + test.points

    print "\n------------------------------- Summary"
    print label.format("Score") + numf.format(str(earnedPoints)) + sep + numf.format(str(maxPoints))
