"""Tests for the extensions module."""

import subprocess
from pathlib import Path
from unittest.mock import patch

from stabblediffusion.config import EXTENSIONS, WEBUI_DIR
from stabblediffusion.extensions import (
    build_clone_command,
    clone_extension,
    get_all_extension_urls,
    get_extension_name,
    get_extension_target_dir,
    get_extensions_dir,
    is_extension_installed,
    list_installed_extensions,
    validate_extension_url,
)


class TestGetExtensionName:
    def test_github_url(self):
        url = "https://github.com/AUTOMATIC1111/stable-diffusion-webui-rembg"
        assert get_extension_name(url) == "stable-diffusion-webui-rembg"

    def test_url_with_trailing_slash(self):
        url = "https://github.com/user/repo/"
        assert get_extension_name(url) == "repo"

    def test_simple_name(self):
        url = "https://github.com/user/my-ext"
        assert get_extension_name(url) == "my-ext"


class TestGetExtensionsDir:
    def test_returns_correct_path(self):
        result = get_extensions_dir()
        assert result == f"{WEBUI_DIR}/extensions"


class TestBuildCloneCommand:
    def test_basic_command(self):
        cmd = build_clone_command("https://github.com/user/repo", "/tmp/ext/repo")
        assert cmd == ["git", "clone", "https://github.com/user/repo", "/tmp/ext/repo"]


class TestGetExtensionTargetDir:
    def test_default_base_dir(self):
        url = "https://github.com/user/my-extension"
        result = get_extension_target_dir(url)
        assert result == f"{WEBUI_DIR}/extensions/my-extension"

    def test_custom_base_dir(self):
        url = "https://github.com/user/my-extension"
        result = get_extension_target_dir(url, "/custom/dir")
        assert result == "/custom/dir/my-extension"


class TestCloneExtension:
    @patch("stabblediffusion.extensions.subprocess.run")
    def test_calls_subprocess(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="", stderr=""
        )
        result = clone_extension("https://github.com/user/ext", "/tmp/ext")
        assert result.returncode == 0
        mock_run.assert_called_once()

    @patch("stabblediffusion.extensions.subprocess.run")
    def test_handles_failure(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(
            args=[], returncode=128, stdout="", stderr="fatal: repository not found"
        )
        result = clone_extension("https://github.com/user/ext", "/tmp/ext")
        assert result.returncode == 128


class TestListInstalledExtensions:
    def test_empty_directory(self, tmp_path):
        result = list_installed_extensions(str(tmp_path))
        assert result == []

    def test_with_extensions(self, tmp_path):
        (tmp_path / "ext-a").mkdir()
        (tmp_path / "ext-b").mkdir()
        (tmp_path / ".hidden").mkdir()
        result = list_installed_extensions(str(tmp_path))
        assert result == ["ext-a", "ext-b"]

    def test_nonexistent_directory(self):
        result = list_installed_extensions("/nonexistent/path/12345")
        assert result == []

    def test_sorted_output(self, tmp_path):
        (tmp_path / "zebra").mkdir()
        (tmp_path / "alpha").mkdir()
        (tmp_path / "middle").mkdir()
        result = list_installed_extensions(str(tmp_path))
        assert result == ["alpha", "middle", "zebra"]


class TestIsExtensionInstalled:
    def test_installed(self, tmp_path):
        (tmp_path / "my-ext").mkdir()
        assert is_extension_installed("my-ext", str(tmp_path)) is True

    def test_not_installed(self, tmp_path):
        assert is_extension_installed("my-ext", str(tmp_path)) is False


class TestGetAllExtensionUrls:
    def test_returns_copy(self):
        urls = get_all_extension_urls()
        assert urls == EXTENSIONS
        urls.append("new-url")
        assert get_all_extension_urls() == EXTENSIONS

    def test_all_are_strings(self):
        for url in get_all_extension_urls():
            assert isinstance(url, str)


class TestValidateExtensionUrl:
    def test_valid_github_url(self):
        assert validate_extension_url("https://github.com/user/repo") is True

    def test_invalid_non_github(self):
        assert validate_extension_url("https://gitlab.com/user/repo") is False

    def test_invalid_trailing_slash(self):
        assert validate_extension_url("https://github.com/user/repo/") is False

    def test_invalid_too_few_parts(self):
        assert validate_extension_url("https://github.com/user") is False

    def test_valid_deep_path(self):
        assert validate_extension_url("https://github.com/org/sub/repo") is True
