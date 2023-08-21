# AVL_Tree
A BST and AVL Tree that utilizes queues and stacks

BST methods:

add(self, value: object) -> None:
This method adds a new value to the tree. Duplicate values are allowed. If a node with
that value is already in the tree, the new value should be added to the right subtree of that
node. It is implemented with O(N) runtime complexity.

remove(self, value: object) -> bool:
This method removes a value from the tree. The method returns True if the value is
removed. Otherwise, it returns False. It is implemented with O(N) runtime
complexity.

contains(self, value: object) -> bool:
This method returns True if the value is in the tree. Otherwise, it returns False. If the tree is
empty, the method should return False. It is implemented with O(N) runtime
complexity.

inorder_traversal(self) -> Queue:
This method will perform an inorder traversal of the tree and return a Queue object that
contains the values of the visited nodes, in the order they were visited. If the tree is empty,
the method returns an empty Queue. It is implemented with O(N) runtime
complexity.

find_min(self) -> object:
This method returns the lowest value in the tree. If the tree is empty, the method should
return None. It is implemented with O(N) runtime complexity.

find_max(self) -> object:
This method returns the highest value in the tree. If the tree is empty, the method should
return None. It is implemented with O(N) runtime complexity.

is_empty(self) -> bool:
This method returns True if the tree is empty. Otherwise, it returns False. It is
implemented with O(1) runtime complexity.

make_empty(self) -> None:
This method removes all of the nodes from the tree. It is implemented with O(1)
runtime complexity.


AVL Methods:

add(self, value: object) -> None:
This method adds a new value to the tree while maintaining its AVL property. Duplicate
values are not allowed. If the value is already in the tree, the method should not change
the tree. It is implemented with O(log N) runtime complexity.

remove(self, value: object) -> bool:
This method removes the value from the AVL tree. The method returns True if the value is
removed. Otherwise, it returns False. It is implemented with O(log N) runtime
complexity.

