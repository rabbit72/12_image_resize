import argparse
import os.path
from PIL import Image


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'img',
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

    args = vars(parser.parse_args())
    check_args(args)
    return args


def check_path_to_img(path_to_picture):
    available_ext = ['jpg', 'jpeg', 'bmp', 'png']
    if not os.path.isfile(path_to_picture):
        raise FileNotFoundError('Incorrect path to image')
    ext = os.path.splitext(path_to_picture)[1].lstrip('.')
    if ext not in available_ext:
        raise RuntimeError("Unsupported image's ext: {0}".format(ext))


def check_dir_for_save(path_for_save):
    if path_for_save and not os.path.isdir(path_for_save):
        raise FileNotFoundError('Incorrect path for save')


def check_args(args):
    check_path_to_img(args['img'])
    check_dir_for_save(args['output'])
    width, height, scale = args['width'], args['height'], args['scale']
    if scale and (width or height):
        raise argparse.ArgumentError(
            None,
            'Сan not use "scale" with "width" or "height"'
        )
    for number in (width, height, scale):
        if number and number <= 0:
            raise ValueError('Value can not be <= 0')


def get_required_size(current_size, raw_size):
    if not any(raw_size):
        return current_size
    width, height, scale = raw_size
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
    path_to_img = args['img']
    dir_for_save = args['output']
    raw_size = args['width'], args['height'], args['scale']
    image = Image.open(path_to_img)
    required_size = get_required_size(image.size, raw_size)
    if get_ratio(image.size) != get_ratio(required_size):
        print('A new proportion of the image is different from the original')
    resize_img = image.resize(required_size)
    path_for_save = get_path_for_save(path_to_img, dir_for_save, required_size)
    resize_img.save(path_for_save)
