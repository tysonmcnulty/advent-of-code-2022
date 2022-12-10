import re
from dataclasses import dataclass
from itertools import chain
from typing import Callable, Iterator, Self, TypedDict


class DirectoryArgData(TypedDict):
    name: str
    directory_lines: list[str]
    files_lines: list[str]


def parse(data: list[str]):
    data_iter = iter(data)
    root_dir_name = re.match(r"\$ cd (.+)", next(data_iter).strip()).group(1)

    return Directory.from_data(root_dir_name, data_iter)


@dataclass(frozen=True)
class File:
    name: str
    size: int


@dataclass(frozen=True)
class Directory:
    name: str
    directories: frozenset[Self]
    files: frozenset[File]

    @property
    def size(self) -> int:
        return sum(f.size for f in self.files) + sum(d.size for d in self.directories)

    @staticmethod
    def from_data(name: str, data_iter: Iterator[str]) -> Self:
        directories = []
        files = []
        for datum in data_iter:
            line = datum.strip()
            if re.match(r"\$ ls", line):
                continue
            elif re.match("dir", line):
                continue
            elif match := re.match(r"(\d+) (.+)", line):
                file_name, file_size = match.group(2, 1)
                files.append(File(file_name, int(file_size)))
                continue
            elif match := re.match(r"\$ cd (.+)", line):
                dir_name = match.group(1)
                if dir_name == "..":
                    break
                else:
                    directories.append(Directory.from_data(dir_name, data_iter))
                    continue

        directory = Directory(name, frozenset(directories), frozenset(files))
        return directory


def find_directories(
    directory: Directory, condition: Callable[[Directory], bool] = lambda d: True
) -> Iterator[Directory]:

    return chain(
        filter(condition, [directory]),
        *(find_directories(subdir, condition) for subdir in directory.directories),
    )
