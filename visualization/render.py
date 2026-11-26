"""Build the teaching GIF and offline explorer archive."""

import argparse
from fractions import Fraction
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from PIL import Image, ImageDraw, ImageFont

SIZE = (704, 826)
PAPER = '#f4f7fa'
INK = '#17283f'
MUTED = '#435977'
LANES = ('Capped arc u', 'Flag f1', 'Flag f2', 'Bypass')
PALETTES = ('#007867', '#0b65aa', '#7a3ea1', '#a64b25')
FONT = '/System/Library/Fonts/Supplemental/Arial{}.ttf'


def text(draw, value, xy, size, *, color=INK, bold=False, anchor=None):
    font = ImageFont.truetype(FONT.format(' Bold' if bold else ''), size)
    bounds = draw.textbbox(xy, value, font=font, anchor=anchor)
    assert bounds[0] >= 0 and bounds[1] >= 0 and bounds[2] < SIZE[0] and bounds[3] < SIZE[1], (value, bounds)
    draw.text(xy, value, font=font, fill=color, anchor=anchor)


def frame(mode, portion):
    image = Image.new('RGB', SIZE, PAPER)
    draw = ImageDraw.Draw(image)
    text(draw, 'Two routes can tie', (38, 28), 50, bold=True)
    text(draw, 'One unit of flow from s to t', (41, 93), 30, color=MUTED)
    draw.rounded_rectangle((39, 151, 665, 589), radius=19, fill='white', outline='#d1dce9', width=2)
    half = Fraction(1, 2)
    costs, flows, state, line_a, line_b = {
        'tied': ((1, 2, 2, 3), (half, portion, half - portion, 0), 'Equal flag costs',
                 'The leftover 1/2 can switch flags.', 'That exchange adds one direction.'),
        'ordered': ((1, 2, Fraction(5, 2), 3), (half, half, 0, 0), 'Flag f1 is cheaper',
                    'All leftover flow uses f1.', 'The exchange direction disappears.'),
        'bypass': ((1, 2, 2, half), (0, 0, 0, 1), 'Bypass is cheapest',
                   'Neither flag carries flow.', 'Equal flag prices alone add nothing.'),
    }[mode]
    text(draw, 'Arc and cost', (169, 170), 24, bold=True)
    text(draw, 'Flow', (510, 170), 24, bold=True)
    for i, (name, price, amount, color) in enumerate(zip(LANES, costs, flows, PALETTES)):
        y = 255 + 85 * i
        line_color = color if amount else '#bac9d9'
        draw.line(((89, 390), (166, y), (538, y), (615, 390)), fill=line_color,
                  width=8 if amount else 4, joint='curve')
        draw.polygon(((525, y - 9), (543, y), (525, y + 9)), fill=line_color)
        text(draw, f'{name} · {price}', (167, y - 42), 28, bold=True, color=color)
        text(draw, str(amount), (501, y - 42), 29, bold=True, color=INK if amount else MUTED)
    for x, label in ((89, 's'), (615, 't')):
        draw.ellipse((x - 19, 371, x + 19, 409), fill=INK)
        text(draw, label, (x, 390), 24, color='white', bold=True, anchor='mm')
    text(draw, 'Capacity on u is 1/2.', (42, 608), 31, color=MUTED)
    text(draw, state, (42, 670), 40, bold=True)
    text(draw, line_a, (42, 728), 30, color=MUTED)
    text(draw, line_b, (42, 772), 30, color=MUTED)
    return image.quantize(colors=96, method=Image.Quantize.MEDIANCUT)


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=here)
    out = parser.parse_args().output
    out.mkdir(parents=True, exist_ok=True)
    stops = [('tied', Fraction(i, 16), 1800 if i in {0, 8} else 160) for i in range(8, -1, -1)]
    stops.extend([('ordered', Fraction(0), 2500), ('bypass', Fraction(0), 2300)])
    frames = [frame(mode, portion) for mode, portion, _ in stops]
    frames[0].save(out / 'flow-measurements.gif', save_all=True, append_images=frames[1:],
                   duration=[delay for _, _, delay in stops], loop=0, optimize=True)
    entry = ZipInfo('index.html', (1980, 1, 1, 0, 0, 0))
    entry.external_attr = 0o100644 << 16
    with ZipFile(out / 'flow-measurements-explorer.zip', 'w') as archive:
        archive.writestr(entry, (here / 'index.html').read_bytes(), compress_type=ZIP_DEFLATED, compresslevel=9)


if __name__ == '__main__':
    main()
