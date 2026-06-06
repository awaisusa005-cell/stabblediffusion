"""Extension management for the Stable Diffusion WebUI."""

import subprocess
from pathlib import Path

from .config import EXTENSIONS, WEBUI_DIR


def get_extension_name(url: str) -> str:
    """Extract the extension name from a git URL."""
    return url.rstrip("/").split("/")[-1]


def get_extensions_dir() -> str:
    """Return the path to the extensions directory."""
    return f"{WEBUI_DIR}/extensions"


def build_clone_command(url: str, target_dir: str) -> list[str]:
    """Build a git clone command for an extension."""
    return ["git", "clone", url, target_dir]


def get_extension_target_dir(url: str, base_dir: str | None = None) -> str:
    """Get the target directory for an extension."""
    ext_dir = base_dir or get_extensions_dir()
    name = get_extension_name(url)
    return f"{ext_dir}/{name}"


def clone_extension(url: str, target_dir: str) -> subprocess.CompletedProcess:
    """Clone an extension repository."""
    cmd = build_clone_command(url, target_dir)
    return subprocess.run(cmd, capture_output=True, text=True, check=False)


def list_installed_extensions(extensions_dir: str | None = None) -> list[str]:
    """List installed extensions by scanning the extensions directory."""
    ext_dir = Path(extensions_dir or get_extensions_dir())
    if not ext_dir.exists():
        return []
    return sorted(
        d.name for d in ext_dir.iterdir() if d.is_dir() and not d.name.startswith(".")
    )


def is_extension_installed(name: str, extensions_dir: str | None = None) -> bool:
    """Check if an extension is already installed."""
    return name in list_installed_extensions(extensions_dir)


def get_all_extension_urls() -> list[str]:
    """Return the full list of extension URLs."""
    return list(EXTENSIONS)


def validate_extension_url(url: str) -> bool:
    """Validate that an extension URL looks correct."""
    return (
        url.startswith("https://github.com/")
        and url.count("/") >= 4
        and not url.endswith("/")
    )
