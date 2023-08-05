import shutil
import gzip
from pathlib import Path
import re
from typing import Optional, cast, Iterator


def _gunzip(src_file: str, dst_dir: str) -> None:
    src_file_path = Path(src_file)
    dst_dir_path = Path(dst_dir)
    dst_file_path = dst_dir_path / src_file_path.stem
    with gzip.open(src_file_path, "rb") as fsrc:
        with open(dst_file_path, "wb") as fdst:
            shutil.copyfileobj(fsrc, fdst)


def enable_gzip() -> None:
    registered_exts = [
        ext for _, exts, _ in shutil.get_unpack_formats() for ext in exts
    ]
    if ".gz" not in registered_exts:
        shutil.register_unpack_format("gunzip", [".gz"], _gunzip)


class SSHConfigEntry:
    def __init__(self):
        self._entry: dict[str, str] = {}

    def __setitem__(self, key: str, value: str) -> None:
        if key in self._entry:
            raise KeyError(f"Entry for {key} already exists!")
        self._entry[key] = value

    def __getitem__(self, key: str) -> str:
        return self._entry[key]

    def __contains__(self, key: str) -> bool:
        return key in self._entry

    def items(self) -> Iterator[tuple[str, str]]:
        for k, v in self._entry.items():
            yield k, v

    def __repr__(self):
        ser = ""
        for key, val in self._entry.items():
            ser += f"  {key} {val}\n"
        return ser


class SSHConfig:
    def __init__(self) -> None:
        self._hosts: dict[str, SSHConfigEntry] = {}
        self._matches: dict[str, SSHConfigEntry] = {}

    def _add(
        self, hsh: dict[str, SSHConfigEntry], alias: str, entry: SSHConfigEntry
    ) -> None:
        if alias in hsh:
            raise KeyError(f"{alias} already has an entry!")
        hsh[alias] = entry

    def _remove(self, hsh: dict[str, SSHConfigEntry], alias: str) -> None:
        if alias not in hsh:
            raise KeyError(f"Entry for {alias} does not exist!")
        del hsh[alias]

    def add_host(self, alias: str, entry: SSHConfigEntry) -> None:
        self._add(self._hosts, alias, entry)

    def add_match(self, alias: str, entry: SSHConfigEntry) -> None:
        self._add(self._matches, alias, entry)

    def remove_host(self, alias: str) -> None:
        self._remove(self._hosts, alias)

    def remove_match(self, alias: str) -> None:
        self._remove(self._matches, alias)

    def contains_host(self, alias: str) -> bool:
        return alias in self._hosts

    def contains_match(self, alias: str) -> bool:
        return alias in self._matches

    @classmethod
    def read(cls, filepath: Path) -> "SSHConfig":
        config = cls()
        entry: Optional[SSHConfigEntry] = None
        with filepath.open("rt") as f:
            for line in f:
                line = line.rstrip()
                if not line:
                    continue
                elif line.startswith("#"):
                    continue
                elif line.startswith("Host "):
                    entry = SSHConfigEntry()
                    alias = line.split("Host")[1].strip()
                    config._hosts[alias] = entry
                elif line.startswith("Match "):
                    entry = SSHConfigEntry()
                    alias = line.split("Match")[1].strip()
                    config._matches[alias] = entry
                elif line.startswith(" "):
                    match = re.search(r"\s+(\w+)\s+([^\s]+)", line)
                    if match is not None:
                        key, value = match.group(1), match.group(2)
                        entry = cast(SSHConfigEntry, entry)
                        entry[key] = value
                    else:
                        raise RuntimeError(f"{line} is badly formatted!")
        return config

    def write(self, filepath: Path) -> None:
        if filepath.exists():
            backup_filepath = filepath.with_suffix(f"{filepath.suffix}.bak")
            shutil.copyfile(filepath, backup_filepath)
            filepath.unlink()
        with filepath.open("wt") as f:
            for host, entry in self._hosts.items():
                print(f"Host {host}", file=f)
                for key, value in entry.items():
                    print(f"  {key} {value}", file=f)
                print("\n", file=f)

            for match, entry in self._matches.items():
                print(f"Match {match}", file=f)
                for key, value in entry.items():
                    print(f"  {key} {value}", file=f)
                print("\n", file=f)


if __name__ == "__main__":
    fn = Path.home() / "temp" / "ssh_config"
    config = SSHConfig.read(fn)
    print(config._hosts)
    print(config._matches)
