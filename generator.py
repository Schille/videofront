#!/usr/bin/env python3

import os
import argparse
import re
import shutil
import sys
import pathlib

import jinja2


def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")


parser = argparse.ArgumentParser(description='Gallery generator script.')
parser.add_argument("--assets", "-a", type=dir_path, default="./assets",
                    help="path to the asset directory")
parser.add_argument("--background-scroll", "-b", type=bool, default=True,
                    help="Generate scrollable background")


templateEnv = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="./"))
TEMPLATE_FILE = "templates/gallery.html"
OUTPUT_DIR = "build"

class Item:
    def __init__(self, title, path):
        self._raw_title = title
        self.path = path

    @property
    def title(self):
        return re.sub(r"(\.(.*))|([^a-zA-ZäÄüÜöÖ0-9_\- ]|([0-9]*\_))", "", self._raw_title)

    @property
    def slug(self):
        return re.sub(r"(\.(.*))|([0-9]*[\W])", "", self._raw_title)


class Video(Item):
    pass


class ItemCollection(Item):

    def __init__(self, title, path, _items):
        super(ItemCollection, self).__init__(title, path)
        self._items = _items

    @property
    def items(self):
        return self._items


class Diashow(ItemCollection):
    pass


class Category(ItemCollection):
    pass


def sort_by_prefix(collection):

    def _get_key(x):
        if type(x) is tuple:
            try:
                return int(x[0].split("_")[0])
            except ValueError:
                return -1
        else:
            try:
                return int(x.split("_")[0])
            except ValueError:
                return -1

    return sorted(collection, key=_get_key)


def get_assets(path):
    assets = []
    root = path.rstrip(os.sep)

    for _i in sort_by_prefix(os.listdir(root)):
        # categories
        cpath = os.path.join(root, _i)
        _items = []
        if os.path.isdir(cpath):
            # get items
            for k in sort_by_prefix(os.listdir(cpath)):
                dpath = os.path.join(cpath, k)
                if os.path.isdir(dpath):
                    _items.append(Diashow(k, path=dpath, _items=[os.path.join(dpath, s)
                                                                 for s in sort_by_prefix(os.listdir(dpath))]))
                else:
                    _items.append(Video(k, path=dpath))
            assets.append(Category(title=_i, path=cpath, _items=_items))
    return assets


if __name__ == "__main__":
    args = parser.parse_args()
    categories_and_items = get_assets(args.assets)
    if not categories_and_items:
        print("The asset directory seems to be empty.")
        sys.exit(-1)
    # render the template
    template = templateEnv.get_template(TEMPLATE_FILE)
    output_html = template.render(items=categories_and_items)

    base_dir = pathlib.Path(__file__).parent.resolve()
    build_dir = os.path.join(base_dir, OUTPUT_DIR)
    try:
        shutil.rmtree(build_dir)
    except FileNotFoundError:
        pass
    os.mkdir(build_dir)
    with open(os.path.join(build_dir, "index.html"), "w") as f:
        f.write(output_html)
    shutil.copytree(os.path.join(base_dir, "templates/src"), os.path.join(build_dir, "src"))
