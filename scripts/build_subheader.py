import base64
from jinja2 import Template
import requests


SUBHEADER_FILENAME: str = "subheader.svg"
IMAGE_URL_MAP: dict[str, str] = {
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


def get_base64(url: str) -> str:
    print(f"Downloading {url}...")
    response = requests.get(url)
    if url.endswith(".gif"):
        media_type = "image/gif"
    elif url.endswith(".svg"):
        media_type = "image/svg+xml"
    else:
        raise ValueError("URL must be .gif or .svg")
    b64_data = base64.b64encode(response.content).decode('utf-8')
    return f"data:{media_type};base64,{b64_data}"


def fetch_images_from_url_values(image_map: dict[str, str]) -> dict[str, str]:
    return {k: get_base64(v) for k, v in image_map.items()}


def render_template(template_filename: str, token_map: dict[str, str]) -> str:
    with open(template_filename, "rt") as f:
        template = f.read()
    return Template(template).render(**token_map)


def build_svg(filename: str, token_map: dict[str, str]):
    template_filename = f"templates/{filename}.j2"
    svg_template = render_template(template_filename, token_map)
    with open(filename, "wt+") as f:
        f.write(svg_template)


def main():
    token_map = fetch_images_from_url_values(IMAGE_URL_MAP)
    build_svg(SUBHEADER_FILENAME, token_map)
    print(f"Finished building {SUBHEADER_FILENAME}")


if __name__ == "__main__":
    main()
