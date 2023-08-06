from __future__ import annotations

import sys
import tempfile
from typing import IO, Any, ContextManager


class Capturing(ContextManager):
    """A context manager that captures stdout and stderr in a temporary file.

    This is used to suppress the output of a task and and retrieve it later if the task fails.
    The standard output and standard error streams are stored in the attributes `stdout`
    and `stderr` as strings.
    """

    stdout: str
    sterr: str

    def __enter__(self) -> Capturing:
        """Open temporary files and redirect stdout and stderr to it.

        Returns:
            The context manager itself.
        """
        # save stdout/stderr and replace them with a temporary file
        self._stdout, sys.stdout = sys.stdout, tempfile.TemporaryFile("r+")  # type: ignore
        self._stderr, sys.stderr = sys.stderr, tempfile.TemporaryFile("r+")  # type: ignore
        return self

    def __exit__(self, *args: Any) -> None:
        """Restore stdout and stderr and read the temporary files."""
        # get the output and restore stdout/stderr
        self.stdout, sys.stdout = _read_whole_file(sys.stdout), self._stdout
        self.stderr, sys.stderr = _read_whole_file(sys.stderr), self._stderr


def _read_whole_file(file: IO[str]) -> str:
    file.flush()
    file.seek(0)
    return file.read()
