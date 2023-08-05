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
from . import AbstractWalk

class ReindexWalk(AbstractWalk):
    """
    This walk is used to re-index nodes of tree.
    ---------
    @author:    Hieu Pham.
    @created:   02.09.2022.
    @updated:   03.09.2022.    
    """

    def __init__(self, **kwargs) -> None:
        """
        Create new object instance.
        :param kwargs:  additional keyword arguments to be passed.
        """
        super().__init__(flatten=(1, 1, 1, 0), **kwargs)

    def _visit(self, node, **kwargs) -> bool:
        """
        Triggered when a node is visited. Change index of all leafs.
        :param node:    node to be visited.
        :param kwargs:  additional keyword arguments to be passed.
        :return:        none.
        """
        for k, v in enumerate(node._leafs):
            if v is not None:
                v._idx = copy(node._idx)
                v._idx.append(k)
        return True
