"""
Shared utilities for MHI2D and MHI3D: config, subprocess, directory lookup, script I/O.
"""
from __future__ import print_function

import os
import pickle
import subprocess
from typing import Callable, List, Optional

CONFIG_NAME = ".masterHI.config"
CONFIG_VERSION = 1

# Encodings for robust cross-platform I/O
BRUKER_ENCODING = "latin-1"   # Bruker acqus/acqu2s/acqu3s, pulseprogram
TEXT_ENCODING = "utf-8"       # nuslist, scripts; use errors='replace' when reading unknown input


def find_bruker_data_dir(
    dir_path: Optional[str],
    validator: Callable[[str], bool],
) -> Optional[str]:
    """
    Find directory containing valid Bruker data.
    validator(path) returns True if path has valid Bruker data (e.g. Bruker2D(d).valid).
    Searches dir_path, or . / .. / ../.. / ../../.. if dir_path is '.' or None.
    """
    if dir_path in (".", None):
        test_dirs = [".", "..", "../..", "../../.."]
    else:
        test_dirs = [dir_path]

    for test_dir in test_dirs:
        if os.path.exists(test_dir) and os.path.isdir(test_dir) and validator(test_dir):
            return test_dir
    return None


def load_saved_args(
    default_factory: Callable[[], object],
    config_path: str = CONFIG_NAME,
) -> object:
    """Load saved options from config_path; return default_factory() if missing or invalid."""
    if not os.path.isfile(config_path):
        return default_factory()
    try:
        with open(config_path, "rb") as f:
            raw = pickle.load(f)
    except (OSError, pickle.PickleError, AttributeError, EOFError):
        return default_factory()

    if isinstance(raw, tuple) and len(raw) == 2 and raw[0] == CONFIG_VERSION:
        return raw[1]
    return default_factory()


def save_args(savedargs: object, config_path: str = CONFIG_NAME) -> None:
    """Persist options to config_path with version prefix for migration."""
    try:
        with open(config_path, "wb") as f:
            pickle.dump((CONFIG_VERSION, savedargs), f)
    except OSError as e:
        raise OSError(f"Failed to write config {config_path}: {e}") from e


def run_cmd(
    cmd: str,
    cwd: Optional[str] = None,
    check: bool = True,
) -> subprocess.CompletedProcess:
    """
    Run a shell command via subprocess.
    Raises subprocess.CalledProcessError on non-zero exit when check=True.
    """
    cwd = cwd or os.getcwd()
    r = subprocess.run(
        cmd,
        shell=True,
        cwd=cwd,
        capture_output=False,
    )
    if check and r.returncode != 0:
        raise subprocess.CalledProcessError(r.returncode, cmd)
    return r


def chmod_executable(*paths: str) -> None:
    """Make paths executable (0o770)."""
    for p in paths:
        os.chmod(p, 0o770)


def run_script(
    script_path: str,
    *args: str,
    cwd: Optional[str] = None,
    chmod_first: bool = True,
) -> subprocess.CompletedProcess:
    """Chmod 0o770 script_path (if chmod_first), then run ./script_path [args] in cwd."""
    cwd = cwd or os.getcwd()
    if chmod_first:
        chmod_executable(script_path)
    cmd = os.path.join(".", os.path.basename(script_path))
    if args:
        cmd += " " + " ".join(args)
    return run_cmd(cmd, cwd=cwd, check=True)


def write_script(path: str, lines: List[str]) -> None:
    """Write lines to path, each followed by newline."""
    try:
        with open(path, "w", encoding=TEXT_ENCODING) as f:
            for line in lines:
                f.write(f"{line}\n")
    except OSError as e:
        raise OSError(f"Failed to write script {path}: {e}") from e
