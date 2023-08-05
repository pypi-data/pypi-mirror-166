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

from . import AbstractWalk


class DataWalk(AbstractWalk):
    """
    This walk is used to serialize tree to flattened data array.
    ---------
    @author:    Hieu Pham.
    @created:   03.09.2022.
    @updated:   03.09.2022.
    """
    # Store data array of flattened tree.
    _data = None

    def __init__(self, **kwargs) -> None:
        """
        Create new object instance.
        :param kwargs:  additional keyword arguments to be passed.
        """
        super().__init__(flatten=(1, 1, 0, 0), **kwargs)
        self._data = list()

    def _visit(self, node, **kwargs) -> bool:
        """
        This function is triggered when a node is visited.
        :param node:    node to be visited.
        :param kwargs:  additional keyword arguments to be passed.
        :return:        boolean to break the current walking process or not.
        """
        self._data.append(node.data)
        return True

    def walks(self, node, **kwargs):
        """
        Perform tree walks.
        :param node:    beginning node.
        :param kwargs:  additional keyword arguments.
        :return:        none.        
        """
        super().walks(node, **kwargs)
        return self._data
