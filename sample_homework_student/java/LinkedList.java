/*

  LinkedList.java

  This is the implementation of the methods declared in the interface
  (LinkedListInterface.java). 

 */

// AUTHOR: <Your name here. Don't include student ID>

// WHAT: CSCI 1300 Assignment N

// COLLABORATORS: <List of EVERYBODY you worked with, including instructors, 
//                     TAs, and other students. Include people you helped.>
//                <List of EVERY WEB SITE you consulted substantially>
//                <Don't worry! Collaboration is encouraged. This is not cheating.>

public class LinkedList implements LinkedListInterface {

    public LinkedList() {

    }

    public Node initNode(int data) {
	Node ret = new Node();
	ret.data = data;
	ret.next = null;
	return ret;
    }

    public String report(Node root) {
	StringBuilder buf = new StringBuilder();
	for (Node cursor = root.next; cursor != null; cursor = cursor.next) {
	    buf.append(cursor.data + " ");
	}
	return buf.toString();
    }

    public void insertData(Node parent, int data) {
	Node child = initNode(data);
	insert(parent, child);
    }

    public void insert(Node parent, Node child) {
	if (parent.next == null) {
	    parent.next = child;
	} else if (parent.next.data >= child.data) {
	    Node nextnext = parent.next;
	    parent.next = child;
	    child.next = nextnext;
	} else {
	    insert(parent.next, child);
	}
    }
    
    
    public void removeData(Node parent, int data) {
	if (parent.next == null) {
	    // nothing
	}

	// condition 2. remove one node by resetting parent.next to point
	// to child's next.
	else if (parent.next.data == data) {
	    parent.next = parent.next.next;
	}

	// condition 3. keep going by calling remove on parent.next
	else if (parent.next.data < data) {
	    removeData(parent.next, data);
	}

	// condition 4. stop because we won't find it.
	else {
	    // nothing
	}
    }
    
    public int size(Node root) {
	// return the number of non-root nodes in this list
	int count = 0;
	for(Node cursor = root.next; cursor != null; cursor = cursor.next) {
	    count++;
	}
	return count;
    }
    
    public boolean contains(Node root, int data) {
	// Return true if the target data is in the linked list, false otherwise.
	boolean ret = false;
	for (Node cursor = root.next; cursor != null; cursor = cursor.next) {
	    if (cursor.data == data) {
		ret = true;
		break;
	    } else if (cursor.data > data) {
		break;
	    }
	}
	return ret;
    }

}
