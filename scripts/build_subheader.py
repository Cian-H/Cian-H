import base64
from jinja2 import Template
from pathlib import Path
import mimetypes
import requests
from typing import Any


SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
TEMPLATE_PATH = REPO_ROOT / "templates/subheader.svg.j2"
OUTPUT_PATH = REPO_ROOT / "subheader.svg"

IMAGE_URL_MAP: dict[str, Any] = {
    "python": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg",
    "rust": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/rust/rust-original.svg",
    "julia": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/julia/julia-original.svg",
    "elixir": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/elixir/elixir-original.svg",
    "numpy": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/numpy/numpy-original.svg",
    "pandas": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/pandas/pandas-original.svg",
    "pytorch": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/pytorch/pytorch-original.svg",
    "nixos": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nixos/nixos-original.svg",
    "bongo": "https://media.tenor.com/0ygiqFaX-ssAAAAC/bongo-cat-typing.gif"
}
ICONS: list[str] = ["python", "rust", "julia", "elixir", "numpy", "pandas", "pytorch", "nixos"]


def get_base64_from_url(url: str) -> str:
    print(f"Downloading {url}...")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        content_type = response.headers.get('Content-Type')
        if not content_type:
             content_type, _ = mimetypes.guess_type(url)

        b64_data = base64.b64encode(response.content).decode('utf-8')
        return f"data:{content_type};base64,{b64_data}"

    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return ""


def fetch_images_from_url_values(image_map: dict[str, str]) -> dict[str, str]:
    return {k: get_base64_from_url(v) for k, v in image_map.items()}


def render_template(template_filepath: Path, token_map: dict[str, str]) -> str:
    with template_filepath.open("rt") as f:
        template = f.read()
    return Template(template).render(**token_map)


def build_svg(filepath: Path, template_filepath: Path, token_map: dict[str, str]):
    svg_template = render_template(template_filepath, token_map)
    with filepath.open("wt+") as f:
        f.write(svg_template)


def main():
    token_map = fetch_images_from_url_values(IMAGE_URL_MAP)
    token_map["icons"] = [v for k, v in token_map.items() if k in ICONS]
    build_svg(OUTPUT_PATH, TEMPLATE_PATH, token_map)
    print(f"Finished building {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
