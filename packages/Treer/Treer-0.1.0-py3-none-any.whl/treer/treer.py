import re
from pathlib import Path
from typing import Union, Optional, AnyStr, List, Mapping
import iro
from abc import ABC, abstractmethod


def find_path(path: Union[Path, AnyStr]) -> Path:
    if isinstance(path, str):
        path = Path(path)
    if not path.exists():
        found = None
        for p in path.parents:
            if p.exists():
                found = p
                break
        error_message = f"Path '{path.absolute()}' is not found."
        if found:
            error_message += f"\nThe closest path found is '{found.absolute()}'."
        raise FileNotFoundError(error_message)
    return path


DEFAULT_FILE_STYLE = (iro.Color.GREEN,)
DEFAULT_SYMLINK_STYLE = (iro.Color.BRIGHT_RED,)
DEFAULT_DIRECTORY_STYLE = (iro.Color.CYAN, iro.Style.BOLD)
DEFAULT_BRANCH_STYLE = (iro.Color.WHITE,)


class Tree(ABC):
    def __init__(self, children: List['Tree'], parent: Optional['Tree'] = None):
        self.children = children
        self.parent = parent

        self.colorize = True

        self.file_style = DEFAULT_FILE_STYLE
        self.symlink_style = DEFAULT_SYMLINK_STYLE
        self.directory_style = DEFAULT_DIRECTORY_STYLE
        self.branch_style = DEFAULT_BRANCH_STYLE

    @abstractmethod
    def default_name_factory(self) -> str:
        ...

    @property
    def name(self) -> str:
        return self.default_name_factory()

    @staticmethod
    def from_path(path: Optional[Union[Path, AnyStr]] = None,
                  exclude: List[Union[re.Pattern, Path, str]] = None) -> 'DirTree':
        return DirTree.from_path(path, exclude)

    @staticmethod
    def from_mapping(mapping: Mapping, exclude: List[Union[re.Pattern, Path, str]] = None) -> 'MapTree':
        return MapTree.from_mapping(mapping, exclude)

    def draw(self) -> str:
        if self.children:
            return f'{self.draw_self()}\n{self.draw_children()}'
        return self.draw_self()

    def draw_self(self) -> str:
        return self.line() + self.name

    def draw_children(self) -> str:
        return '\n'.join(child.draw() for child in self.children)

    def line(self) -> str:
        self_line = ''
        if self.parent:
            self_line = ' └── ' if self.is_last_sibling() else ' ├── '
        if self.root.colorize:
            return iro.Iro((*self.root.branch_style, self.parent_line() + self_line)).text
        return self.parent_line() + self_line

    def parent_line(self) -> str:
        if self.parent is None or self.parent.parent is None:
            return ''
        if self.parent.is_last_sibling():
            return self.parent.parent_line() + '     '
        return self.parent.parent_line() + ' │   '

    def is_last_sibling(self) -> bool:
        if not self.parent:
            return True
        return self.parent.children[-1] == self

    @property
    def root(self) -> 'Tree':
        if self.parent is None:
            return self
        return self.parent.root


class DirTree(Tree):
    def __init__(self, path: Path, children: List['DirTree'], parent: Optional['DirTree'] = None):
        self.path = path
        super().__init__(children, parent)

    @staticmethod
    def from_path(path: Optional[Union[Path, AnyStr]] = None,
                  exclude: List[Union[re.Pattern, Path, str]] = None) -> 'DirTree':
        if exclude is None:
            exclude = []
        if path:
            path = find_path(path).resolve()
        else:
            path = Path.cwd()
        root = DirTree(path, [], None)
        root.dig_path(exclude)
        return root

    def dig_path(self, exclude: Optional[List[Union[re.Pattern, Path, str]]]):
        self.children = []
        for p in sorted(self.path.iterdir()):
            break_flag = False
            for ex in exclude:
                if isinstance(ex, re.Pattern) and ex.search(str(p)):
                    break_flag = True
                elif isinstance(ex, Path) and p == ex:
                    break_flag = True
                elif isinstance(ex, str) and ex in str(p):
                    break_flag = True
            if break_flag:
                continue
            child = DirTree(p, [], self)
            if p.is_dir():
                child.dig_path(exclude)
            self.children.append(child)

    def colorizer(self, text: str) -> str:
        if not self.root.colorize:
            return text

        if self.path.is_dir():
            return iro.Iro((*self.root.directory_style, text)).text
        if self.path.is_symlink():
            return iro.Iro((*self.root.symlink_style, text)).text
        return iro.Iro((*self.root.file_style, text)).text

    def default_name_factory(self) -> str:
        if self.path.is_symlink():
            return self.colorizer('*' + self.path.name)
        return self.colorizer(self.path.name)


class MapTree(Tree):
    def __init__(self, identifier: str, children: List['MapTree'], parent: Optional['MapTree'] = None):
        self.identifier = identifier
        super().__init__(children, parent)

    @staticmethod
    def from_mapping(mapping: Mapping, exclude: List[Union[re.Pattern, Path, str]] = None) -> 'MapTree':
        if exclude is None:
            exclude = []
        if len(mapping.keys()) != 1:
            raise ValueError("Mapping must have exactly one key but found {len(mapping.keys())}.")
        root_identifier = list(mapping.keys())[0]
        root = MapTree(root_identifier, [], None)
        root.dig_mapping(mapping[root_identifier], exclude)
        return root

    def dig_mapping(self, mapping: Mapping, exclude: Optional[List[Union[re.Pattern, str]]]):
        self.children = []
        if isinstance(mapping, Mapping):
            for k, v in mapping.items():
                break_flag = False
                for ex in exclude:
                    if isinstance(ex, re.Pattern) and ex.search(str(k)):
                        break_flag = True
                    elif isinstance(ex, str) and ex in str(k):
                        break_flag = True
                if break_flag:
                    continue
                child = MapTree(k, [], self)
                if v:
                    child.dig_mapping(v, exclude)
                self.children.append(child)
        elif isinstance(mapping, str):
            self.children.append(MapTree(mapping, [], self))
        elif isinstance(mapping, (list, tuple)):
            for v in mapping:
                child = MapTree(v, [], self)
                self.children.append(child)

    def default_name_factory(self) -> str:
        return self.colorizer(self.identifier)

    def colorizer(self, text: str) -> str:
        if not self.root.colorize:
            return text

        if self.children:
            return iro.Iro((*self.root.directory_style, text)).text
        return iro.Iro((*self.root.file_style, text)).text
