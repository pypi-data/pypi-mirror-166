

from . import AbstractWalk


class ToDataWalk(AbstractWalk):

    _data = None

    def __init__(self, **kwargs) -> None:
        """
        Create new object instance.
        :param kwargs:  additional keyword arguments to be passed.
        """
        super().__init__(flatten=(1, 1, 1, 0), **kwargs)
        self._data = list()

    def _visit(self, node, **kwargs) -> bool:
        self._data.append(node.data)
        return True

    def walks(self, node, **kwargs):
        super().walks(node, **kwargs)