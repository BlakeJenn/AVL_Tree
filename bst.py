# Name: Blake Jennings
# GitHub: BlakeJenn
# Email: blakej94@gmail.com
# Description: A binary search tree with various methods


import random
from queue_and_stack import Queue, Stack


class BSTNode:
    """
    Binary Search Tree Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        """
        Initialize a new BST node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.value = value   # to store node's data
        self.left = None     # pointer to root of left subtree
        self.right = None    # pointer to root of right subtree

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'BST Node: {}'.format(self.value)


class BST:
    """
    Binary Search Tree class
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize new Binary Search Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._root = None

        # populate BST with initial values (if provided)
        # before using this feature, implement add() method
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self) -> str:
        """
        Override string method; display in pre-order
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        self._str_helper(self._root, values)
        return "BST pre-order { " + ", ".join(values) + " }"

    def _str_helper(self, node: BSTNode, values: []) -> None:
        """
        Helper method for __str__. Does pre-order tree traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if not node:
            return
        values.append(str(node.value))
        self._str_helper(node.left, values)
        self._str_helper(node.right, values)

    def get_root(self) -> BSTNode:
        """
        Return root of tree, or None if empty
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._root

    def is_valid_bst(self) -> bool:
        """
        Perform pre-order traversal of the tree.
        Return False if nodes don't adhere to the bst ordering property.

        This is intended to be a troubleshooting method to help find any
        inconsistencies in the tree after the add() or remove() operations.
        A return of True from this method doesn't guarantee that your tree
        is the 'correct' result, just that it satisfies bst ordering.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                if node.left and node.left.value >= node.value:
                    return False
                if node.right and node.right.value < node.value:
                    return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        Adds a new value to the binary search tree.

        :param value: value of the node to add to the tree

        :return:      None
        """
        if self._root is None:
            self._root = BSTNode(value)
            return
        parent = None
        cur = self._root
        while cur is not None:
            parent = cur
            if value < cur.value:
                cur = cur.left
            else:
                cur = cur.right
        cur = BSTNode(value)
        if cur.value < parent.value:
            parent.left = cur
        else:
            parent.right = cur

    def remove(self, value: object) -> bool:
        """
        Removes a value from the binary search tree if it exists in the tree.
        If a value is removed, it re-balances the tree.

        :param value: value of the node to remove from the tree

        :return:      True if value is found and removed
                      False otherwise
        """
        cur = self._root
        parent = cur
        while cur is not None and cur.value != value:
            parent = cur
            if value < cur.value:
                cur = cur.left
            else:
                cur = cur.right
        if cur is None:
            return False
        elif cur.right is not None and cur.left is not None:
            self._remove_two_subtrees(parent, cur)
            return True
        elif cur.right is None and cur.left is not None:
            self._remove_one_subtree(parent, cur)
            return True
        elif cur.right is not None and cur.left is None:
            self._remove_one_subtree(parent, cur)
            return True
        else:
            self._remove_no_subtrees(parent, cur)
            return True

    def _remove_no_subtrees(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        Removes a node with no subtrees. Called on by remove method.

        :param remove_parent: Parent node of node to remove
        :param remove_node:   Node to remove from tree with 0 subtrees

        :return:              None
        """
        if remove_node == self._root:
            self._root = None
        elif remove_node.value < remove_parent.value:
            remove_parent.left = None
        else:
            remove_parent.right = None

    def _remove_one_subtree(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        Removes a node with one subtree. Called on by remove method.

        :param remove_parent: Parent node of node to remove
        :param remove_node:   Node to remove from tree with one subtree

        :return:              None
        """
        if remove_node == self._root:
            if self._root.right:
                self._root = self._root.right
            else:
                self._root = self._root.left
        elif remove_node.right is not None:
            if remove_node.value < remove_parent.value:
                remove_parent.left = remove_node.right
            else:
                remove_parent.right = remove_node.right
        else:
            if remove_node.value < remove_parent.value:
                remove_parent.left = remove_node.left
            else:
                remove_parent.right = remove_node.left

    def _remove_two_subtrees(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        Removes a node with two subtrees. Called on by remove method.

        :param remove_parent: Parent node of node to remove
        :param remove_node:   Node to remove from tree with two subtrees

        :return:              None
        """
        remove_node.value = self.leftmost(remove_node, remove_node.right)

    def leftmost(self, parent: BSTNode, node: BSTNode) -> object:
        """
        Finds the leftmost value of the right subtree of a Node with
        two subtrees that is being removed. Called on by
        _remove_two_subtrees method.
        
        :param parent: Node to remove from tree with two subtrees
        :param node:   Right child Node of Node to be removed

        :return:       Value of leftmost node of right subtree
        """
        cur = node
        cur_parent = parent
        if cur.left is None:
            final = cur.value
            cur_parent.right = cur.right
            return final
        while cur.left is not None:
            cur_parent = cur
            cur = cur.left
        final = cur.value
        cur_parent.left = cur.right
        return final

    def contains(self, value: object) -> bool:
        """
        Determines if the binary search tree contains a Node with
        the designated value.

        :param value: Value to determine if the tree contains

        :return:      True if the value is in the binary search tree
                      False otherwise
        """
        if self._root is None:
            return False
        cur = self._root
        while cur is not None:
            if cur.value == value:
                return True
            if value < cur.value:
                cur = cur.left
            else:
                cur = cur.right
        return False

    def inorder_traversal(self) -> Queue:
        """
        Inorder traverses the binary search tree and creates a Queue object
        of all the values of the nodes it traverses.

        :return: Queue object of values traversed
        """
        final = Queue()
        self.traverse_rec_helper(self._root, final)
        return final

    def traverse_rec_helper(self, node: BSTNode, queue: Queue) -> None:
        """
        Helper method to recursively inorder traverse the binary search tree.

        :param node:  Current node being traversed in the tree
        :param queue: Queue object to add values to

        :return:      None
        """
        if node is not None:
            self.traverse_rec_helper(node.left, queue)
            queue.enqueue(node.value)
            self.traverse_rec_helper(node.right, queue)
        return

    def find_min(self) -> object:
        """
        Returns the lowest value in the binary search tree.

        :return: Lowest value object in the tree
        """
        if self._root is None:
            return None
        final = self.inorder_traversal()
        return final.dequeue()

    def find_max(self) -> object:
        """
        Returns the highest value in the binary search tree.

        :return: Highest value object in the tree
                 None if tree is empty
        """
        if self._root is None:
            return None
        final = Queue()
        self.max_helper(self._root, final)
        return final.dequeue()

    def max_helper(self, node: BSTNode, queue: Queue) -> None:
        """
        Helper method to recursively traverse the tree.

        :param node:  Current node traversed in the tree
        :param queue: Queue help return the highest value

        :return:      None
        """
        if node is not None:
            self.max_helper(node.right, queue)
            queue.enqueue(node.value)
            self.max_helper(node.left, queue)
        return

    def is_empty(self) -> bool:
        """
        Determines if the binary search tree is empty.

        :return: True if tree is empty
                 False otherwise
        """
        return self._root is None

    def make_empty(self) -> None:
        """
        Empties the binary search tree of all of its Nodes.

        :return: None
        """
        self._root = None


# ------------------- BASIC TESTING -----------------------------------------

if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),
        (3, 2, 1),
        (1, 3, 2),
        (3, 1, 2),
    )
    for case in test_cases:
        tree = BST(case)
        print(tree)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),
        (10, 20, 30, 50, 40),
        (30, 20, 10, 5, 1),
        (30, 20, 10, 1, 5),
        (5, 4, 6, 3, 7, 2, 8),
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = BST(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = BST()
        for value in case:
            tree.add(value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),
        ((1, 2, 3), 2),
        ((1, 2, 3), 3),
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = BST(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = BST(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
        print('RESULT :', tree)


    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = BST([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = BST()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
    
