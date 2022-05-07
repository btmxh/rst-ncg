import argparse
import pygame
import os
import traceback


paths = None


def parse_bg_color(bg):
    srcbg = bg
    if bg[0] != '#':
        raise Exception(f"Invalid color: {srcbg}")
    bg = bg[1:]
    if len(bg) == 3:
        bg = "".join([x+x for x in bg])
    if len(bg) != 6:
        raise Exception(f"Invalid color: {srcbg}")
    return tuple(int(bg[i:i+2], 16) for i in (0, 2, 4))


def load_img(ch):
    global paths
    if paths is None:
        paths = os.listdir("notes")

    for path in paths:
        (name, _) = os.path.splitext(path)
        rel_path = os.path.join("notes", path)
        if name == ch:
            try:
                img = pygame.image.load(rel_path)
                img.convert()
                return img
            except Exception:
                print(f"Warn: Unable to load image '{rel_path}' for char {ch}")
                traceback.print_exc()

    raise FileNotFoundError(f"Note image for char {ch} not found")


def main():
    parser = argparse.ArgumentParser(
        description="Re:Stage! Prism Step note color generator")
    parser.add_argument("colors", metavar="colors",
                        help="A string indicating the generated colors")
    parser.add_argument("output", metavar="output",
                        help="Output image file")
    parser.add_argument("-bg", "--background", default="#fff",
                        help="Background color, in web hex format, allow both short (#fff) and long (#ff0158) format")
    parser.add_argument("-pt", "--padding-top", default="2",
                        help="Top padding, the empty space will be filled by the background color")
    parser.add_argument("-pl", "--padding-left", default="3",
                        help="Left padding, the empty space will be filled by the background color")
    parser.add_argument("-pr", "--padding-right", default="3",
                        help="Right padding, the empty space will be filled by the background color")
    parser.add_argument("-pb", "--padding-bottom", default="3",
                        help="Bottom padding, the empty space will be filled by the background color")
    parser.add_argument("-s", "--spacing", default="0",
                        help="Spacing between notes")
    args = parser.parse_args()

    args.padding_top = int(args.padding_top)
    args.padding_left = int(args.padding_left)
    args.padding_right = int(args.padding_right)
    args.padding_bottom = int(args.padding_bottom)
    args.spacing = int(args.spacing)

    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    pygame.init()
    pygame.display.set_mode((1, 1))

    chars = set(args.colors)
    imgs = {ch: load_img(ch) for ch in chars}
    count = {ch: args.colors.count(ch) for ch in chars}
    width = sum([imgs[ch].get_width() * count[ch] for ch in chars]) \
        + args.padding_left + args.padding_right \
        + args.spacing * (len(args.colors) - 1)
    height = max([imgs[ch].get_height() for ch in chars])   \
        + args.padding_top + args.padding_bottom

    surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
    pygame.draw.rect(surface, parse_bg_color(
        args.background), (0, 0, width, height))

    x, y = args.padding_left, args.padding_top
    for ch in args.colors:
        img = imgs[ch]
        surface.blit(img, (x, y))
        x += img.get_width() + args.spacing

    pygame.image.save(surface, args.output)


if __name__ == "__main__":
    main()
