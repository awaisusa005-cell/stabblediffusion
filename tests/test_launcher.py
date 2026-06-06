"""Tests for the launcher module."""

import subprocess
from pathlib import Path
from unittest.mock import patch

from stabblediffusion.config import WEBUI_DIR, WebUIConfig
from stabblediffusion.launcher import (
    apply_sed_patches,
    build_launch_command,
    get_default_config,
    launch_webui,
    validate_webui_directory,
)


class TestBuildLaunchCommand:
    def test_default_config(self):
        config = WebUIConfig()
        cmd = build_launch_command(config)
        assert cmd[0] == "python"
        assert f"{WEBUI_DIR}/launch.py" in cmd[1]
        assert "--listen" in cmd
        assert "--xformers" in cmd

    def test_custom_webui_dir(self):
        config = WebUIConfig()
        cmd = build_launch_command(config, webui_dir="/my/webui")
        assert cmd[1] == "/my/webui/launch.py"

    def test_minimal_config(self):
        config = WebUIConfig(
            listen=False,
            xformers=False,
            insecure_extensions=False,
            theme="",
            gradio_queue=False,
            multiple=False,
        )
        cmd = build_launch_command(config)
        assert cmd == ["python", f"{WEBUI_DIR}/launch.py"]


class TestApplySedPatches:
    def test_returns_list_of_commands(self):
        patches = apply_sed_patches()
        assert isinstance(patches, list)
        assert len(patches) >= 2
        for patch_cmd in patches:
            assert patch_cmd[0] == "sed"

    def test_custom_webui_dir(self):
        patches = apply_sed_patches("/custom/webui")
        for patch_cmd in patches:
            assert any("/custom/webui" in arg for arg in patch_cmd)

    def test_targets_correct_files(self):
        patches = apply_sed_patches()
        file_targets = [p[-1] for p in patches]
        assert any("launch.py" in f for f in file_targets)
        assert any("shared.py" in f for f in file_targets)


class TestGetDefaultConfig:
    def test_returns_webui_config(self):
        config = get_default_config()
        assert isinstance(config, WebUIConfig)

    def test_default_values(self):
        config = get_default_config()
        assert config.listen is True
        assert config.xformers is True
        assert config.theme == "dark"


class TestLaunchWebui:
    @patch("stabblediffusion.launcher.subprocess.run")
    def test_calls_subprocess(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="", stderr=""
        )
        result = launch_webui()
        assert result.returncode == 0
        mock_run.assert_called_once()

    @patch("stabblediffusion.launcher.subprocess.run")
    def test_uses_provided_config(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="", stderr=""
        )
        config = WebUIConfig(listen=False, xformers=False)
        launch_webui(config=config)
        call_args = mock_run.call_args[0][0]
        assert "--listen" not in call_args
        assert "--xformers" not in call_args

    @patch("stabblediffusion.launcher.subprocess.run")
    def test_uses_custom_dir(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="", stderr=""
        )
        launch_webui(webui_dir="/custom/dir")
        call_args = mock_run.call_args[0][0]
        assert "/custom/dir/launch.py" in call_args


class TestValidateWebuiDirectory:
    def test_valid_directory(self, tmp_path):
        (tmp_path / "launch.py").touch()
        (tmp_path / "webui.py").touch()
        assert validate_webui_directory(str(tmp_path)) is True

    def test_missing_launch_py(self, tmp_path):
        (tmp_path / "webui.py").touch()
        assert validate_webui_directory(str(tmp_path)) is False

    def test_missing_webui_py(self, tmp_path):
        (tmp_path / "launch.py").touch()
        assert validate_webui_directory(str(tmp_path)) is False

    def test_nonexistent_directory(self):
        assert validate_webui_directory("/nonexistent/dir/12345") is False
