"""Environment setup utilities for the Stable Diffusion WebUI."""

import os
import subprocess

from .config import (
    GRADIO_CLIENT_VERSION,
    TORCH_VERSION,
    TORCHAUDIO_VERSION,
    TORCHVISION_VERSION,
    TRITON_VERSION,
    XFORMERS_VERSION,
)


def get_pip_torch_packages() -> list[str]:
    """Return the list of torch pip packages with versions."""
    return [
        f"torch=={TORCH_VERSION}",
        f"torchvision=={TORCHVISION_VERSION}",
        f"torchaudio=={TORCHAUDIO_VERSION}",
        "torchtext==0.15.2",
        "torchdata==0.6.1",
    ]


def get_pip_extra_packages() -> list[str]:
    """Return the list of extra pip packages with versions."""
    return [
        f"xformers=={XFORMERS_VERSION}",
        f"triton=={TRITON_VERSION}",
        f"gradio_client=={GRADIO_CLIENT_VERSION}",
    ]


def get_apt_packages() -> list[str]:
    """Return the list of required apt packages."""
    return ["aria2", "libcairo2-dev", "pkg-config", "python3-dev"]


def build_pip_install_command(
    packages: list[str],
    extra_index_url: str | None = None,
    upgrade: bool = True,
    quiet: bool = True,
) -> list[str]:
    """Build a pip install command."""
    cmd = ["pip", "install"]
    if quiet:
        cmd.append("-q")
    cmd.extend(packages)
    if extra_index_url:
        cmd.extend(["--extra-index-url", extra_index_url])
    if upgrade:
        cmd.append("-U")
    return cmd


def build_apt_install_command(packages: list[str], quiet: bool = True) -> list[str]:
    """Build an apt install command."""
    cmd = ["apt", "-y", "install"]
    if quiet:
        cmd.append("-qq")
    cmd.extend(packages)
    return cmd


def set_environment_variable(key: str, value: str) -> None:
    """Set an environment variable in the current process."""
    os.environ[key] = value


def get_environment_variable(key: str, default: str = "") -> str:
    """Get an environment variable value."""
    return os.environ.get(key, default)


def install_packages(
    packages: list[str],
    extra_index_url: str | None = None,
) -> subprocess.CompletedProcess:
    """Install pip packages."""
    cmd = build_pip_install_command(packages, extra_index_url)
    return subprocess.run(cmd, capture_output=True, text=True, check=False)


def install_apt_packages(packages: list[str]) -> subprocess.CompletedProcess:
    """Install apt packages."""
    cmd = build_apt_install_command(packages)
    return subprocess.run(cmd, capture_output=True, text=True, check=False)
