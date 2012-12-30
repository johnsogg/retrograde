/*

  linked_list_test.cpp

  This is a sample/template unit test for RetroGrade assignments. To
  make your own, copy this file somewhere, and replace references to
  'LinkedList' to whatever the assignment is about (just be
  consistent). Then, make a bunch of TEST macro implementations. Keep
  the main() function as it is. When run, the program will output
  something like the following:

  RetroGrade >	 Test LinkedListTest.Report starting.
  RetroGrade Result >	 Report: +
  RetroGrade >	 Test LinkedListTest.InitNode starting.
  RetroGrade Result >	 InitNode: +
  RetroGrade >	 Test LinkedListTest.InsertEmpty starting.
  RetroGrade Result >	 InsertEmpty: +
  RetroGrade >	 Test LinkedListTest.InsertStart starting.
  RetroGrade Result >	 InsertStart: +
  RetroGrade >	 Test LinkedListTest.InsertEnd starting.
  RetroGrade Result >	 InsertEnd: +
  RetroGrade >	 Test LinkedListTest.InsertRedundant starting.
  RetroGrade Result >	 InsertRedundant: +
  RetroGrade >	 Test LinkedListTest.Remove starting.
  RetroGrade >	 *** Failsauce in ./linked_list_test.cpp:111
  Value of: 2
  Expected: 1
  This failure was manufactured for the sake of example.
  RetroGrade Result >	 Remove: -
  Retro> TEST FAILED

  If the output is filtered by lines that start with "RetroGrade
  Result >", it is easier to see from a high level what happened:

  RetroGrade Result >	 Report: +
  RetroGrade Result >	 InitNode: +
  RetroGrade Result >	 InsertEmpty: +
  RetroGrade Result >	 InsertStart: +
  RetroGrade Result >	 InsertEnd: +
  RetroGrade Result >	 InsertRedundant: +
  RetroGrade Result >	 Remove: -

  This format should be consistent with the other testing programs for
  Python and Java, and whatever other languages are later
  supported. This testing program should be compiled and executed by a
  script that parses its output, computes a score, records results,
  and reports back to the user.

 */

#include "linked_list.h"
#include "gtest/gtest.h"
#include <iostream>
#include "RetroPrinter.h"
#include <string>

using ::testing::InitGoogleTest;
using ::testing::UnitTest;
using ::testing::TestEventListeners;
using std::string;
using std::cout;
using std::endl;

namespace {

// The fixture for testing linked lists
class LinkedListTest : public ::testing::Test {
private:

protected:
  
  LinkedListTest() {
  }

  virtual ~LinkedListTest() {
  }

  // If the constructor and destructor are not enough for setting up
  // and cleaning up each test, you can define the following methods:

  virtual void SetUp() {
    // Code here will be called immediately after the constructor (right
    // before each test).
  }

  virtual void TearDown() {
    // Code here will be called immediately after each test (right
    // before the destructor).
  }
}; // ends class LinkListTest

TEST(LinkedListTest, Report) {
  node* top = init_node(0);
  string exp ("");
  string out = report(top);
  EXPECT_NE(string::npos, out.find(exp, 0)) << "Empty list should report '' or ' '";
  node* one = init_node(1);
  node* two = init_node(2);
  top->next = one;
  one->next = two;
  exp = "1 2";
  out = report(top);
  EXPECT_NE(string::npos, out.find(exp, 0)) << "List should report '1 2' or '1 2 '";
}

TEST(LinkedListTest, InitNode) {
  node* top = init_node(1);
  EXPECT_EQ(1, top->data) << "Newly initialized node should have '0' for data";
  EXPECT_TRUE(top->next == NULL) << "Newly initialized node should have null 'next'";
}

TEST(LinkedListTest, InsertEmpty) {
  node* top = init_node(0);
  insert_data(top, 4);
  EXPECT_EQ(4, top->next->data) << "Inserting '4' in to empty list should result in a list containing one item (namely, a '4').";
}

TEST(LinkedListTest, InsertStart) {
  node* top = init_node(0);
  insert_data(top, 3);
  insert_data(top, 2);
  EXPECT_EQ(2, top->next->data) << "Inserting 3, then 2, into an empty list should result in a list containing 2, then 3, in that order.";
  EXPECT_EQ(3, top->next->next->data) << "Inserting 3, then 2, into an empty list should result in a list containing 2, then 3, in that order.";
}

TEST(LinkedListTest, InsertEnd) {
  node* top = init_node(0);
  insert_data(top, 3);
  insert_data(top, 2);
  insert_data(top, 6);
  EXPECT_EQ(2, top->next->data) << "Inserting 3, then 2, then 6 into an empty list should result in a list containing 2, then 3, then 6 in that order.";
  EXPECT_EQ(3, top->next->next->data) << "Inserting 3, then 2, then 6 into an empty list should result in a list containing 2, then 3, then 6 in that order.";
  EXPECT_EQ(6, top->next->next->next->data) << "Inserting 3, then 2, then 6 into an empty list should result in a list containing 2, then 3, then 6 in that order.";

}

TEST(LinkedListTest, InsertRedundant) {
  node* top = init_node(0);
  insert_data(top, 3);
  insert_data(top, 2);
  insert_data(top, 6);
  insert_data(top, 3);
  EXPECT_EQ(2, top->next->data) << "Inserting 3, 2, 6, 3 into an empty list should result in a list containing 2, 3, 3, then 6 in that order.";
  EXPECT_EQ(3, top->next->next->data) << "Inserting 3, 2, 6, 3 into an empty list should result in a list containing 2, 3, 3, then 6 in that order.";
  EXPECT_EQ(3, top->next->next->next->data) << "Inserting 3, 2, 6, 3 into an empty list should result in a list containing 2, 3, 3, then 6 in that order.";
  EXPECT_EQ(6, top->next->next->next->next->data) << "Inserting 3, 2, 6, 3 into an empty list should result in a list containing 2, 3, 3, then 6 in that order.";
}

TEST(LinkedListTest, Remove) {
  EXPECT_EQ(1, 2) << "This failure was manufactured for the sake of example.";
}

}  // namespace

int main(int argc, char **argv) {
  InitGoogleTest(&argc, argv);
  UnitTest& unit_test = *UnitTest::GetInstance();
  TestEventListeners& listeners = unit_test.listeners();

  // if we don't want the default listener printing anything, remove it:
  delete listeners.Release(listeners.default_result_printer());

  // if we do want our custom listener to record success/fail, add it:
  listeners.Append(new RetroPrinter);

  return RUN_ALL_TESTS();
}
