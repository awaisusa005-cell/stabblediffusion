"""Tests for the config module."""

from stabblediffusion.config import (
    BASE_DIR,
    CONTROLNET_BASE_URL,
    CONTROLNET_MODELS_DIR,
    CONTROLNET_SAFETENSOR_MODELS,
    EXTENSIONS,
    SD_MODEL_DIR,
    SD_MODEL_URL,
    T2I_ADAPTER_MODELS,
    WEBUI_BRANCH,
    WEBUI_DIR,
    WEBUI_REPO_URL,
    DownloadTask,
    WebUIConfig,
)


class TestConstants:
    def test_base_dir(self):
        assert BASE_DIR == "/content"

    def test_webui_dir_under_base(self):
        assert WEBUI_DIR.startswith(BASE_DIR)

    def test_webui_repo_url_is_https(self):
        assert WEBUI_REPO_URL.startswith("https://")

    def test_webui_branch_not_empty(self):
        assert WEBUI_BRANCH

    def test_controlnet_base_url_is_https(self):
        assert CONTROLNET_BASE_URL.startswith("https://")

    def test_controlnet_models_dir_under_webui(self):
        assert CONTROLNET_MODELS_DIR.startswith(WEBUI_DIR)

    def test_sd_model_url_is_https(self):
        assert SD_MODEL_URL.startswith("https://")

    def test_sd_model_dir_under_webui(self):
        assert SD_MODEL_DIR.startswith(WEBUI_DIR)

    def test_extensions_not_empty(self):
        assert len(EXTENSIONS) > 0

    def test_all_extensions_are_https(self):
        for ext in EXTENSIONS:
            assert ext.startswith("https://"), f"{ext} is not HTTPS"

    def test_controlnet_models_not_empty(self):
        assert len(CONTROLNET_SAFETENSOR_MODELS) > 0

    def test_t2i_adapter_models_not_empty(self):
        assert len(T2I_ADAPTER_MODELS) > 0

    def test_no_duplicate_extensions(self):
        assert len(EXTENSIONS) == len(set(EXTENSIONS))

    def test_no_duplicate_controlnet_models(self):
        assert len(CONTROLNET_SAFETENSOR_MODELS) == len(
            set(CONTROLNET_SAFETENSOR_MODELS)
        )

    def test_no_duplicate_t2i_models(self):
        assert len(T2I_ADAPTER_MODELS) == len(set(T2I_ADAPTER_MODELS))


class TestDownloadTask:
    def test_default_values(self):
        task = DownloadTask(
            url="https://example.com/file.bin",
            output_dir="/tmp/out",
            filename="file.bin",
        )
        assert task.connections == 16
        assert task.segments == 16
        assert task.min_split_size == "1M"

    def test_custom_values(self):
        task = DownloadTask(
            url="https://example.com/file.bin",
            output_dir="/tmp/out",
            filename="file.bin",
            connections=8,
            segments=8,
            min_split_size="2M",
        )
        assert task.connections == 8
        assert task.segments == 8
        assert task.min_split_size == "2M"

    def test_stores_url(self):
        task = DownloadTask(
            url="https://example.com/model.safetensors",
            output_dir="/models",
            filename="model.safetensors",
        )
        assert task.url == "https://example.com/model.safetensors"
        assert task.output_dir == "/models"
        assert task.filename == "model.safetensors"


class TestWebUIConfig:
    def test_default_config(self):
        config = WebUIConfig()
        assert config.listen is True
        assert config.xformers is True
        assert config.insecure_extensions is True
        assert config.theme == "dark"
        assert config.gradio_queue is True
        assert config.multiple is True
        assert config.extra_args == []

    def test_to_args_default(self):
        config = WebUIConfig()
        args = config.to_args()
        assert "--listen" in args
        assert "--xformers" in args
        assert "--enable-insecure-extension-access" in args
        assert "--theme" in args
        assert "dark" in args
        assert "--gradio-queue" in args
        assert "--multiple" in args

    def test_to_args_disabled_flags(self):
        config = WebUIConfig(
            listen=False,
            xformers=False,
            insecure_extensions=False,
            theme="",
            gradio_queue=False,
            multiple=False,
        )
        args = config.to_args()
        assert "--listen" not in args
        assert "--xformers" not in args
        assert "--enable-insecure-extension-access" not in args
        assert "--theme" not in args
        assert "--gradio-queue" not in args
        assert "--multiple" not in args

    def test_to_args_custom_theme(self):
        config = WebUIConfig(theme="light")
        args = config.to_args()
        idx = args.index("--theme")
        assert args[idx + 1] == "light"

    def test_to_args_extra_args(self):
        config = WebUIConfig(extra_args=["--api", "--port", "7860"])
        args = config.to_args()
        assert "--api" in args
        assert "--port" in args
        assert "7860" in args

    def test_to_args_order_stability(self):
        config = WebUIConfig()
        args1 = config.to_args()
        args2 = config.to_args()
        assert args1 == args2
