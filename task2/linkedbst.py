"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from linkedqueue import LinkedQueue
from math import log
import copy
from time import time
import random


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            snake = ""
            if node != None:
                snake += recurse(node.right, level + 1)
                snake += "| " * level
                snake += str(node.data) + "\n"
                snake += recurse(node.left, level + 1)
            return snake

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode == None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        "Return Position representing p's parent (or None if p is root)."
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return -1
            else:
                return 1 + max(height1(top.left), height1(top.right))
        return height1(self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        nnneee = self._size
        should_be = 2 * log((nnneee+1), 2) - 1
        if self.height() <= should_be:
            return True
        else:
            return False

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        lst = list(self.inorder())
        lst_result = []
        for i in lst:
            if i <= high and i >= low:
                lst_result.append(i)
        return lst_result
    def rebalance(self):
        """
        Rebalances the tree.
        :return:
        """

        bst1 = sorted(list(self.inorder()))
        self.clear()
        bst = LinkedBST()
        for j in bst1:
            bst.add(j)
        bal = []
        def append_items(lyst):
            if lyst:
                mid = len(lyst)//2
                bal.append(lyst[mid])
                append_items(lyst[:mid])
                append_items(lyst[(mid+1):])
        append_items(bst1)
        for el in bal:
            self.add(el)
        
    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        lyst = list(self)
        while len(lyst) != 0:
            minn = min(lyst)
            if minn > item:
                return minn
            else:
                del lyst[lyst.index(minn)]
        return None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        lyst = list(self)
        while len(lyst) != 0:
            minn = max(lyst)
            if minn < item:
                return minn
            else:
                del lyst[lyst.index(minn)]
        return None
        
    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        def get_words(path):
            with open(path) as f:
                lines = f.read().splitlines()
            return lines

        def check_list_find(lst):
            random_words = []
            while len(random_words) < 10000:
                word = random.choice(lst)
                random_words.append(word)
            start = time()
            for i in random_words:
                this_word = random_words.index(i)
            finish = time() - start
            return finish 
        
        def bst_find_words(lst):
            random_words = []
            while len(random_words) < 10000:
                word = random.choice(lst)
                random_words.append(word)
            bst = LinkedBST()
            for i in lst:
                bst.add(i)
            start = time()
            for j in range(10000):
                bst.find(random_words[j])
            finish = time() - start
            return finish
        
        def random_bst_find(lst):
            random_words = []
            bst = LinkedBST()
            lst1 = []
            for el in lst:
                chosen = random.choice(lst)
                lst1.append(chosen)
                random_words.append(chosen)
            while len(random_words) < 10000:
                word = random.choice(random_words)
                random_words.append(word)
            for i in lst1:
                bst.add(i)
            start = time()
            for j in range(10000):
                bst.find(random_words[j])
            finish = time() - start
            return finish
        
        def check_in_balanced(lst):
            random_words = []
            while len(random_words) < 10000:
                word = random.choice(lst)
                random_words.append(word)
            bst = LinkedBST()
            for i in lst:
                bst.add(i)
            bst.rebalance()
            start = time()
            for j in range(10000):
                bst.find(random_words[j])
            finish = time() - start
            return finish

        lst = get_words(path)[:990]
        print(f'In list by index: {round(check_list_find(lst), 2)} sec')  
        print(f'BST finding with straight alphabet: {round(bst_find_words(lst), 2)} sec')
        print(f'In BST with a shuffled alphabet: {round(random_bst_find(lst), 2)} sec')
        print(f'Finding in balanced tree: {round(check_in_balanced(lst), 2)} sec')


if __name__ == "__main__":
    bst = LinkedBST()
    bst.demo_bst('task2/words.txt')