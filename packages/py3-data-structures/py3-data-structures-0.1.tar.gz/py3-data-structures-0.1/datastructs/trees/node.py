# -----------------------------------------------------------------------------
# MIT License
#
# Copyright (c) 2022 Hieu Pham. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# -----------------------------------------------------------------------------

from copy import copy
from threading import Lock
from abc import ABC, abstractmethod


class AbstractNode(ABC):
    """
    This class is abstract interface of all inherited tree nodes.
    ---------
    @author:    Hieu Pham.
    @created:   04.09.2022.
    @updated:   05.09.2022.
    """
    @property
    @abstractmethod
    def parent(self):
        """
        Get parent node of current node.
        """
        raise NotImplemented

    @property
    @abstractmethod
    def leafs(self):
        """
        Get all leaf nodes of current node.
        """
        raise NotImplemented

    @property
    @abstractmethod
    def capacity(self):
        """
        Get leafs capacity of current node. 
        """
        raise NotImplemented
    
    @property
    @abstractmethod
    def root(self):
        """
        Get root node of current tree.
        """
        raise NotImplemented

    @property
    @abstractmethod
    def data(self):
        """
        Get data of current node.
        """
        raise NotImplemented

    @data.setter
    @abstractmethod
    def data(self, data):
        """
        Set data of current node.
        """
        raise NotImplemented


class Node(AbstractNode):
    """
    This is thread-safe implementation of basic tree node.
    ---------
    @author:    Hieu Pham
    @created:   05.09.2022.
    @updated:   05.09.2022.
    """
    # Locking for thread-safe purpose.
    __lock = Lock()
    # Reference to parent node.
    __parent = None
    # Array of references to leaf nodes.
    __leafs = None
    # Capacity of leafs array.
    __capacity = None
    # Reference to data of node.
    __data = None
    # Reference to root of current tree.
    __root = None
    # Depth level of current node on tree.
    __level = 0

    @property
    def parent(self):
        """
        Get parent node of current node.
        """
        return self.__parent

    @property
    def leafs(self):
        """
        Get all leaf nodes of current node.
        """
        return copy(self.__leafs)

    @property
    def capacity(self):
        """
        Get leafs capacity of current node. 
        """
        return self.__capacity

    @property
    def data(self):
        """
        Get data of current node.
        """
        return self.__data

    @data.setter
    def data(self, data):
        """
        Set data of current node.
        :param data:    desired data.
        """
        self.__data = data

    @property
    def root(self):
        """
        Get root node of current tree.
        """
        return self.__root

    @property
    def level(self):
        """
        Get level of current node.
        """
        return self.__level

    def __init__(self, capacity: int = None, **kwargs):
        """
        Class constructor.
        :param capacity:    capacity of leafs array.
        :param udm:         undermost walk of node.
        :param kwargs:      additional keyword arguments to be passed.
        """
        self.__root = self
        self.__capacity = capacity
        self.__leafs = [] if capacity is None else [None] * capacity

    def __on_attach(self, parent, node, pos):
        """
        Trigger when leaf node is attached successfully.
        :param parent:  parent node.
        :param node:    node to be attached.
        :param pos:     position to be attached.
        """
        parent.__leafs[pos] = node
        node.__parent = parent
        node.__root = parent.root
        node.__level = parent.level + 1

    def attach(self, node, pos: int = 0, bottommost: bool = False, lock: bool = True, **kwargs):
        """
        Attach a node as leaf node.
        :param node:        node to be attached.
        :param pos:         position to be attached.
        :param bottommost:  attach to bottommost leaf or not.
        :param lock:        lock for thread-safe or not.
        :param kwargs:      additional keyword arguments to be passed.
        :return:            none.
        """
        # Lock for thread-safe.
        if lock:
            self.__lock.acquire()
        # In case of capacity is unlimited, attach node to head or tail based on position.
        if self.capacity is None:
            self.__leafs.append(node) if pos > 0 else self.__leafs.insert(0)
        # Otherwise.
        elif pos < self.capacity:
            parent = self
            # If the leaf at desired position is not filled yet then we can attach the node.
            if parent.__leafs[pos] is None:
                self.__on_attach(parent, node, pos)
            # If the leaf at desired position is filled, node will be attach to bottommost 
            # leaf at the same position if bottommost is true.
            elif bottommost:
                while parent.__leafs[pos] is not None:
                    parent = parent.__leafs[pos if parent.capacity > 1 else 0]
                self.__on_attach(parent, node, pos)
            # Otherwise, release thread-lock and raise index error.
            else:
                if self.__lock.locked: self.__lock.release()
                raise IndexError()
        # Release thread-lock.
        if self.__lock.locked: self.__lock.release()
