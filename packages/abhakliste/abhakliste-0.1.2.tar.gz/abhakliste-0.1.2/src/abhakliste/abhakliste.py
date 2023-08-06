import os
import sys
import traceback
from contextlib import contextmanager
from subprocess import Popen
from typing import Any, Callable, Generator, List, Optional, Union

from abhakliste._capture import Capturing
from abhakliste._colors import Colors


class Abhakliste:
    """Abhakliste is a minimal task runner that prints a list of tasks and their status.

    The object provides several methods such as
    [run_context()][abhakliste.abhakliste.Abhakliste.run_context] and
    [run_cmd()][abhakliste.abhakliste.Abhakliste.run_cmd] that can be used
    to run tasks in sequence.
    The status of each task is printed to the console.
    If a task fails, the error message and its traceback are printed to the console but the program
    continues.
    Otherwise all output to stdout and stderr is suppressed.
    At the end of the program, the object can be used to raise an exception if any
    of the tasks failed.
    This can be used to fail a CI build if any of the tasks failed.

    Example:
        ```python
        from time import sleep
        from abhakliste import Abhakliste

        # Create a new Abhakliste instance.
        abhaker = Abhakliste()

        # Run first task in context
        with abhaker.run_context(desc="Test 1"):
            sleep(1)

        # Run second task as cmd
        abhaker.run_cmd(["ls", "-l"], desc="Test 2"):

        def _test3():
            sleep(1)
        abhaker.run_function(_test3, desc="Test 3")
        ```

    Attributes:
        error_runs: Number of tasks that failed.
        total_runs: Number of tasks that were run.
    """

    def __init__(self) -> None:
        self.error_runs: int = 0
        self.total_runs: int = 0

    @contextmanager
    def run_context(self, desc: str) -> Generator[None, None, None]:
        """The context manager that is used to run a tasks.

        It provides a context manager in which the a single task is run and its status is printed.
        The following functionality is provided by the the context manager:

        - Print the description of the task.
        - Capture stdout and stderr.
        - Print the status of the task.
        - Print the error message and traceback if the task failed.

        Args:
            desc: A short description of the task.

        Yields:
            Nothing is yielded.

        Example:
            ```python
            from time import sleep
            from abhakliste import Abhakliste

            # Run first task in context
            abhaker = Abhakliste()
            with abhaker.run_context(desc="Test 1"):
                sleep(1)
            ```
        """
        func_err: Optional[Exception] = None

        self.total_runs += 1

        # print run description
        just_width = min(max(_get_terminal_width() - 2, 30), 100)
        print(desc.ljust(just_width, "."), end="")
        sys.stdout.flush()

        # run function and capture output
        with Capturing() as capture:
            try:
                yield
            except Exception as e:
                self.error_runs += 1
                func_err = e

        # print output
        if func_err is None:
            print("✅")
        else:
            print("🚨")

            # print caputred output
            if capture.stdout:
                print(f"{Colors.BLUE}{Colors.BOLD}==>{Colors.END} Stdout:")
                print(capture.stdout)
            if capture.stderr:
                print(f"{Colors.BLUE}{Colors.BOLD}==>{Colors.END} Stderr:")
                print(capture.stderr)

            # print traceback
            print(f"{Colors.BLUE}{Colors.BOLD}==>{Colors.END} Traceback:")
            print(traceback.format_exc())

    def run_function(self, func: Callable, desc: str, *args: Any, **kwargs: Any) -> None:
        """Run a function as a task and print its status.

        This is a helper method that runs a function in a context managed by `run_context()`.
        The function is called with the provided arguments.
        If the function raises an exception, the task is considered to have failed.
        See [run_context()][abhakliste.abhakliste.Abhakliste.run_context] for more information.

        Args:
            func: Function that will be run as a task.
            desc: A short description of the task.
            *args: Positional arguments that will be passed to the function.
            **kwargs: Keyword arguments that will be passed to the function.

        Example:
            ```python
            from time import sleep
            from abhakliste import Abhakliste

            # Define a test function
            def test_func(time: int) -> None:
                sleep(time)

            # Run function as task
            abhaker = Abhakliste()
            abhaker.run_function(test_func, desc="Test 1", time=1)
            ```
        """
        with self.run_context(desc):
            func(*args, **kwargs)

    def run_cmd(
        self,
        args: Union[str, List[Any]],
        desc: str,
        shell: bool = False,
        cwd: Optional[str] = None,
        text: Optional[Any] = None,
        **kwargs: Any,
    ) -> None:
        """Run a command line command as a task and print its status.

        This is a thin wrapper around `subprocess.Popen()` that runs a command line command,
        waits for it to finish and checks its return code.
        If the return code is not `0`, the command is considered to have failed.
        A description of the command and its status is printed to the console.

        Args:
            args: A string, or a sequence of program arguments.
            desc: A short description of the task.
            shell: If `True`, the command will be executed through the shell.
            cwd: Sets the current directory before the child is executed.
            text: If `True`, the `stdout` and `stderr` arguments must be `str` and will be
            **kwargs: Keyword arguments that will be passed to `subprocess.Popen()`.

        Raises:
            RuntimeError: The command failed and the return code was not `0`.

        Example:
            ```python
            from time import sleep
            from abhakliste import Abhakliste

            # Run command as task
            abhaker = Abhakliste()
            abhaker.run_cmd(["ls", "-l"], desc="Run ls"):
            ```
        """
        with self.run_context(desc):
            p = Popen(
                args=args,
                shell=shell,
                cwd=cwd,
                stdout=sys.stdout,
                stderr=sys.stderr,
                text=text,
                **kwargs,
            )
            p.wait()
            if p.returncode != 0:
                raise RuntimeError("The command exited with a non-zero exit code.")

    def raise_on_fail(self) -> None:
        """Raise an exception if any of the tasks failed.

        This method can be used to fail a CI build if any of the tasks failed or to raise an
        exception if the program is run from the command line.

        Raises:
            RuntimeError: At least one task failed.
        """
        if self.error_runs > 0:
            raise RuntimeError(f"{self.error_runs} of {self.total_runs} runs failed.")


def _get_terminal_width() -> int:
    try:
        return os.get_terminal_size().columns
    except Exception:
        return 40
