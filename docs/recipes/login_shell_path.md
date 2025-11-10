# Using the login shell `PATH` in non-interactive environments

By default, `find-exe` searches only the current process’ `PATH`. 

In non-interactive environments (macOS GUI apps, cron/systemd, CI, containers) this `PATH` is often minimal, so tools that are available in your interactive terminal (e.g. Homebrew at `/opt/homebrew/bin`, pipx at `~/.local/bin`) may not be found.

If you want `find-exe` to output the same as in your interactive/login shell, one can capture that shell’s `PATH` once and pass it in via `paths=...`. 

The following snippet provides an example of how to do this:

```python
import os, platform, shutil, subprocess

COMMANDS = {
    "bash": [["bash", "-l", "-c", "echo $PATH"], ["bash", "-i", "-c", "echo $PATH"]],
    "zsh":  [["zsh", "-l", "-c", "print -r -- $path | paste -sd: -"], ["zsh", "-i", "-c", "echo $PATH"]],
    "fish": [["fish", "-l", "-c", "string join : $PATH"], ["fish", "-i", "-c", "string join : $PATH"]],
    "sh":   [["sh", "-l", "-c", "echo $PATH"], ["sh", "-i", "-c", "echo $PATH"]],
    "xonsh": [["xonsh", "-i", "--login", "-c", "print(':'.join($PATH))"], ["xonsh", "-i", "-c", "print(':'.join($PATH))"]],
}

def _windows_path() -> list[str]:
    ps = shutil.which("pwsh") or shutil.which("powershell")
    if ps:
        argv = [
            ps, "-NoProfile", "-Command",
            "$m=[Environment]::GetEnvironmentVariable('Path','Machine');"
            "$u=[Environment]::GetEnvironmentVariable('Path','User');"
            "[Environment]::ExpandEnvironmentVariables(($m,$u -join ';'))"
        ]
        p = subprocess.run(argv, capture_output=True, text=True)
        if p.returncode == 0 and p.stdout.strip():
            return [s for s in p.stdout.strip().split(os.pathsep) if s]
    return [s for s in os.environ.get("PATH", "").split(os.pathsep) if s]

def _posix_path(shell: str) -> list[str]:
    for argv in COMMANDS.get(shell, COMMANDS["bash"]):
        if shutil.which(argv[0]) is None:
            continue
        p = subprocess.run(argv, capture_output=True, text=True)
        if p.returncode == 0 and p.stdout.strip():
            return [s for s in p.stdout.strip().split(os.pathsep) if s]
    return [s for s in os.environ.get("PATH", "").split(os.pathsep) if s]

def shell_path(*, system: str | None = None, shell: str | None = None) -> list[str]:
    sysname = system or platform.system()
    if sysname == "Windows":
        return _windows_path()
    sh = shell or os.path.basename(os.environ.get("SHELL","")) or "bash"
    return _posix_path(sh)

# Usage:
# find_exe("ruff", paths=shell_path())                 # auto
# find_exe("ruff", paths=shell_path(system="Windows")) # force Windows
# find_exe("ruff", paths=shell_path(shell="zsh"))      # force shell on POSIX
```