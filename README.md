# PRODIGY_CS_TASK-2
IMAGE PIXEL MANIPULATION ENCRYPTION AND DECRYPTION
# Pixel Image Encryption Tool

A simple image encryption and decryption tool using **pixel manipulation**.

This project has:

- A **Python CLI** to encrypt/decrypt images using pixel operations.
- A **browser-based UI** (pure HTML/CSS/JavaScript) to do the same operations without installing anything extra.

## Features

- Encrypt and decrypt images with a numeric key.
- Pixel-wise operations:
  - Bitwise **XOR**.
  - **Add/Subtract** modulo 256.
- Optional scrambling:
  - Swap **neighbouring pixels** (pair swapping).
  - Swap **color channels** (R ↔ B).
- Fully reversible: using the same settings you can get back the original image.

---

## Project Structure

```text
.
├── image_cipher.py   # Python command-line tool
└── index.html        # Simple web UI (HTML + CSS + JS)
```

---

## 1. Python CLI Usage

### Requirements

- Python 3
- [Pillow](https://python-pillow.org/) library

Install Pillow:

```bash
pip install pillow
```

### Basic Command

From the project folder:

```bash
python image_cipher.py MODE INPUT_PATH OUTPUT_PATH --key KEY [--method xor|add] [--swap-pairs] [--swap-channels]
```

**Arguments**

- `MODE`
  - `encrypt` – encrypt the image.
  - `decrypt` – decrypt an image previously encrypted with the same settings.
- `INPUT_PATH`
  - Path to input image (e.g. `input.png`, `photo.jpg`).
- `OUTPUT_PATH`
  - Path to save the output image (e.g. `encrypted.png`).
- `--key KEY`
  - Integer key (0–255). Internally reduced using `key % 256`.
- `--method`
  - `xor` (default) – bitwise XOR on each color channel.
  - `add` – add/subtract the key on each channel modulo 256.
- `--swap-pairs`
  - If set, neighbouring pixels are swapped in pairs (0↔1, 2↔3, …).
- `--swap-channels`
  - If set, the Red and Blue channels are swapped (R ↔ B) during processing.

### Examples

Encrypt with XOR and extra scrambling:

```bash
python image_cipher.py encrypt input.png encrypted.png --key 123 --method xor --swap-pairs --swap-channels
```

Decrypt back to original:

```bash
python image_cipher.py decrypt encrypted.png decrypted.png --key 123 --method xor --swap-pairs --swap-channels
```

Encrypt with add/subtract (no extra swaps):

```bash
python image_cipher.py encrypt input.jpg enc.jpg --key 77 --method add
```

Decrypt:

```bash
python image_cipher.py decrypt enc.jpg dec.jpg --key 77 --method add
```

To see all options:

```bash
python image_cipher.py --help
```

---

## 2. Web UI (HTML + CSS + JavaScript)

`index.html` is a self-contained page that lets you encrypt and decrypt images entirely in the browser.

No backend or server is required.

### How to Run

1. Open the project folder in your file explorer.
2. Double-click `index.html`.
3. Your default browser (Chrome/Edge/etc.) will open the app.

### Using the Web App

1. **Choose image** – select an image file from your computer.
2. **Mode** – select:
   - `Encrypt` or
   - `Decrypt`.
3. **Method** – select:
   - `XOR` or
   - `Add/Subtract`.
4. **Key (0–255)** – enter a numeric key (same idea as the Python tool).
5. **Extra scrambling** (optional):
   - `Swap neighbouring pixels` – pairwise pixel swapping.
   - `Swap R/B channels` – swap red and blue channels.
6. Click **“Encrypt / Decrypt”**.

The app will:

- Show the **original** image on the left.
- Show the **result** on the right.
- Offer a **“Download result”** link to save the processed image as a PNG.

To decrypt a previously encrypted image, use exactly the **same**:

- Mode (`Decrypt` for decrypting),
- Method (`XOR` or `Add/Subtract`),
- Key,
- Extra options (swap neighbours / swap channels).

---

## How the Encryption Works (Conceptual)

For each pixel:

1. Optionally **swap channels**:
   - Swap Red and Blue (R ↔ B) if the option is enabled.
2. Apply pixel-wise math using the key:
   - **XOR method**:
     - `R = R ^ key`
     - `G = G ^ key`
     - `B = B ^ key`
   - **Add/Subtract method**:
     - Encrypt: add key modulo 256: `(value + key) % 256`
     - Decrypt: subtract key modulo 256: `(value - key) % 256`
3. Optionally **swap channels back**.
4. Treat alpha channel (transparency) as-is (not modified by key).

If **neighbouring swap** is enabled, pixel pairs are swapped:

- (pixel 0 ↔ 1), (2 ↔ 3), (4 ↔ 5), …

This operation is its own inverse, so applying the same mode and settings again will undo it.

Because every operation is either self-inverse (XOR, swaps) or has a defined inverse (add/subtract modulo 256), the process is reversible.

---

## Notes

- Recommended lossless format for best reversibility: **PNG**.
- This is an educational / lightweight encryption tool, not a replacement for strong cryptography in security-critical applications.
- You can use the Python script for batch processing and the web UI for quick visual experimentation.
