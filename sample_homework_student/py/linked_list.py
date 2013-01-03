#!/usr/bin/env python

class node:
    def __init__(self):
        self.data = 0
        self.next = None

def init_node(data):
    """
    Return an initialized node.
    """
    ret = node()
    ret.data = data
    return ret

def report(root):
    """
    Given a list, output the contents separated by spaces
    """
    sb = []
    cursor = root
    while (cursor.next is not None):
        sb.append(str(cursor.next.data))
        cursor = cursor.next
    ret = " ".join(sb)
    return ret

def insert(parent, child):
    """
    Insert the child node after the parent node.
    """
    pass

def insert_data(parent, data):
    """
    Create a node for the data and inser it after the parent node.
    """
    pass

def remove_data(parent, data):
    """
    Remove from the linked list a single node that contains this data.
    """
    pass

def size(root):
    """
    Report the size of this linked list.
    """
    pass

def contains(root, data):
    """
    Return True or False depending on if the list contains this data.
    """

