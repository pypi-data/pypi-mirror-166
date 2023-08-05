from pathlib import Path
from typing import Any, Union


class FileBytes(bytearray):
    path: Path

    def __init__(self, bytesobj: bytes, path: Path):
        self.path = path
        super().__init__(bytesobj)

    def __iadd__(self, other) -> "FileBytes":
        if isinstance(other, str):
            other = other.encode()
        with open(self.path, "wb+") as f:
            f.write(other)
        super().__iadd__(other)
        return self

    def __add__(self, other) -> "FileBytes":
        return FileBytes(bytearray.__add__(self, other), self.path)


class DirDict:
    path: Path

    def __init__(self, path: str | Path = Path(".")):
        self.path = path if isinstance(path, Path) else Path(path)
        if not self.path.exists():
            self.path.mkdir()
        if not self.path.is_dir():
            raise EnvironmentError("DirDict path must be a directory or non-existing")

    def __setitem__(self, name: str, item: str | bytes):
        filepath = self.path / name
        mode = "w" if isinstance(item, str) else "wb"
        with open(filepath, mode) as f:
            f.write(item)

    def __getitem__(self, name: str) -> Union[FileBytes, "DirDict"]:
        filepath = self.path / name
        if filepath.is_dir():
            return DirDict(filepath)
        with open(filepath, "rb") as f:
            return FileBytes(f.read(), path=filepath)

    def __truediv__(self, other: str | Path) -> "DirDict":
        return DirDict(path=self.path / other)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, DirDict):
            return other.path == self.path
        return False

    def keys(self) -> list[str]:
        return [p.name for p in self.path.glob("*")]
