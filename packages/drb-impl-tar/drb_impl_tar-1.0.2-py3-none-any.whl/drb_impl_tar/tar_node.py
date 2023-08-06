import os

import datetime
import enum
from tarfile import ExFileObject, TarInfo, DIRTYPE
from typing import Any, List, Dict, Tuple, Optional

import drb

from drb import DrbNode, AbstractNode
from drb.exceptions import DrbNotImplementationException, DrbException
from drb.path import ParsedPath
from pathlib import Path


class DrbTarAttributeNames(enum.Enum):
    SIZE = 'size'
    """
    The size of the file in bytes.
    """
    DIRECTORY = 'directory'
    """
    A boolean that tell if the file is a directory.
    """
    MODIFIED = 'modified'
    """
    The last modification date of the file with this format:
        [DAY MONTH NUMB HH:MM:SS YEAR].
    """


class DrbTarNode(AbstractNode):
    """
    This node is used to browse the content of a zip container.

    Parameters:
        parent (DrbNode): The zip container.
        tar_info (ZipInfo): Class with attributes describing
                            each file in the ZIP archive.

    """

    def __init__(self, parent: DrbNode, tar_info: TarInfo = None,
                 name=None,
                 dir=False):
        super().__init__()
        self._tar_info = tar_info
        self._attributes: Dict[Tuple[str, str], Any] = None
        self._name = name
        self._parent: DrbNode = parent
        self._children: List[DrbNode] = None
        self._path = None
        self._dir = dir
        if tar_info is not None and tar_info.type == DIRTYPE:
            self._dir = True

    @property
    def parent(self) -> Optional[DrbNode]:
        return self._parent

    @property
    def path(self) -> ParsedPath:
        if self._path is None:
            self._path = self.parent.path / self.name
        return self._path

    def name_entry(self):
        if self._tar_info is not None:
            return self._tar_info.name
        else:
            name_entry = self.parent.name_entry() + self._name
            if self._dir:
                name_entry += os.sep
            return name_entry

    @property
    def name(self) -> str:
        if self._name is None:
            if self._tar_info.name.endswith('/'):
                self._name = self._tar_info.name[:-1]
            else:
                self._name = self._tar_info.name
            if '/' in self._name:
                self._name = self._name[self._name .rindex('/') + 1:]
        return self._name

    @property
    def namespace_uri(self) -> Optional[str]:
        return None

    @property
    def value(self) -> Optional[Any]:
        return None

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        if self._attributes is None:
            self._attributes = {}
            name_attribute = DrbTarAttributeNames.DIRECTORY.value
            self._attributes[name_attribute, None] = self._dir

            if self._tar_info is not None:
                name_attribute = DrbTarAttributeNames.SIZE.value
                self._attributes[name_attribute, None] = self._tar_info.size

                date_time = datetime.datetime.fromtimestamp(
                    self._tar_info.mtime)

                name_attribute = DrbTarAttributeNames.MODIFIED.value
                self._attributes[name_attribute, None] = \
                    date_time.strftime("%c")

        return self._attributes

    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        key = (name, namespace_uri)
        if key in self.attributes.keys():
            return self.attributes[key]
        raise DrbException(f'Attribute not found name: {name}, '
                           f'namespace: {namespace_uri}')

    @staticmethod
    def is_a_subdir(entry) -> bool:
        if os.path.basename(entry.name) is not None and len(
                os.path.basename(entry.name)) > 1:
            return False

        paths_array = Path(entry.name).parts

        if len(paths_array) > 1:
            return False
        return True

    def _add_sub_child(self):

        name = self.name_entry()
        for entry in self.get_members():
            filename = entry.name[len(name):]

            # Chek if this entries is a child or a sub
            # child if yes => not a child
            # of the root
            # if os.path.basename(entry.name) is not None and len(
            #         os.path.basename(entry.name)) > 1:
            #         continue

            if filename.startswith('/'):
                filename = filename[1:]

            paths_array = Path(filename).parts

            if len(paths_array) == 1:
                continue

            name_sub_dir = paths_array[0]

            found = False
            for child in self._children:
                if child.name == name_sub_dir:
                    found = True
            if not found:
                self._children.append(DrbTarNode(self, None,
                                                 name=name_sub_dir, dir=True))

    def get_members(self):
        if not self._dir:
            return []

        members = []

        name = self.name_entry()
        if name.startswith('/'):
            name = name[1:]
        for entry in self.parent.get_members():
            entry_name = entry.name
            if entry_name.startswith('/'):
                entry_name = entry_name[1:]
            if not entry_name.startswith(name):
                continue

            filename = entry_name[len(name):]
            if not filename:
                continue

            members.append(entry)
        return members

    def _is_a_child(self, filename):
        name = self.name_entry()
        filename = filename[len(name):]

        if not filename.startswith('/') and \
                not name.endswith('/'):
            return False

        filename = filename[1:]
        if filename.endswith('/'):
            filename = filename[:-1]

        paths_array = Path(filename).parts

        if len(paths_array) > 1:
            return False

        if os.path.basename(filename) is not None \
                and len(os.path.basename(filename)) > 0:
            return True

        # Either the name do not contains sep either only one a last position
        return '/' not in filename

    @property
    @drb.resolve_children
    def children(self) -> List[DrbNode]:

        if self._children is None:
            self._children = []

            for entry in self.get_members():
                if self._is_a_child(entry.name):
                    self._children.append(DrbTarNode(self, entry))
                elif self.is_a_subdir(entry):
                    self._children.append(DrbTarNode(self,
                                                     None, name=entry.name))

            self._add_sub_child()

            self._children = sorted(self._children,
                                    key=lambda entry_cmp: entry_cmp.name)

        return self._children

    def has_impl(self, impl: type) -> bool:
        if issubclass(ExFileObject, impl):
            return not self.get_attribute(DrbTarAttributeNames.DIRECTORY.value,
                                          None)
        return False

    def get_impl(self, impl: type, **kwargs) -> Any:
        if self.has_impl(impl):
            return self.parent.open_member(self._tar_info)
        raise DrbNotImplementationException(f'no {impl} '
                                            f'implementation found')

    def close(self):
        pass

    def open_member(self, tar_info: TarInfo):
        # open a member to retrieve tje implementation
        # back to first parent that is file tar to open it...
        return self.parent.open_member(tar_info)
