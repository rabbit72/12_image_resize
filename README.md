# Image Resizer

This script takes the path to the image and puts an image with a new size
where the user will say or next to the source.
Required argument is the path to the original image.

Supported Extensions: jpg, jpeg, bmp, png
# How install 
Python 3 should be already installed. Then use pip (or pip3 if there is a conflict with old Python 2 setup) to install dependencies:

```bash
$ pip install -r requirements.txt
```
# Quick start

```bash
$ python3 image_resize.py <path_to_img>
```
Running on Windows is similar.

*(Possibly requires call of 'python' executive instead of just 'python3'.)*

# Supported arguments
```bash
usage: image_resize.py [-h] [--width WIDTH] [--height HEIGHT] [--scale SCALE]
                       [--output OUTPUT]
                       path_to_img

positional arguments:
  path_to_img      Path to image

optional arguments:
  -h, --help       show this help message and exit
  --width WIDTH    Required image width
  --height HEIGHT  Required image height
  --scale SCALE    Required scale image
  --output OUTPUT  Directory for new picture
```
1. If only the width is specified, the height is considered to preserve the
aspect ratio of the image. And vice versa. 
1. If both width and height are specified - create this image. Display a warning
in the console if the proportions do not match the original image.
1. If the scale is specified, the width and height can not be specified.
Otherwise, no resize occurs and the script breaks with an understandable error.
1. If no path is specified before the final file, the result is placed next to
the source file. If the source file is called ```pic.jpg``` (100x200), then after
the call to ```python image_resize.py --scale 2 pic.jpg``` the file
```pic__200x400.jpg``` should appear.
# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
