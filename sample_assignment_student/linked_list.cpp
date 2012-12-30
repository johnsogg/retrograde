/*

  linked_list.cpp

  This is the definition of the functions declared in the
  corresponding header file (linked_list.h). This will be nearly
  blank, with the exception of the top matter stuff like the
  who/what/when/where block, the include statement, the namespace std
  statement, and possibly comments on what to do.

 */

// AUTHOR: <Your name here. Don't include student ID>

// WHAT: CSCI 1300 Assignment N

// COLLABORATORS: <List of EVERYBODY you worked with, including instructors, 
//                     TAs, and other students. Include people you helped.>
//                <List of EVERY WEB SITE you consulted substantially>
//                <Don't worry! Collaboration is encouraged. This is not cheating.>

#include "linked_list.h"
#include <sstream>

using namespace std;

node* init_node(int data) {
  node* ret = new node;
  ret->data = data;
  ret->next = NULL;
  return ret;
}

string report(node* root) {
  stringstream ret_stream;
  for (node* cursor = root->next; cursor != NULL; cursor = cursor->next) {
    ret_stream << cursor->data << " ";
  }
  return ret_stream.str();
}

void insert_data(node* parent, int data) {
  node* child = init_node(data);
  insert(parent, child);
}

void insert(node* parent, node* child) {
  // this function inserts 'child' somewhere after parent.
  // possible conditions:
  //   1. 'parent' has no next node
  //   2. 'parent->next->data' is greater than or equal to 'child->data'
  //   3. 'parent->next->data' is less than 'child->data'.

  // condition 1. simply set parent->next to point to child
  if (parent->next == NULL) {
    parent->next = child;
  }

  // condition 2. insert child between parent and parent->next
  else if (parent->next->data >= child->data) {
    node* nextnext = parent->next;
    parent->next = child;
    child->next = nextnext;
  }

  // condition 3. use this insertion function to try again
  else {
    insert(parent->next, child);
  }
}

void remove_data(node* parent, int data) {
  // removes exactly zero or one nodes that come after 'parent' that
  // have the same data value.
  
  // conditions:
  //   1. parent has no next node.
  //   2. parent has a next node and its data value matches our target
  //   3. parent has a next node and its data value is less than our target
  //   4. parent has a next node and its data value is greater than our target

  // condition 1. stop.
  if (parent->next == NULL) {
    // nothing
  }

  // condition 2. remove one node by resetting parent->next to point
  // to child's next.
  else if (parent->next->data == data) {
    parent->next = parent->next->next;
  }

  // condition 3. keep going by calling remove on parent->next
  else if (parent->next->data < data) {
    remove_data(parent->next, data);
  }

  // condition 4. stop because we won't find it.
  else {
    // nothing
  }
}

int size(node* root) {
  // return the number of non-root nodes in this list
  int count = 0;
  for(node* cursor = root->next; cursor != NULL; cursor = cursor->next) {
    count++;
  }
  return count;
}


bool contains(node* root, int data) {
  // Return true if the target data is in the linked list, false otherwise.
  bool ret = false;
  for (node* cursor = root->next; cursor != NULL; cursor = cursor->next) {
    //    cout << "Cursor data: " << cursor->data << endl;
    if (cursor->data == data) {
      //      cout << "definitely contains " << data << endl;
      ret = true;
      break;
    } else if (cursor->data > data) {
      //      cout << "definitely does not contain " << data << endl;
      break; // no longer possible for target to be found
    }
  }
  //  cout << "Done with contains. Returning " << ret << endl;
  return ret;
}
