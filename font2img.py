from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import os
import numpy as np
import pathlib
import argparse
from fontTools.ttLib import TTFont

parser = argparse.ArgumentParser(description="Obtaining characters from .ttf")
parser.add_argument(
    "--ttf_path", type=str, default="../ttf_folder", help="ttf directory"
)
parser.add_argument("--chara", type=str, default="../chara.txt", help="characters")
parser.add_argument(
    "--save_path", type=str, default="../save_folder", help="images directory"
)
parser.add_argument("--img_size", type=int, help="The size of generated images")
parser.add_argument("--chara_size", type=int, help="The size of generated characters")
args = parser.parse_args()

file_object = open(args.chara, encoding="utf-8")
try:
    characters = file_object.read()
finally:
    file_object.close()


def draw_single_char(ch, font, canvas_size, x_offset, y_offset):
    img = Image.new("RGB", (canvas_size, canvas_size), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((x_offset, y_offset), ch, (0, 0, 0), font=font)
    return img


def draw_example(ch, src_font, canvas_size, x_offset, y_offset):
    src_img = draw_single_char(ch, src_font, canvas_size, x_offset, y_offset)
    example_img = Image.new("RGB", (canvas_size, canvas_size), (255, 255, 255))
    example_img.paste(src_img, (0, 0))
    return example_img


data_dir = args.ttf_path
data_root = pathlib.Path(data_dir)
print(data_root)

all_image_paths = list(data_root.glob("*.ttf*")) + list(data_root.glob("*.ttc*"))
all_image_paths = [pathlib.Path(path) for path in all_image_paths]
print(len(all_image_paths))
for i in range(len(all_image_paths)):
    print(all_image_paths[i])

for label, item in zip(range(len(all_image_paths)), all_image_paths):
    family_index = -1
    while True:
        family_index += 1
        try:
            src_font = ImageFont.truetype(
                str(item), size=args.chara_size, index=family_index
            )
            src_font_TTF = TTFont(str(item), fontNumber=family_index)
        except OSError:
            break
        cmap = src_font_TTF.getBestCmap()
        if cmap is None:
            continue
        cmap = list(cmap)
        flag = False
        for character in characters:
            if ord(character) not in cmap:
                print(
                    "Missing character %s in %s (%s)" % (character, item, family_index)
                )
                flag = True
                break
        if flag:
            continue
        for chara, cnt in zip(characters, range(len(characters))):
            img = draw_example(
                chara,
                src_font,
                args.img_size,
                (args.img_size - args.chara_size) / 2,
                (args.img_size - args.chara_size) / 2,
            )
            file_suffix = "" if item.suffix == ".ttf" else "_%d" % family_index
            path_full = os.path.join(args.save_path, "id_%d%s" % (label, file_suffix))
            if not os.path.exists(path_full):
                os.mkdir(path_full)
            img.save(os.path.join(path_full, "%04d.png" % (cnt)))
        print(
            "Finish %s (%s) %s"
            % (
                src_font_TTF["name"].names[1],
                family_index,
                pathlib.Path(path_full).name,
            )
        )
