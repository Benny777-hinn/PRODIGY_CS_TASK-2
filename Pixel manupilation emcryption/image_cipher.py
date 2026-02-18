import argparse
from pathlib import Path

from PIL import Image


def apply_xor(value: int, key: int) -> int:
    return value ^ key


def apply_add(value: int, key: int, decrypt: bool = False) -> int:
    if decrypt:
        return (value - key) % 256
    return (value + key) % 256


def transform_pixel(pixel, key: int, method: str, decrypt: bool) -> tuple[int, ...]:
    if method == "xor":
        func = lambda v: apply_xor(v, key)
    elif method == "add":
        func = lambda v: apply_add(v, key, decrypt=decrypt)
    else:
        raise ValueError("Unsupported method")

    if isinstance(pixel, int):
        return (func(pixel),)

    return tuple(func(v) for v in pixel)


def swap_channels(pixel) -> tuple[int, ...]:
    if isinstance(pixel, int):
        return (pixel,)
    if len(pixel) >= 3:
        r, g, b, *rest = pixel
        return (b, g, r, *rest)
    return tuple(pixel)


def process_image(
    input_path: Path,
    output_path: Path,
    key: int,
    method: str,
    mode: str,
    swap_pairs: bool,
    swap_channels_flag: bool,
) -> None:
    img = Image.open(input_path)
    img = img.convert("RGBA")
    pixels = list(img.getdata())

    decrypt = mode == "decrypt"

    if swap_pairs:
        for i in range(0, len(pixels) - 1, 2):
            pixels[i], pixels[i + 1] = pixels[i + 1], pixels[i]

    transformed = []
    for p in pixels:
        current = p
        if swap_channels_flag:
            current = swap_channels(current)
        current = transform_pixel(current, key, method, decrypt)
        if swap_channels_flag:
            current = swap_channels(current)
        transformed.append(current)

    img.putdata(transformed)
    img.save(output_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Simple image encryption/decryption using pixel manipulation"
    )
    parser.add_argument("mode", choices=["encrypt", "decrypt"])
    parser.add_argument("input", type=str)
    parser.add_argument("output", type=str)
    parser.add_argument(
        "--key",
        type=int,
        required=True,
        help="Integer key between 0 and 255",
    )
    parser.add_argument(
        "--method",
        choices=["xor", "add"],
        default="xor",
        help="Pixel operation to use",
    )
    parser.add_argument(
        "--swap-pairs",
        action="store_true",
        help="Swap neighbouring pixels as part of the cipher",
    )
    parser.add_argument(
        "--swap-channels",
        action="store_true",
        help="Swap red and blue channels as part of the cipher",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    key = args.key % 256
    input_path = Path(args.input)
    output_path = Path(args.output)

    process_image(
        input_path=input_path,
        output_path=output_path,
        key=key,
        method=args.method,
        mode=args.mode,
        swap_pairs=args.swap_pairs,
        swap_channels_flag=args.swap_channels,
    )


if __name__ == "__main__":
    main()

