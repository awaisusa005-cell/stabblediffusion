"""Tests for the downloader module."""

import subprocess
from pathlib import Path
from unittest.mock import patch

from stabblediffusion.config import DownloadTask
from stabblediffusion.downloader import (
    build_aria2c_command,
    build_wget_command,
    download_file,
    download_with_wget,
    ensure_directory,
    get_filename_from_url,
    validate_url,
)


class TestBuildAria2cCommand:
    def test_basic_command(self):
        task = DownloadTask(
            url="https://example.com/file.bin",
            output_dir="/tmp/out",
            filename="file.bin",
        )
        cmd = build_aria2c_command(task)
        assert cmd[0] == "aria2c"
        assert "--console-log-level=error" in cmd
        assert "-c" in cmd
        assert "https://example.com/file.bin" in cmd
        assert "-d" in cmd
        assert "/tmp/out" in cmd
        assert "-o" in cmd
        assert "file.bin" in cmd

    def test_connections_and_segments(self):
        task = DownloadTask(
            url="https://example.com/file.bin",
            output_dir="/tmp/out",
            filename="file.bin",
            connections=32,
            segments=32,
        )
        cmd = build_aria2c_command(task)
        x_idx = cmd.index("-x")
        s_idx = cmd.index("-s")
        assert cmd[x_idx + 1] == "32"
        assert cmd[s_idx + 1] == "32"

    def test_min_split_size(self):
        task = DownloadTask(
            url="https://example.com/file.bin",
            output_dir="/tmp/out",
            filename="file.bin",
            min_split_size="2M",
        )
        cmd = build_aria2c_command(task)
        k_idx = cmd.index("-k")
        assert cmd[k_idx + 1] == "2M"


class TestBuildWgetCommand:
    def test_basic_command(self):
        cmd = build_wget_command("https://example.com/file.py", "/tmp/file.py")
        assert cmd == ["wget", "https://example.com/file.py", "-O", "/tmp/file.py"]


class TestDownloadFile:
    @patch("stabblediffusion.downloader.subprocess.run")
    def test_calls_subprocess(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="", stderr=""
        )
        task = DownloadTask(
            url="https://example.com/file.bin",
            output_dir="/tmp/out",
            filename="file.bin",
        )
        result = download_file(task)
        assert result.returncode == 0
        mock_run.assert_called_once()
        call_args = mock_run.call_args
        assert call_args[0][0][0] == "aria2c"

    @patch("stabblediffusion.downloader.subprocess.run")
    def test_handles_failure(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(
            args=[], returncode=1, stdout="", stderr="error"
        )
        task = DownloadTask(
            url="https://example.com/file.bin",
            output_dir="/tmp/out",
            filename="file.bin",
        )
        result = download_file(task)
        assert result.returncode == 1


class TestDownloadWithWget:
    @patch("stabblediffusion.downloader.subprocess.run")
    def test_calls_subprocess(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="", stderr=""
        )
        result = download_with_wget("https://example.com/f.py", "/tmp/f.py")
        assert result.returncode == 0
        mock_run.assert_called_once()


class TestEnsureDirectory:
    def test_creates_directory(self, tmp_path):
        new_dir = str(tmp_path / "a" / "b" / "c")
        result = ensure_directory(new_dir)
        assert result.exists()
        assert result.is_dir()

    def test_existing_directory(self, tmp_path):
        result = ensure_directory(str(tmp_path))
        assert result == tmp_path


class TestValidateUrl:
    def test_https_url(self):
        assert validate_url("https://example.com/file") is True

    def test_http_url(self):
        assert validate_url("http://example.com/file") is True

    def test_ftp_url(self):
        assert validate_url("ftp://example.com/file") is False

    def test_empty_string(self):
        assert validate_url("") is False

    def test_no_scheme(self):
        assert validate_url("example.com/file") is False


class TestGetFilenameFromUrl:
    def test_simple_url(self):
        assert get_filename_from_url("https://example.com/model.bin") == "model.bin"

    def test_nested_path(self):
        assert (
            get_filename_from_url("https://example.com/a/b/c/file.safetensors")
            == "file.safetensors"
        )

    def test_trailing_slash(self):
        assert get_filename_from_url("https://example.com/dir/") == "dir"

    def test_url_with_query_params(self):
        result = get_filename_from_url("https://example.com/file.bin?token=abc")
        assert result == "file.bin?token=abc"
