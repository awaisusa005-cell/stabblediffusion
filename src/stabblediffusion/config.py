"""Configuration constants for the Stable Diffusion WebUI setup."""

from dataclasses import dataclass, field


BASE_DIR = "/content"
WEBUI_DIR = f"{BASE_DIR}/stable-diffusion-webui"
WEBUI_REPO_URL = "https://github.com/camenduru/stable-diffusion-webui"
WEBUI_BRANCH = "v2.4"

CONTROLNET_BASE_URL = (
    "https://huggingface.co/ckpt/ControlNet-v1-1"
)
CONTROLNET_MODELS_DIR = (
    f"{WEBUI_DIR}/extensions/sd-webui-controlnet/models"
)

SD_MODEL_URL = (
    "https://huggingface.co/ckpt/sd14/resolve/main/sd-v1-4.ckpt"
)
SD_MODEL_DIR = f"{WEBUI_DIR}/models/Stable-diffusion"

TORCH_VERSION = "2.0.1+cu118"
TORCHVISION_VERSION = "0.15.2+cu118"
TORCHAUDIO_VERSION = "2.0.2+cu118"
XFORMERS_VERSION = "0.0.20"
TRITON_VERSION = "2.0.0"
GRADIO_CLIENT_VERSION = "0.2.7"

EXTENSIONS = [
    "https://github.com/deforum-art/deforum-for-automatic1111-webui",
    "https://github.com/camenduru/stable-diffusion-webui-images-browser",
    "https://github.com/camenduru/stable-diffusion-webui-huggingface",
    "https://github.com/camenduru/sd-civitai-browser",
    "https://github.com/kohya-ss/sd-webui-additional-networks",
    "https://github.com/Mikubill/sd-webui-controlnet",
    "https://github.com/fkunn1326/openpose-editor",
    "https://github.com/jexom/sd-webui-depth-lib",
    "https://github.com/hnmr293/posex",
    "https://github.com/nonnonstop/sd-webui-3d-open-pose-editor",
    "https://github.com/camenduru/sd-webui-tunnels",
    "https://github.com/etherealxx/batchlinks-webui",
    "https://github.com/camenduru/stable-diffusion-webui-catppuccin",
    "https://github.com/AUTOMATIC1111/stable-diffusion-webui-rembg",
    "https://github.com/ashen-sensored/stable-diffusion-webui-two-shot",
    "https://github.com/thomasasfk/sd-webui-aspect-ratio-helper",
    "https://github.com/tjm35/asymmetric-tiling-sd-webui",
]

CONTROLNET_SAFETENSOR_MODELS = [
    "control_v11e_sd15_ip2p_fp16",
    "control_v11e_sd15_shuffle_fp16",
    "control_v11p_sd15_canny_fp16",
    "control_v11f1p_sd15_depth_fp16",
    "control_v11p_sd15_inpaint_fp16",
    "control_v11p_sd15_lineart_fp16",
    "control_v11p_sd15_mlsd_fp16",
    "control_v11p_sd15_normalbae_fp16",
    "control_v11p_sd15_openpose_fp16",
    "control_v11p_sd15_scribble_fp16",
    "control_v11p_sd15_seg_fp16",
    "control_v11p_sd15_softedge_fp16",
    "control_v11p_sd15s2_lineart_anime_fp16",
    "control_v11f1e_sd15_tile_fp16",
]

T2I_ADAPTER_MODELS = [
    "t2iadapter_style_sd14v1",
    "t2iadapter_sketch_sd14v1",
    "t2iadapter_seg_sd14v1",
    "t2iadapter_openpose_sd14v1",
    "t2iadapter_keypose_sd14v1",
    "t2iadapter_depth_sd14v1",
    "t2iadapter_color_sd14v1",
    "t2iadapter_canny_sd14v1",
    "t2iadapter_canny_sd15v2",
    "t2iadapter_depth_sd15v2",
    "t2iadapter_sketch_sd15v2",
    "t2iadapter_zoedepth_sd15v1",
]


@dataclass
class DownloadTask:
    """Represents a file download task."""

    url: str
    output_dir: str
    filename: str
    connections: int = 16
    segments: int = 16
    min_split_size: str = "1M"


@dataclass
class WebUIConfig:
    """Configuration for launching the WebUI."""

    listen: bool = True
    xformers: bool = True
    insecure_extensions: bool = True
    theme: str = "dark"
    gradio_queue: bool = True
    multiple: bool = True
    extra_args: list[str] = field(default_factory=list)

    def to_args(self) -> list[str]:
        """Convert config to command-line arguments."""
        args = []
        if self.listen:
            args.append("--listen")
        if self.xformers:
            args.append("--xformers")
        if self.insecure_extensions:
            args.append("--enable-insecure-extension-access")
        if self.theme:
            args.extend(["--theme", self.theme])
        if self.gradio_queue:
            args.append("--gradio-queue")
        if self.multiple:
            args.append("--multiple")
        args.extend(self.extra_args)
        return args
