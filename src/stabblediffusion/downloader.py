"""Download helpers using aria2c and wget."""

import subprocess
from pathlib import Path

from .config import DownloadTask


def build_aria2c_command(task: DownloadTask) -> list[str]:
    """Build an aria2c command from a DownloadTask."""
    return [
        "aria2c",
        "--console-log-level=error",
        "-c",
        "-x", str(task.connections),
        "-s", str(task.segments),
        "-k", task.min_split_size,
        task.url,
        "-d", task.output_dir,
        "-o", task.filename,
    ]


def build_wget_command(url: str, output_path: str) -> list[str]:
    """Build a wget command for a single file download."""
    return ["wget", url, "-O", output_path]


def download_file(task: DownloadTask) -> subprocess.CompletedProcess:
    """Download a file using aria2c."""
    cmd = build_aria2c_command(task)
    return subprocess.run(cmd, capture_output=True, text=True, check=False)


def download_with_wget(url: str, output_path: str) -> subprocess.CompletedProcess:
    """Download a file using wget."""
    cmd = build_wget_command(url, output_path)
    return subprocess.run(cmd, capture_output=True, text=True, check=False)


def ensure_directory(path: str) -> Path:
    """Ensure a directory exists, creating it if necessary."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def validate_url(url: str) -> bool:
    """Validate that a URL has the expected scheme."""
    return url.startswith("http://") or url.startswith("https://")


def get_filename_from_url(url: str) -> str:
    """Extract filename from a URL path."""
    return url.rstrip("/").split("/")[-1]
