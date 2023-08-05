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


class AbstractNode(ABC):
    """
    This is class is abstract interface of all inherited nodes.
    ---------
    @author:    Hieu Pham.
    @created:   02.09.2022.
    @updated:   03.09.2022.
    """

    @property
    @abstractmethod
    def idx(self):
        """
        Get index of node.
        """
        raise NotImplemented

    @property
    @abstractmethod
    def root(self):
        """
        Get root node of the tree.
        """
        raise NotImplemented

    @property
    @abstractmethod
    def leafs(self):
        """
        Get leaf nodes as an reference array.
        """
        raise NotImplemented

    @property
    @abstractmethod
    def limit(self):
        """
        Get limit size of leafs
        """
        raise NotImplemented

    @property
    @abstractmethod
    def parent(self):
        """
        Get parent node.
        """
        raise NotImplemented

    @property
    def data(self):
        """
        Get node data as dictionary.
        """
        return dict({'idx': '.'.join([str(i) for i in self.idx])})

    def __init__(self, limit: int = None, **kwargs) -> None:
        """
        Create a new  instance.
        :param limit:   set the limit size of leafs.
        :param kwargs:  additional keyword arguments to be passed.
        """
        super().__init__()

    @abstractmethod
    def attach(self, node, pos: int = -1, **kwargs):
        """
        Attach a node as leaf node.
        :param node:    node to be attached.
        :param pos:     position to attach node.
        :param kwargs:  additional keyword arguments to be passed.
        :return:        node and attached node.
        """
        raise NotImplemented

    @abstractmethod
    def detach(self, index: int, **kwargs):
        """
        Detach a leaf node based on its index.
        :param index:   index of leaf node to be detached.
        :param kwargs:  additional keyword arguments to be passed.
        :return:        node and detached node.
        """
        raise NotImplemented

    @abstractmethod
    def clean(self):
        """
        Clean all leafs.
        :return:    node and leaf nodes as separated tree.
        """
        raise NotImplemented
    