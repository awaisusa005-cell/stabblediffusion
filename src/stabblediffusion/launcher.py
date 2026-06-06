"""WebUI launcher utilities."""

import subprocess

from .config import WEBUI_DIR, WebUIConfig


def build_launch_command(config: WebUIConfig, webui_dir: str = WEBUI_DIR) -> list[str]:
    """Build the launch command for the WebUI."""
    return ["python", f"{webui_dir}/launch.py"] + config.to_args()


def apply_sed_patches(webui_dir: str = WEBUI_DIR) -> list[list[str]]:
    """Return the list of sed patch commands needed before launch."""
    patches = [
        [
            "sed", "-i", "-e",
            "/from modules import launch_utils/a\\import os",
            f"{webui_dir}/launch.py",
        ],
        [
            "sed", "-i", "-e",
            's/\\["sd_model_checkpoint"\\]/\\["sd_model_checkpoint","sd_vae","CLIP_stop_at_last_layers"\\]/g',
            f"{webui_dir}/modules/shared.py",
        ],
    ]
    return patches


def get_default_config() -> WebUIConfig:
    """Return the default WebUI configuration."""
    return WebUIConfig()


def launch_webui(
    config: WebUIConfig | None = None,
    webui_dir: str = WEBUI_DIR,
) -> subprocess.CompletedProcess:
    """Launch the WebUI with the given configuration."""
    if config is None:
        config = get_default_config()
    cmd = build_launch_command(config, webui_dir)
    return subprocess.run(cmd, capture_output=True, text=True, check=False)


def validate_webui_directory(webui_dir: str = WEBUI_DIR) -> bool:
    """Check if the WebUI directory exists and has the expected structure."""
    from pathlib import Path

    path = Path(webui_dir)
    required_files = ["launch.py", "webui.py"]
    if not path.is_dir():
        return False
    return all((path / f).exists() for f in required_files)
