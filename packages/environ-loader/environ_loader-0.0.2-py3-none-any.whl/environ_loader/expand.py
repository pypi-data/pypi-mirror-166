import subprocess
import shutil
import typing


class unsafe_shell_expander:
    """
    Expand variable values by invoking a shell to parse the value and expand variable.
    You should ONLY evaluate data you TRUST.
    """

    def __init__(
        self,
        shell_cmd: str,
        echo_cmd: str,
        shell_opts: typing.List[str] = [],
        output_filter: typing.Callable[[str], str] = lambda x: x.rstrip('\n'),
    ) -> None:
        self.shell_cmd: str = shell_cmd
        self.shell_opts: typing.List[str] = shell_opts
        self.echo_cmd: str = echo_cmd
        self.output_filter: typing.Callable[[str], str] = output_filter

        if shutil.which(shell_cmd) is None:
            raise RuntimeError(
                f"Could not find `{shell_cmd}` executable to use for variable expansion."
            )
        self.shell_cmd = str(shutil.which(shell_cmd))

    def __call__(self, value: str) -> str:
        cmd: typing.List[str] = [self.shell_cmd, *self.shell_opts, f"{self.echo_cmd} {value}"]
        try:
            output: str = self.output_filter(subprocess.check_output(cmd, text=True))
        except Exception as e:
            raise RuntimeError(
                "There was problem running the shell to expand variable value."
            )

        return output


class unsafe_bash_expander(unsafe_shell_expander):
    def __init__(self) -> None:
        super().__init__("bash", "echo", ["-c"])


class unsafe_cmd_expander(unsafe_shell_expander):
    def __init__(self) -> None:
        super().__init__("cmd", "echo", ["/c"])
