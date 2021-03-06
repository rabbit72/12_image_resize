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
        type=positive_int,
        help='Required image width'

    )
    parser.add_argument(
        '--height',
        type=positive_int,
        help='Required image height'
    )
    parser.add_argument(
        '--scale',
        type=positive_float,
        help='Required scale image'
    )
    parser.add_argument(
        '--output',
        help='Directory for new picture'
    )
    return parser.parse_args()


def positive_int(arg):
    if not isinstance(arg, int) and int(arg) <= 0:
        raise argparse.ArgumentTypeError
    return int(arg)


def positive_float(arg):
    if not isinstance(arg, float) and float(arg) <= 0:
        raise argparse.ArgumentTypeError
    return float(arg)


def check_args(args):
    if not os.path.isfile(args.path_to_img):
        return 'Incorrect path to image'
    elif args.output and not os.path.isdir(args.output):
        return 'Incorrect path for save'
    elif not any((args.width, args.height, args.scale)):
        return 'No resizing specified'
    elif args.scale and (args.width or args.height):
        return 'Сan not use "scale" with "width" or "height"'


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
    original_dir, original_name_with_ext = os.path.split(original_path)
    name, ext = os.path.splitext(original_name_with_ext)
    width, height = size_img
    new_name = '{0}__{1}x{2}{3}'.format(name, width, height, ext)
    if new_dir and not os.path.samefile(original_dir, new_dir):
        return os.path.join(new_dir, original_name_with_ext)
    return os.path.join(original_dir, new_name)


if __name__ == '__main__':
    args = get_args()
    error = check_args(args)
    if error:
        exit(error)
    path_to_img = args.path_to_img
    dir_for_save = args.output
    image = Image.open(path_to_img)
    size_for_new_file = get_size_for_new_img(image.size, args)
    if get_ratio(image.size) != get_ratio(size_for_new_file):
        print('A new proportion of the image is different from the original')
    resized_img = image.resize(size_for_new_file)
    path_for_save = get_path_for_save(path_to_img, dir_for_save, size_for_new_file)
    resized_img.save(path_for_save)
