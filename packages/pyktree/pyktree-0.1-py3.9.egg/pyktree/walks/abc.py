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

from abc import ABC, abstractmethod


class AbstractWalk(ABC):
    """
    This class use queue technique to perform tree traversal without recursion.
    ---------
    @author:    Hieu Pham.
    @created:   03.09.2022.
    @updated:   03.09.2022.
    """
    # Queue is a list which is used to flattens the tree.
    _queue = None
    # The binary vector define how tree will be flatten into queue.
    _flatten = None

    def __init__(self, flatten: tuple = (1, 1, 1, 1), **kwargs) -> None:
        """
        Class constructor.
        :param flatten:     binary vector to define how tree will be flatten.
        :param kwargs:      additional keyword arguments to be passed.
        """
        self._queue = list()
        self._flatten = flatten

    @abstractmethod
    def _visit(self, node, **kwargs) -> bool:
        """
        This function is triggered when a node is visited.
        :param node:    node to be visited.
        :param kwargs:  additional keyword arguments to be passed.
        :return:        boolean to break the current walking process or not.
        """
        raise NotImplemented

    def _append(self, node, **kwargs) -> None:
        """
        Append node into queue.
        :param node:    node to be appended.
        :param kwargs:  additional keyword arguments to be passed.
        :return:        none.
        """
        if self._flatten[0]:
            self._queue.append([node, [n for n in node.leafs if n is not None]])
        else:
            self._queue.append([node, [] if node.parent is None else [node.parent]])

    def _flattens(self, **kwargs) -> None:
        """
        Flatten tree into queue.
        :param kwargs:  additional keyword arguments to be passed.
        :return:        none
        """
        index, leafs = 0, self._queue[-1][-1]
        # In case of singular flatten style.
        if self._flatten[1]:
            while(True):
                # In case there are leafs.
                if len(leafs) > 0:
                    self._append(leafs.pop() if self._flatten[2] else leafs.pop(0))
                    index, leafs = len(self._queue) - 1, self._queue[-1][-1]
                # Step back.
                elif index > 0:
                    index = index - 1
                    leafs = self._queue[index][-1]
                else:
                    break
        # Otherwise do bulk flatten style.
        else:
            while True:
                # In case there are leafs.
                if len(leafs) > 0:
                    for i in range(0, len(leafs)):
                        self._append(leafs.pop() if self._flatten[2] else leafs.pop(0))
                # Step forward.
                index += 1
                # In case there are still left in queue.
                if index < len(self._queue):
                    leafs = self._queue[index][-1]
                # Otherwise, break the process.
                else:
                    break

    def _walks(self, **kwargs) -> None:
        """
        Perform tree walks after flattening.
        :param kwargs:  additional keyword arguments to be passed.
        :return:        none.
        """
        for i in range(0, len(self._queue)):
            node = self._queue.pop() if self._flatten[3] else self._queue.pop(0)
            if not self._visit(node[0], **kwargs):
                break

    def walks(self, node, **kwargs):
        """
        Perform tree walks.
        :param node:    beginning node.
        :param kwargs:  additional keyword arguments.
        :return:        none.        
        """
        self._append(node, **kwargs)
        self._flattens()
        self._walks()
