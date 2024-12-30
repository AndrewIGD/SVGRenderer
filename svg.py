import os

from drawer.drawer import SVGConfig
from parser.parser import parse_svg

def main():
    ##if len(sys.argv) != 2:
    ##    raise Exception("Usage: svg.py <svg_image>")

    ##svg_path = sys.argv[1]
    ##if not os.path.isfile(svg_path):
    ##    raise Exception("File not found")

    pixels_per_mm = 10

    svg_path = "temp/arc.svg"

    svg = parse_svg(svg_path, SVGConfig(pixels_per_mm=pixels_per_mm))

    image = svg.get_image()

    filename, ext = os.path.splitext(svg_path)
    image.save(filename + ".png", "PNG")

if __name__ == '__main__':
    main()