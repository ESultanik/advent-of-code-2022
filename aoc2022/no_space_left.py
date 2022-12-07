from abc import ABC, abstractmethod
import re
from typing import Dict, List, Iterator, Optional, Sequence, Tuple

from . import challenge, Path

"""
--- Day 7: No Space Left On Device ---
You can hear birds chirping and raindrops hitting leaves as the expedition proceeds. Occasionally, you can even hear much louder sounds in the distance; how big do the animals get out here, anyway?

The device the Elves gave you has problems with more than just its communication system. You try to run a system update:

$ system-update --please --pretty-please-with-sugar-on-top
Error: No space left on device
Perhaps you can delete some files to make space for the update?

You browse around the filesystem to assess the situation and save the resulting terminal output (your puzzle input). For example:

$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
The filesystem consists of a tree of files (plain data) and directories (which can contain other directories or files). The outermost directory is called /. You can navigate around the filesystem, moving into or out of directories and listing the contents of the directory you're currently in.

Within the terminal output, lines that begin with $ are commands you executed, very much like some modern computers:

cd means change directory. This changes which directory is the current directory, but the specific result depends on the argument:
cd x moves in one level: it looks in the current directory for the directory named x and makes it the current directory.
cd .. moves out one level: it finds the directory that contains the current directory, then makes that directory the current directory.
cd / switches the current directory to the outermost directory, /.
ls means list. It prints out all of the files and directories immediately contained by the current directory:
123 abc means that the current directory contains a file named abc with size 123.
dir xyz means that the current directory contains a directory named xyz.
Given the commands and output in the example above, you can determine that the filesystem looks visually like this:

- / (dir)
  - a (dir)
    - e (dir)
      - i (file, size=584)
    - f (file, size=29116)
    - g (file, size=2557)
    - h.lst (file, size=62596)
  - b.txt (file, size=14848514)
  - c.dat (file, size=8504156)
  - d (dir)
    - j (file, size=4060174)
    - d.log (file, size=8033020)
    - d.ext (file, size=5626152)
    - k (file, size=7214296)
Here, there are four directories: / (the outermost directory), a and d (which are in /), and e (which is in a). These directories also contain files of various sizes.

Since the disk is full, your first step should probably be to find directories that are good candidates for deletion. To do this, you need to determine the total size of each directory. The total size of a directory is the sum of the sizes of the files it contains, directly or indirectly. (Directories themselves do not count as having any intrinsic size.)

The total sizes of the directories above can be found as follows:

The total size of directory e is 584 because it contains a single file i of size 584 and no other directories.
The directory a has total size 94853 because it contains files f (size 29116), g (size 2557), and h.lst (size 62596), plus file i indirectly (a contains e which contains i).
Directory d has total size 24933642.
As the outermost directory, / contains every file. Its total size is 48381165, the sum of the size of every file.
To begin, find all of the directories with a total size of at most 100000, then calculate the sum of their total sizes. In the example above, these directories are a and e; the sum of their total sizes is 95437 (94853 + 584). (As in this example, this process can count files more than once!)

Find all of the directories with a total size of at most 100000. What is the sum of the total sizes of those directories?
"""


class FileSystemElement:
    @property
    @abstractmethod
    def size(self) -> int:
        raise NotImplementedError()


class File(FileSystemElement):
    def __init__(self, size: int):
        self._size: int = size

    @property
    def size(self) -> int:
        return self._size

    def __eq__(self, other):
        return isinstance(other, File) and other._size == self._size

    def __hash__(self):
        return self._size


class Directory(FileSystemElement):
    def __init__(self, parent: Optional["Directory"] = None):
        self.parent: Optional[Directory] = parent
        self._children: Dict[str, FileSystemElement] = {}

    def __eq__(self, other):
        return isinstance(other, Directory) and self._children == other._children and self.parent == other.parent

    def __contains__(self, item):
        if isinstance(item, str):
            return item in self._children
        elif isinstance(item, FileSystemElement):
            return item in self._children.values()
        else:
            return False

    def __getitem__(self, name: str) -> FileSystemElement:
        return self._children[name]

    def walk(self) -> Iterator[FileSystemElement]:
        stack: List[Directory] = [self]
        while stack:
            d = stack.pop()
            for element in d._children.values():
                yield element
                if isinstance(element, Directory):
                    stack.append(element)

    @property
    def root(self) -> "Directory":
        d = self
        while d.parent is not None:
            d = d.parent
        return d

    @property
    def size(self) -> int:
        stack: List[FileSystemElement] = list(self._children.values())
        total = 0
        while stack:
            element = stack.pop()
            if isinstance(element, Directory):
                stack.extend(element._children.values())
            else:
                total += element.size
        return total

    def add(self, name: str, element: FileSystemElement):
        if name in self._children:
            if self._children[name] == element:
                return
            raise ValueError(f"{self._children[name]!r} already exists")
        self._children[name] = element


CMD_PATTERN: re.Pattern = re.compile(r"^\s*\$\s*(\S+)(\s+(.*))?$")


