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
from . import AbstractNode
from ..walks import ReindexWalk


class Node(AbstractNode):
    """
    This class is base class of all inherited nodes.
    ---------
    @author:    Hieu Pham.
    @created:   02.09.2022.
    @updated:   03.09.2022.
    """
    # Store index of node.
    _idx = None
    # Root of the tree.
    _root = None
    # Leaf nodes of node.
    _leafs = None
    # Max size of leafs.
    _limit = None
    # Parent node of node.
    _parent = None

    @property
    def idx(self):
        """
        Get index of node.
        """
        return copy(self._idx)

    @property
    def root(self):
        """
        Get root node of the tree.
        """
        return self._root

    @property
    def leafs(self):
        """
        Get leaf nodes as an reference array.
        """
        return copy(self._leafs)

    @property
    def limit(self):
        """
        Get limit size of leafs
        """
        return self._limit

    @property
    def parent(self):
        """
        Get parent node.
        """
        return self._parent

    def __init__(self, limit: int = None, **kwargs) -> None:
        """
        Create a new  instance.
        :param limit:   set the limit size of leafs.
        :param kwargs:  additional keyword arguments to be passed.
        """
        super().__init__()
        # Initialize
        self._idx = [0]
        self._root = self
        self._limit = limit
        self._leafs = [] if self._limit is None else [None] * self._limit

    def attach(self, node, pos: int = -1, **kwargs):
        """
        Attach a node as leaf node.
        :param node:    node to be attached.
        :param pos:     position to attach node.
        :param kwargs:  additional keyword arguments to be passed.
        :return:        node and attached node.
        """
        # Attach node.
        if self._limit is None:
            self._leafs.insert(pos, node) if pos == 0 else self._leafs.append(node)
        else:
            if pos > self._limit - 1 or self._leafs[pos] is not None:
                raise IndexError
            else:
                self._leafs[pos] = node
        # Set up leaf node.
        node._parent = self
        node._root = self._root
        # re-index leafs using walk.
        walk = ReindexWalk()
        walk.walks(self)
        # Return result.
        return self, node

    def detach(self, index: int, **kwargs):
        """
        Detach a leaf node based on its index.
        :param index:   index of leaf node to be detached.
        :param kwargs:  additional keyword arguments to be passed.
        :return:        node and detached node.
        """
        # Pop node from leafs.
        node = self._leafs.pop(index)
        node._idx = [0]
        node._root = node
        node._parent = None
        # Re-index current and popped nodes.
        walk = ReindexWalk()
        walk.walks(self)
        walk.walks(node)
        # Return result.
        return self, node

    def clean(self):
        """
        Clean all leafs.
        :return:    node and leaf nodes as separated tree.
        """
        nodes = [self.detach(i)[-1] for i in range(0, len(self._leafs))]
        return self, nodes

    def goto(self, idx, **kwargs):
        """
        Go to the node based on its idx.
        :param idx:     idx of desired node.
        :param kwargs:  additional keyword arguments to be passed.
        :return:        desired node.
        """
        node = self._root
        _idx = copy(idx)
        _idx.pop(0)
        for i in range(0, len(_idx)):
            node = node._leafs[_idx[i]]
        return node
