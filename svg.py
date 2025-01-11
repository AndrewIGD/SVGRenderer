import os
import sys

from drawer.drawer import SVGConfig
from parser.parser import parse_svg

def main():
    """
    Renders an svg file to png format in the same folder as the svg file.

    Args:
        svg_file (str): Path to target svg file
        ppm (int): pixels per millimeter. Higher values yield higher resolutions. Default = 1

    Raises:
        Exception: If svg_file does not exist
        ValueError: If ppm is not an integer
    """

    if len(sys.argv) < 2 or len(sys.argv) > 3:
        raise Exception("Usage: svg.py <svg_file> or svg.py <svg_file> <ppm>")

    svg_path = sys.argv[1]
    if not os.path.isfile(svg_path):
        raise Exception("File not found")

    pixels_per_mm = 1
    if len(sys.argv) == 3:
        try:
            pixels_per_mm = int(sys.argv[2])
        except ValueError:
            raise ValueError("Invalid ppm type")

    svg = parse_svg(svg_path, SVGConfig(pixels_per_mm=pixels_per_mm))

    image = svg.get_image()

    filename, ext = os.path.splitext(svg_path)
    image.save(filename + ".png", "PNG")

if __name__ == '__main__':
    main()