class Command(ABC):
    def __init__(self, args: Optional[str] = None, output: Sequence[str] = ()):
        if args is None:
            args = ""
        self.args: str = args.strip()
        self.output: Tuple[str, ...] = tuple(output)

    @abstractmethod
    def run(self, cwd: Directory) -> Directory:
        raise NotImplementedError()

    @staticmethod
    def parse(line: str, output: Sequence[str] = ()) -> "Command":
        m = CMD_PATTERN.match(line)
        if not m:
            raise ValueError(line)
        cmd = m.group(1)
        args = m.group(3)
        if cmd == "cd":
            return Cd(args, output)
        elif cmd == "ls":
            return Ls(args, output)
        else:
            raise ValueError(f"Unknown command: {line!r}")


class Cd(Command):
    def run(self, cwd: Directory) -> Directory:
        if self.output:
            raise NotImplementedError(repr(self.output))
        elif not self.args:
            raise NotImplementedError("$ cd")
        elif self.args == "..":
            if cwd.parent is None:
                raise ValueError("Cannot `$cd ..` from the root directory!")
            return cwd.parent
        elif self.args.startswith("/"):
            d = cwd.root
            remaining_path = self.args[1:]
            while remaining_path:
                next_separator = remaining_path.find("/")
                if next_separator == 0:
                    raise ValueError(self.args)
                elif next_separator < 0:
                    next_dir = remaining_path
                    remaining_path = ""
                else:
                    next_dir = remaining_path[:next_separator]
                    remaining_path = remaining_path[next_separator+1:]
                if next_dir not in d:
                    raise ValueError(self.args)
                nd = d[next_dir]
                if not isinstance(nd, Directory):
                    raise ValueError(self.args)
                d = nd
            return d
        else:
            if self.args not in cwd:
                raise ValueError(f"Invalid directory: {self.args!r}")
            d = cwd[self.args]
            if not isinstance(d, Directory):
                raise ValueError(f"{self.args!r} is not a directory, it is {d!r}")
            return d

    def __str__(self):
        return f"$ cd {self.args}"


class Ls(Command):
    def run(self, cwd: Directory) -> Directory:
        if self.args:
            raise NotImplementedError(self.args)
        for element in self.output:
            if element.startswith("dir "):
                dirname = element[4:].strip()
                if dirname not in cwd:
                    cwd.add(dirname, Directory(parent=cwd))
            else:
                first_space = element.find(" ")
                if first_space < 0:
                    raise ValueError(f"Invalid output: {element!r}")
                filesize = int(element[:first_space])
                filename = element[first_space+1:].strip()
                if not filename:
                    raise ValueError(f"Invalid filename: {element!r}")
                if filename in cwd:
                    obj = cwd[filename]
                    if not isinstance(filename, File):
                        raise ValueError(f"{self!s} returned {element!r}, but {filename} is already a directory in "
                                         f"{cwd}")
                    elif obj.size != filesize:
                        raise ValueError(f"{self!s} returned {element!r} but {filename} was already reported as size "
                                         f"{obj.size}")
                else:
                    cwd.add(filename, File(filesize))
        return cwd

    def __str__(self):
        return f"$ ls {self.args}"


def parse_commands(path: Path) -> Iterator[Command]:
    with open(path, "r") as f:
        cmd_line: str = ""
        output_lines: List[str] = []
        for line in f:
            line = line.strip()
            if line.startswith("$"):
                if cmd_line:
                    yield Command.parse(cmd_line, output_lines)
                    output_lines = []
                cmd_line = line
            else:
                if not cmd_line:
                    raise ValueError(f"Unexpected output line: {line!r}")
                output_lines.append(line)
        if cmd_line:
            yield Command.parse(cmd_line, output_lines)

@challenge(day=7)
def directory_sizes(path: Path) -> int:
    root = Directory()
    cwd = root
    for cmd in parse_commands(path):
        cwd = cmd.run(cwd)
    return sum(
        e.size
        for e in root.walk()
        if isinstance(e, Directory) and e.size <= 100000
    )


"""
--- Part Two ---
Now, you're ready to choose a directory to delete.

The total disk space available to the filesystem is 70000000. To run the update, you need unused space of at least 30000000. You need to find a directory you can delete that will free up enough space to run the update.

In the example above, the total size of the outermost directory (and thus the total amount of used space) is 48381165; this means that the size of the unused space must currently be 21618835, which isn't quite the 30000000 required by the update. Therefore, the update still requires a directory with total size of at least 8381165 to be deleted before it can run.

To achieve this, you have the following options:

Delete directory e, which would increase unused space by 584.
Delete directory a, which would increase unused space by 94853.
Delete directory d, which would increase unused space by 24933642.
Delete directory /, which would increase unused space by 48381165.
Directories e and a are both too small; deleting them would not free up enough space. However, directories d and / are both big enough! Between these, choose the smallest: d, increasing unused space by 24933642.

Find the smallest directory that, if deleted, would free up enough space on the filesystem to run the update. What is the total size of that directory?
"""

@challenge(day=7)
def dir_to_delete(path: Path):
    root = Directory()
    cwd = root
    for cmd in parse_commands(path):
        cwd = cmd.run(cwd)
    total_space = 70000000
    space_needed = 30000000
    free_space = total_space - root.size
    assert free_space <= space_needed
    space_to_free = space_needed - free_space
    return min(
        e.size
        for e in root.walk()
        if isinstance(e, Directory) and e.size >= space_to_free
    )
