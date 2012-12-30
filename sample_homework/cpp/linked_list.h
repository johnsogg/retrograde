/*

  linked_list.h

  This is a sample header file for student homework assignments in
  1300 and 2270. This is provided to students as-is, with the possible
  exception of struct members and (later on) inline class member
  definitions.

 */

#ifndef __linked_list__
#define __linked_list__

#include <iostream>
#include <string>

struct node {
  int data;
  node* next;
};

node* init_node(int data);

std::string report(node* root);

void insert(node* parent, node* child);

void insert_data(node* parent, int data);

void remove_data(node* parent, int data);

int size(node* root);

bool contains(node* root, int data);

#endif /* defined __linked_list__ */
