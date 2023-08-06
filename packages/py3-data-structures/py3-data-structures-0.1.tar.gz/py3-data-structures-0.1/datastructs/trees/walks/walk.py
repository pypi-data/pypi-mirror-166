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

from ... import Stack
from copy import copy


class Walk:
    """
    Use stack technique to perform anti-recursive tree traversal.
    ---------
    @author:    Hieu Pham.
    @created:   05.09.2022.
    @updated:   05.09.2022.
    """
    # Use stack to flattens tree structure.
    __stack: Stack = Stack()
    # Store result nodes as a list.
    __nodes: list = list()
    # Axis vector of flatten process.
    __axis: tuple = (0, 0, 0)

    @property
    def nodes(self):
        """
        Get result nodes.
        """
        return copy(self.__nodes)

    def __init__(self, axis: tuple = (0, 0, 0), **kwargs):
        """
        Class constructor.
        :param axis:    axis vector of flatten process.
        :param kwargs:  additional keyword arguments to be passed.
        """
        self.__axis = axis

    def walks(self, begin, **kwargs):
        """
        Perform anti-recursive tree traversal.
        :param begin:   beginning node.
        :param kwargs:  additional keyword arguments to be passed.
        :return:        result nodes.
        """
        # Clean previous data.
        self.__stack.clear()
        self.__nodes.clear()
        # Push first node.
        self.__stack.push(begin)
        # Loop until stack is empty.
        while self.__stack.size > 0:
            # Pop top node from stack.
            node = self.__stack.pop()
            if not self.on_pop(node, **kwargs):
                break
            self.__nodes.append(node)
            # In case axis[0] is 0, going upward.
            if not self.__axis[0]:
                #
                if node.parent is not None and self.on_push(node.parent):
                    self.__stack.push(node.parent)
                #
                else: return self.on_walk(**kwargs)
            # Otherwise, going downward.
            else:
                leafs = node.leafs()
                # Reverse other if axis[1] is 0.
                if not self.__axis[1]:
                    leafs.reverse()
                # Push leafs to stack.
                for leaf in leafs:
                    if self.on_push(leaf): self.__stack.push(leaf)
                    else: return self.on_walk(**kwargs)
        # Reverse other if axis[2] is 0.
        if not self.__axis[2]: self.__nodes.reverse()
        # Return result.
        return self.on_walk(**kwargs)

    def on_walk(self, **kwargs):
        """
        Triggered when flattening is done and walking process begin.
        :param kwargs:  additional keyword arguments to be passed.
        :return:        result nodes.
        """
        for node in self.__nodes:
            if not self.on_visit(node, **kwargs):
                break
        return self.__nodes
    
    def on_push(self, node, **kwargs):
        """
        Triggered when a node is pushed to stack.
        :param node:    node to be pushed.
        :return:        break walk process or not.
        """
        return True

    def on_pop(self, node, **kwargs):
        """
        Triggered when a node is popped to stack.
        :param node:    node to be pushed.
        :return:        break walk process or not.
        """
        return True

    def on_visit(self, node, **kwargs):
        """
        Triggered when a node is visited.
        :param node:    node to be visited.
        :return:        break walk process or not.
        """
        return True
