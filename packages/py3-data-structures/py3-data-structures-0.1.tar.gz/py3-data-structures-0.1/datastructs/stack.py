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
from typing import Any, Union


class Stack:
    """
    This is the thread-safe implementation of stack.
    ---------
    @author:    Hieu Pham.
    @created:   04.09.2022.
    @updated:   05.09.2022.
    """

    # Locking will be acquired in data writing.
    __lock = Lock()
    # Store data in a list.
    __data = list()

    @property
    def data(self):
        """
        Get a copy of stack data.
        """
        return copy(self.__data)

    @property
    def size(self):
        """
        Get size of stack data.
        """
        return len(self.__data)

    def push(self, item, lock: bool = True, **kwargs):
        """
        Push a item into stack.
        :param item:    item to be pushed.
        :param lock:    lock for thread-safe or not.
        :param kwargs:  additional keyword arguments to be passed.
        :return:        none.
        """
        # Lock for thread-safe.
        if lock:
            self.__lock.acquire()
        # Push item into stack data list.
        self.__data.append(item)
        # Unlock thread.
        if self.__lock.locked():
            self.__lock.release()

    def pop(self, lock: bool = True, **kwargs) -> Union[Any, None]:
        """
        Pop the top item out from stack.
        :param lock:    lock for thread-safe or not.
        :param kwargs:  additional keyword arguments to be passed.
        :return:        top item or none.
        """
        # Lock for thread-safe.
        if lock:
            self.__lock.acquire()
        # Pop item out from stack.
        item = self.__data.pop() if len(self.__data) > 0 else None
        # Unlock thread.
        if self.__lock.locked():
            self.__lock.release()
        # Return popped item.
        return item

    def peek(self, index: int = None, **kwargs):
        """
        Peek an item from stack.
        :param index:   index of item to be peeked.
        :param kwargs:  additional keyword arguments to be passed.
        :return:        peeked item.
        """
        return self.__data[-1] if index is None else self.__data[index]

    def clear(self, **kwargs):
        """
        Clear all data in stack.
        :param kwargs:  additional keyword arguments to be passed.
        :return:        none.
        """
        self.__data.clear()
