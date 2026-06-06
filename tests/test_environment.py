"""Tests for the environment module."""

import os
from unittest.mock import patch

from stabblediffusion.environment import (
    build_apt_install_command,
    build_pip_install_command,
    get_apt_packages,
    get_environment_variable,
    get_pip_extra_packages,
    get_pip_torch_packages,
    set_environment_variable,
)


class TestGetPipTorchPackages:
    def test_returns_list(self):
        packages = get_pip_torch_packages()
        assert isinstance(packages, list)
        assert len(packages) > 0

    def test_contains_torch(self):
        packages = get_pip_torch_packages()
        torch_pkgs = [p for p in packages if p.startswith("torch==")]
        assert len(torch_pkgs) == 1

    def test_contains_torchvision(self):
        packages = get_pip_torch_packages()
        tv_pkgs = [p for p in packages if p.startswith("torchvision==")]
        assert len(tv_pkgs) == 1

    def test_contains_torchaudio(self):
        packages = get_pip_torch_packages()
        ta_pkgs = [p for p in packages if p.startswith("torchaudio==")]
        assert len(ta_pkgs) == 1

    def test_all_have_versions(self):
        packages = get_pip_torch_packages()
        for pkg in packages:
            assert "==" in pkg, f"{pkg} missing version pin"


class TestGetPipExtraPackages:
    def test_returns_list(self):
        packages = get_pip_extra_packages()
        assert isinstance(packages, list)
        assert len(packages) > 0

    def test_contains_xformers(self):
        packages = get_pip_extra_packages()
        xf = [p for p in packages if p.startswith("xformers==")]
        assert len(xf) == 1

    def test_all_have_versions(self):
        packages = get_pip_extra_packages()
        for pkg in packages:
            assert "==" in pkg


class TestGetAptPackages:
    def test_returns_list(self):
        packages = get_apt_packages()
        assert isinstance(packages, list)
        assert len(packages) > 0

    def test_contains_aria2(self):
        assert "aria2" in get_apt_packages()


class TestBuildPipInstallCommand:
    def test_basic_command(self):
        cmd = build_pip_install_command(["numpy"])
        assert cmd[0] == "pip"
        assert "install" in cmd
        assert "numpy" in cmd

    def test_quiet_flag(self):
        cmd = build_pip_install_command(["numpy"], quiet=True)
        assert "-q" in cmd

    def test_no_quiet_flag(self):
        cmd = build_pip_install_command(["numpy"], quiet=False)
        assert "-q" not in cmd

    def test_upgrade_flag(self):
        cmd = build_pip_install_command(["numpy"], upgrade=True)
        assert "-U" in cmd

    def test_no_upgrade_flag(self):
        cmd = build_pip_install_command(["numpy"], upgrade=False)
        assert "-U" not in cmd

    def test_extra_index_url(self):
        cmd = build_pip_install_command(
            ["torch"], extra_index_url="https://download.pytorch.org/whl/cu118"
        )
        assert "--extra-index-url" in cmd
        assert "https://download.pytorch.org/whl/cu118" in cmd

    def test_no_extra_index_url(self):
        cmd = build_pip_install_command(["numpy"])
        assert "--extra-index-url" not in cmd

    def test_multiple_packages(self):
        cmd = build_pip_install_command(["numpy", "pandas", "scipy"])
        assert "numpy" in cmd
        assert "pandas" in cmd
        assert "scipy" in cmd


class TestBuildAptInstallCommand:
    def test_basic_command(self):
        cmd = build_apt_install_command(["vim"])
        assert cmd[0] == "apt"
        assert "-y" in cmd
        assert "install" in cmd
        assert "vim" in cmd

    def test_quiet_flag(self):
        cmd = build_apt_install_command(["vim"], quiet=True)
        assert "-qq" in cmd

    def test_no_quiet_flag(self):
        cmd = build_apt_install_command(["vim"], quiet=False)
        assert "-qq" not in cmd


class TestEnvironmentVariables:
    def test_set_and_get(self):
        set_environment_variable("TEST_SD_VAR", "hello")
        assert get_environment_variable("TEST_SD_VAR") == "hello"
        del os.environ["TEST_SD_VAR"]

    def test_get_default(self):
        result = get_environment_variable("NONEXISTENT_VAR_12345", "fallback")
        assert result == "fallback"

    def test_get_empty_default(self):
        result = get_environment_variable("NONEXISTENT_VAR_12345")
        assert result == ""
