import argparse
import os.path
from PIL import Image


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'path_to_img',
        help='Path to image'
    )
    parser.add_argument(
        '--width',
        type=int,
        help='Required image width'

    )
    parser.add_argument(
        '--height',
        type=int,
        help='Required image height'
    )
    parser.add_argument(
        '--scale',
        type=float,
        help='Required scale image'
    )
    parser.add_argument(
        '--output',
        help='Directory for new picture'
    )
    return parser.parse_args()


def check_path_to_img(path_to_picture):
    if not os.path.isfile(path_to_picture):
        exit('Incorrect path to image')


def check_dir_for_save(path_for_save):
    if path_for_save and not os.path.isdir(path_for_save):
        exit('Incorrect path for save')


def check_args(args):
    check_path_to_img(args.path_to_img)
    check_dir_for_save(args.output)
    width, height, scale = args.width, args.height, args.scale
    if not any((width, height, scale)):
        exit('No resizing specified')
    if scale and (width or height):
        exit('Сan not use "scale" with "width" or "height"')
    for number in (width, height, scale):
        if number and number <= 0:
            exit('Value can not be <= 0')


def get_size_for_new_img(current_size, args):
    width, height, scale = args.width, args.height, args.scale
    current_ratio = get_ratio(current_size)
    current_width, current_height = current_size
    if scale:
        width = current_width * scale
        height = current_height * scale
    elif width and not height:
        height = width / current_ratio
    elif height and not width:
        width = height * current_ratio
    return round(width), round(height)


def get_ratio(size):
    width, height = size
    return width / height


def get_path_for_save(original_path, new_dir, size_img):
    original_dir, original_name = os.path.split(path_to_img)
    root, ext = os.path.splitext(original_name)
    width, height = size_img
    new_name = '{0}__{1}x{2}{3}'.format(root, width, height, ext)
    if new_dir and not os.path.samefile(original_path, new_dir):
        return os.path.join(new_dir, original_name)
    return os.path.join(original_dir, new_name)


if __name__ == '__main__':
    args = get_args()
    check_args(args)
    path_to_img = args.path_to_img
    dir_for_save = args.output
    image = Image.open(path_to_img)
    size_for_new_file = get_size_for_new_img(image.size, args)
    if get_ratio(image.size) != get_ratio(size_for_new_file):
        print('A new proportion of the image is different from the original')
    resize_img = image.resize(size_for_new_file)
    path_for_save = get_path_for_save(path_to_img, dir_for_save, size_for_new_file)
    resize_img.save(path_for_save)
