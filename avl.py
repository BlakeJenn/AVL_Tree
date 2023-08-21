# Name: Blake Jennings
# GitHub: BlakeJenn
# Email: blakej94@gmail.com
# Description: An AVL tree with various methods


import random
from queue_and_stack import Queue, Stack
from bst import BSTNode, BST


class AVLNode(BSTNode):
    """
    AVL Tree Node class. Inherits from BSTNode
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    def __init__(self, value: object) -> None:
        """
        Initialize a new AVL node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(value)

        # new variables needed for AVL
        self.parent = None
        self.height = 0

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'AVL Node: {}'.format(self.value)


class AVL(BST):
    """
    AVL Tree class. Inherits from BST
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize a new AVL Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(start_tree)

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        super()._str_helper(self._root, values)
        return "AVL pre-order { " + ", ".join(values) + " }"

    def is_valid_avl(self) -> bool:
        """
        Perform pre-order traversal of the tree. Return False if there
        are any problems with attributes of any of the nodes in the tree.

        This is intended to be a troubleshooting 'helper' method to help
        find any inconsistencies in the tree after the add() or remove()
        operations. Review the code to understand what this method is
        checking and how it determines whether the AVL tree is correct.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                # check for correct height (relative to children)
                left = node.left.height if node.left else -1
                right = node.right.height if node.right else -1
                if node.height != 1 + max(left, right):
                    return False

                if node.parent:
                    # parent and child pointers are in sync
                    if node.value < node.parent.value:
                        check_node = node.parent.left
                    else:
                        check_node = node.parent.right
                    if check_node != node:
                        return False
                else:
                    # NULL parent is only allowed on the root of the tree
                    if node != self._root:
                        return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        Adds a new value to the AVL search tree.
        After adding the value, it re-balances the tree.

        :param value: value of the node to add to the tree

        :return:      None
        """
        if self._root is None:
            self._root = AVLNode(value)
            return
        parent = self._root
        cur = self._root
        while cur is not None:
            parent = cur
            if cur.value == value:
                return
            elif value < cur.value:
                cur = cur.left
            else:
                cur = cur.right
        cur = AVLNode(value)
        cur.height = 0
        cur.parent = parent
        if cur.value < parent.value:
            parent.left = cur
        else:
            parent.right = cur
        while parent is not None:
            self._rebalance(parent)
            cur = parent
            parent = parent.parent
        self._root = cur

    def remove(self, value: object) -> bool:
        """
        Removes a value from the AVL search tree if it exists in the tree.
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
        elif cur.right is None and cur.left is not None:
            parent = cur.parent
            self._remove_one_subtree(parent, cur)
            cur = cur.left
        elif cur.right is not None and cur.left is None:
            parent = cur.parent
            self._remove_one_subtree(parent, cur)
            cur = cur.right
        else:
            self._remove_no_subtrees(parent, cur)
        if self._root is None:
            return True
        while parent is not None:
            self._rebalance(parent)
            cur = parent
            parent = parent.parent
        self._root = cur
        return True

    def _remove_no_subtrees(self, remove_parent: AVLNode, remove_node: AVLNode) -> None:
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
        if remove_parent:
            self._rebalance(remove_parent)

    def _remove_one_subtree(self, remove_parent: AVLNode, remove_node: AVLNode) -> None:
        """
        Removes a node with one subtree. Called on by remove method.

        :param remove_parent: Parent node of node to remove
        :param remove_node:   Node to remove from tree with one subtree

        :return:              None
        """
        if remove_node == self._root:
            if self._root.right:
                self._root = self._root.right
                self._root.parent = None
            else:
                self._root = self._root.left
                self._root.parent = None
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
        if remove_parent:
            self._rebalance(remove_parent)

    def _remove_two_subtrees(self, remove_parent: AVLNode, remove_node: AVLNode) -> None:
        """
        Removes a node with two subtrees. Called on by remove method.

        :param remove_parent: Parent node of node to remove
        :param remove_node:   Node to remove from tree with two subtrees

        :return:              None
        """
        remove_node.value = self.leftmost(remove_node, remove_node.right)
        if remove_node.right:
            self._rebalance(remove_node.right)
        self._rebalance(remove_node)

    def leftmost(self, parent: AVLNode, node: AVLNode) -> object:
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
        while cur_parent is not None:
            self._rebalance(cur_parent)
            cur_parent = cur_parent.parent
        return final

    def _balance_factor(self, node: AVLNode) -> int:
        """
        Finds the balance factor of a Node in the AVL tree.

        :param node: Node to find balance factor

        :return:     integer representing balance factor of Node
        """
        left = -1
        right = -1
        if node.left is not None:
            left = node.left.height
        if node.right is not None:
            right = node.right.height
        return right - left

    def _get_height(self, node: AVLNode) -> int:
        """
        Finds the height of an individual node in an AVL tree.

        :param node: Node to find height of

        :return:     integer representing height of Node
        """
        return node.height

    def _rotate_left(self, node: AVLNode) -> AVLNode:
        """
        Rotates an unbalanced tree or subtree in an AVL tree by
        using a left rotation.

        :param node: Parent node to rotate

        :return:     child Node rotated to become the new root
        """
        child = node.right
        node.right = child.left
        if node.right is not None:
            node.right.parent = node
        child.left = node
        child.parent = node.parent
        node.parent = child
        self._update_height(node)
        self._update_height(child)
        return child

    def _rotate_right(self, node: AVLNode) -> AVLNode:
        """
        Rotates an unbalanced tree or subtree in an AVL tree by
        using a right rotation.

        :param node: Parent node to rotate

        :return:     child Node rotated to become the new root
        """
        child = node.left
        node.left = child.right
        if node.left is not None:
            node.left.parent = node
        child.right = node
        child.parent = node.parent
        node.parent = child
        self._update_height(node)
        self._update_height(child)
        return child

    def _update_height(self, node: AVLNode) -> None:
        """
        Updates the height value of an individual Node in the AVL tree.

        :param node: Node to update height value of

        :return:     None
        """
        left = -1
        right = -1
        if node.left:
            left = node.left.height
        if node.right:
            right = node.right.height
        node.height = max(left, right) + 1

    def _rebalance(self, node: AVLNode) -> None:
        """
        Determines if a Node tree or subtree is unbalanced and balances it accordingly.

        :param node: current Node to determine if it is unbalanced

        :return:     None
        """
        if self._balance_factor(node) < -1:
            if self._balance_factor(node.left) > 0:
                node.left = self._rotate_left(node.left)
                node.left.parent = node
            parent_hold = node.parent
            newSubtreeRoot = self._rotate_right(node)
            newSubtreeRoot.parent = parent_hold
            if newSubtreeRoot.parent:
                if newSubtreeRoot.value < newSubtreeRoot.parent.value:
                    newSubtreeRoot.parent.left = newSubtreeRoot
                elif newSubtreeRoot.value > newSubtreeRoot.parent.value:
                    newSubtreeRoot.parent.right = newSubtreeRoot
        elif self._balance_factor(node) > 1:
            if self._balance_factor(node.right) < 0:
                node.right = self._rotate_right(node.right)
                node.right.parent = node
            parent_hold = node.parent
            newSubtreeRoot = self._rotate_left(node)
            newSubtreeRoot.parent = parent_hold
            if newSubtreeRoot.parent:
                if newSubtreeRoot.value < newSubtreeRoot.parent.value:
                    newSubtreeRoot.parent.left = newSubtreeRoot
                elif newSubtreeRoot.value > newSubtreeRoot.parent.value:
                    newSubtreeRoot.parent.right = newSubtreeRoot
        else:
            self._update_height(node)

# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    tree = AVL([50, 40, 60, 30, 70, 20, 80, 45])
    tree.remove(45)
    if not tree.is_valid_avl():
        raise Exception("PROBLEM WITH REMOVE OPERATION")

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),  # RR
        (3, 2, 1),  # LL
        (1, 3, 2),  # RL
        (3, 1, 2),  # LR
    )
    for case in test_cases:
        tree = AVL(case)
        print(tree)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),   # RR, RR
        (10, 20, 30, 50, 40),   # RR, RL
        (30, 20, 10, 5, 1),     # LL, LL
        (30, 20, 10, 1, 5),     # LL, LR
        (5, 4, 6, 3, 7, 2, 8),  # LL, RR
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = AVL(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL()
        for value in case:
            tree.add(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),  # no AVL rotation
        ((1, 2, 3), 2),  # no AVL rotation
        ((1, 2, 3), 3),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),  # no AVL rotation
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),  # RR
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),  # LL
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),  # RL
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),  # LR
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = AVL(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)


    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = AVL(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 5")
    print("-------------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL(case)
        for value in case[::2]:
            tree.remove(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
    print('remove() stress test finished')

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = AVL([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = AVL()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
