# **PDF Watermark Removal Tool**
A Python-based tool for converting PDF files to images and removing image-based watermarks using OpenCV template matching and inpainting techniques.

<br>

## Features

- PDF to Image Conversion: Convert PDF files to high-quality PNG images
- Watermark Detection: Locate watermarks using template matching
- Watermark Removal: Remove detected watermarks using OpenCV inpainting
- Interactive CLI: User-friendly command-line interface with menu options
- Configurable Settings: Adjustable DPI and detection threshold
- Multiple Watermark Support: Detect and remove multiple instances of the same watermark
<br>

## Dependencies

- Poppler: Required for PDF processing

  - Windows: Download lateset release ```https://github.com/oschwartz10612/poppler-windows/releases/``` and add to PATH 

  - macOS: 
    ``` 
    brew install poppler
    ```
  - Linux: 
    (Ubuntu/Debian)
    ```
    sudo apt-get install poppler-utils 
    ```
    or
    (CentOS/RHEL)
    ```
    sudo yum install poppler-utils 
    ```
- Python Dependencies:
  ```bash
  pip install pdf2image opencv-python numpy
  ```
<br>

## Running the Program
```bash
python watermark_tool.py
```
