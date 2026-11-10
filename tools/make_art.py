"""Draws the profile's pixel art into assets/: python3 tools/make_art.py

Everything is drawn here with a built-in 5x7 font, so no fonts or images are needed. Each picture is a PNG
inside an SVG, and the SVG adds the animation on top (stars, campfire, cursor).
To change a text, edit it below and run the script again.
"""
import base64, math, random, struct, zlib
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
SCALE = 3  # screen pixels per art pixel

# Palette: a dark night with cream ink and greens.
BG = (16, 18, 14)
PANEL = (24, 28, 21)
INK = (233, 228, 200)
INK2 = (168, 164, 138)
DIM = (96, 98, 80)
G1 = (140, 198, 63)
G2 = (88, 150, 48)
G3 = (44, 92, 34)
G4 = (24, 52, 22)
SKY1 = (12, 16, 26)
SKY2 = (30, 52, 66)
MOUNT = (46, 66, 74)
MOUNT2 = (34, 50, 56)
WOOD = (92, 62, 38)
FIRE = (240, 170, 60)
FIRE2 = (220, 90, 40)

FONT = {
    "A": [" ### ", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"],
    "B": ["#### ", "#   #", "#   #", "#### ", "#   #", "#   #", "#### "],
    "C": [" ### ", "#   #", "#    ", "#    ", "#    ", "#   #", " ### "],
    "D": ["#### ", "#   #", "#   #", "#   #", "#   #", "#   #", "#### "],
    "E": ["#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#####"],
    "F": ["#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#    "],
    "G": [" ### ", "#   #", "#    ", "# ###", "#   #", "#   #", " ####"],
    "H": ["#   #", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"],
    "I": [" ### ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "],
    "J": ["  ###", "   # ", "   # ", "   # ", "   # ", "#  # ", " ##  "],
    "K": ["#   #", "#  # ", "# #  ", "##   ", "# #  ", "#  # ", "#   #"],
    "L": ["#    ", "#    ", "#    ", "#    ", "#    ", "#    ", "#####"],
    "M": ["#   #", "## ##", "# # #", "# # #", "#   #", "#   #", "#   #"],
    "N": ["#   #", "#   #", "##  #", "# # #", "#  ##", "#   #", "#   #"],
    "O": [" ### ", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "],
    "P": ["#### ", "#   #", "#   #", "#### ", "#    ", "#    ", "#    "],
    "Q": [" ### ", "#   #", "#   #", "#   #", "# # #", "#  # ", " ## #"],
    "R": ["#### ", "#   #", "#   #", "#### ", "# #  ", "#  # ", "#   #"],
    "S": [" ####", "#    ", "#    ", " ### ", "    #", "    #", "#### "],
    "T": ["#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  "],
    "U": ["#   #", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "],
    "V": ["#   #", "#   #", "#   #", "#   #", "#   #", " # # ", "  #  "],
    "W": ["#   #", "#   #", "#   #", "# # #", "# # #", "# # #", " # # "],
    "X": ["#   #", "#   #", " # # ", "  #  ", " # # ", "#   #", "#   #"],
    "Y": ["#   #", "#   #", " # # ", "  #  ", "  #  ", "  #  ", "  #  "],
    "Z": ["#####", "    #", "   # ", "  #  ", " #   ", "#    ", "#####"],
    "0": [" ### ", "#   #", "#  ##", "# # #", "##  #", "#   #", " ### "],
    "1": ["  #  ", " ##  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "],
    "2": [" ### ", "#   #", "    #", "   # ", "  #  ", " #   ", "#####"],
    "3": ["#### ", "    #", "    #", " ### ", "    #", "    #", "#### "],
    "4": ["   # ", "  ## ", " # # ", "#  # ", "#####", "   # ", "   # "],
    "5": ["#####", "#    ", "#### ", "    #", "    #", "#   #", " ### "],
    "6": [" ### ", "#    ", "#    ", "#### ", "#   #", "#   #", " ### "],
    "7": ["#####", "    #", "   # ", "  #  ", " #   ", " #   ", " #   "],
    "8": [" ### ", "#   #", "#   #", " ### ", "#   #", "#   #", " ### "],
    "9": [" ### ", "#   #", "#   #", " ####", "    #", "    #", " ### "],
    " ": ["     "] * 7,
    ".": ["     "] * 6 + ["  #  "],
    ",": ["     "] * 5 + ["  #  ", " #   "],
    ":": ["     ", "     ", "  #  ", "     ", "     ", "  #  ", "     "],
    "/": ["    #", "    #", "   # ", "  #  ", " #   ", "#    ", "#    "],
    "-": ["     ", "     ", "     ", " ### ", "     ", "     ", "     "],
    "_": ["     "] * 6 + ["#####"],
    ">": ["#    ", " #   ", "  #  ", "   # ", "  #  ", " #   ", "#    "],
    "<": ["    #", "   # ", "  #  ", " #   ", "  #  ", "   # ", "    #"],
    "!": ["  #  "] * 5 + ["     ", "  #  "],
    "?": [" ### ", "#   #", "    #", "   # ", "  #  ", "     ", "  #  "],
    "'": ["  #  ", "  #  "] + ["     "] * 5,
    "(": ["   # ", "  #  ", " #   ", " #   ", " #   ", "  #  ", "   # "],
    ")": [" #   ", "  #  ", "   # ", "   # ", "   # ", "  #  ", " #   "],
    "+": ["     ", "  #  ", "  #  ", "#####", "  #  ", "  #  ", "     "],
    "@": [" ### ", "#   #", "# ###", "# # #", "# ###", "#    ", " ####"],
    "&": [" ##  ", "#  # ", "#  # ", " ##  ", "# # #", "#  # ", " ## #"],
    "*": ["     ", "# # #", " ### ", "#####", " ### ", "# # #", "     "],
    "=": ["     ", "     ", "#####", "     ", "#####", "     ", "     "],
    "~": ["     ", "     ", " #   ", "# # #", "   # ", "     ", "     "],
    "%": ["##   ", "##  #", "   # ", "  #  ", " #   ", "#  ##", "   ##"],
    "|": ["  #  "] * 7,
    "·": ["     ", "     ", "     ", "  #  ", "     ", "     ", "     "],
}
BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


class Canvas:
    def __init__(self, w, h, fill=BG):
        self.w, self.h = w, h
        self.px = [[fill] * w for _ in range(h)]

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.px[y][x] = c

    def rect(self, x, y, w, h, c):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, c)

    def frame(self, x, y, w, h, c):
        self.rect(x, y, w, 1, c)
        self.rect(x, y + h - 1, w, 1, c)
        self.rect(x, y, 1, h, c)
        self.rect(x + w - 1, y, 1, h, c)

    def text(self, x, y, s, c, size=1, shadow=None):
        if shadow:
            self.text(x + size, y + size, s, shadow, size)
        for i, ch in enumerate(s.upper()):
            for row, line in enumerate(FONT.get(ch, FONT["?"])):
                for col, bit in enumerate(line):
                    if bit == "#":
                        self.rect(x + (i * 6 + col) * size, y + row * size, size, size, c)
        return x + len(s) * 6 * size

    def dither(self, x, y, c1, c2, t):
        """c2 where t (0..1) beats the Bayer threshold, so gradients come out as an ordered dither."""
        self.set(x, y, c2 if t * 16 > BAYER[y % 4][x % 4] + 0.5 else c1)

    def png(self):
        rows = b""
        for line in self.px:
            row = b"".join(bytes(c) * SCALE for c in line)
            rows += (b"\x00" + row) * SCALE

        def chunk(kind, data):
            return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))

        w, h = self.w * SCALE, self.h * SCALE
        return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
                + chunk(b"IDAT", zlib.compress(rows, 9)) + chunk(b"IEND", b""))


def hexc(c):
    return "#%02x%02x%02x" % c


def svg(name, canvas, overlay="", style=""):
    """Writes the canvas as a PNG inside an SVG, with animated overlay rects in art pixels."""
    w, h = canvas.w * SCALE, canvas.h * SCALE
    data = base64.b64encode(canvas.png()).decode()
    (OUT / name).write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{w}" height="{h}" viewBox="0 0 {w} {h}" shape-rendering="crispEdges">'
        f"<style>{style}</style>"
        f'<image width="{w}" height="{h}" xlink:href="data:image/png;base64,{data}"/>'
        f'<g transform="scale({SCALE})">{overlay}</g></svg>')


def px(x, y, c, cls="", w=1, h=1, delay=0):
    d = f' style="animation-delay:{delay}s"' if delay else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{hexc(c)}" class="{cls}"{d}/>'


def window(c, x, y, w, h, title, menu=None):
    """A retro OS window: cream title bar with buttons, optional menu bar, cream border."""
    c.rect(x, y, w, h, PANEL)
    c.frame(x, y, w, h, INK)
    c.rect(x, y, w, 11, INK)
    c.text(x + 4, y + 2, title, BG)
    for i, b in enumerate(["_", "+", "X"]):
        bx = x + w - 30 + i * 9
        c.frame(bx, y + 2, 7, 7, BG)
        if b == "X":
            for k in range(3):
                c.set(bx + 2 + k, y + 4 + k, BG)
                c.set(bx + 4 - k, y + 4 + k, BG)
        elif b == "_":
            c.rect(bx + 2, y + 6, 3, 1, BG)
        else:
            c.frame(bx + 2, y + 4, 3, 3, BG)
    if menu:
        mx = x + 4
        for item in menu:
            mx = c.text(mx, y + 13, item, INK2) + 8
        c.rect(x, y + 21, w, 1, INK)
        return y + 22
    return y + 11


def pine(c, x, base, h, rnd):
    top = base - h
    c.rect(x, base - 2, 1, 3, WOOD)
    for t in range(3):
        y0 = top + t * h // 4
        th = h // 3 + 1
        for r in range(th):
            hw = (r * (t + 2)) // 4
            for xx in range(x - hw, x + hw + 1):
                col = G2 if xx == x - hw else (G4 if xx == x + hw else G3)
                if col == G3 and rnd.random() < 0.08:
                    col = G2
                c.set(xx, y0 + r, col)


def header():
    rnd = random.Random(4)
    c = Canvas(300, 150)
    top = window(c, 0, 0, 300, 150, "REASONSX.EXE", ["FILE", "PARTY", "QUESTS", "INVENTORY", "HELP"])
    sx, sy, sw, sh = 1, top, 298, 150 - top - 1
    ground = sy + sh

    for y in range(sy, ground):
        for x in range(sx, sx + sw):
            c.dither(x, y, SKY1, SKY2, (y - sy) / sh * 1.1)
    stars = []
    for _ in range(70):
        x, y = rnd.randrange(sx, sx + sw), rnd.randrange(sy, sy + 80)
        c.set(x, y, INK2 if rnd.random() < 0.3 else DIM)
        stars.append((x, y))

    mx, my = 252, sy + 18  # moon
    for y in range(-8, 9):
        for x in range(-8, 9):
            d = math.hypot(x, y)
            if d <= 8:
                c.set(mx + x, my + y, INK if d < 7 or (x + y) % 2 else INK2)
    for cx, cy, r in [(-3, -2, 2), (3, 3, 1.5), (2, -4, 1)]:
        for y in range(-2, 3):
            for x in range(-2, 3):
                if math.hypot(x, y) <= r:
                    c.set(mx + cx + x, my + cy + y, INK2)

    for x in range(sx, sx + sw):  # far mountains with snow caps, then near hills
        hgt = 32 + 12 * math.sin(x / 23) + 7 * math.sin(x / 9 + 1) + 4 * math.sin(x / 4.3)
        peak = ground - int(hgt)
        for y in range(peak, ground):
            c.dither(x, y, MOUNT, MOUNT2, (y - peak) / 30)
            if y - peak < 2 and hgt > 42:
                c.set(x, y, INK2)
        hill = ground - int(14 + 5 * math.sin(x / 17 + 2) + 3 * math.sin(x / 7))
        for y in range(hill, ground):
            c.dither(x, y, G4, G3, (y - hill) / 22)

    for x in range(sx, sx + sw, 1):  # forest, back row then front row
        if rnd.random() < 0.12 and not 108 < x < 210:
            pine(c, x, ground - 6 - rnd.randrange(4), rnd.randrange(12, 20), rnd)
    for x in range(sx + 2, sx + sw, 1):
        if rnd.random() < 0.08 and not 120 < x < 205:
            pine(c, x, ground, rnd.randrange(16, 28), rnd)
    for x in range(sx, sx + sw):
        for y in range(ground - 4, ground):
            c.dither(x, y, G3, G2, 0.35 if rnd.random() < 0.5 else 0.1)

    tx, ty = 150, ground - 2  # tent
    for r in range(16):
        for x in range(tx - r, tx + r + 1):
            c.set(x, ty - 16 + r, INK if x < tx + r - 1 else INK2)
        if r > 6:
            c.rect(tx - (r - 6) // 2, ty - 16 + r, (r - 6) // 2 + 1, 1, BG)
    c.rect(tx, ty - 17, 1, 2, WOOD)
    fx, fy = 186, ground - 2  # campfire logs
    c.rect(fx - 5, fy, 11, 1, WOOD)
    c.rect(fx - 4, fy - 1, 9, 1, WOOD)
    for x in range(fx - 5, fx + 6):
        c.set(x, fy + 1, DIM)

    c.text(12, sy + 8, "KAMIL", INK, 4, shadow=BG)
    c.text(14, sy + 42, "FULL-STACK DEVELOPER", G1, 1, shadow=BG)
    c.text(14, sy + 52, "WEB DEV GRADUATE · DENMARK", INK2, 1, shadow=BG)
    end = c.text(14, sy + 62, "> @REASONSX", INK, 1, shadow=BG)

    o = "".join(px(x, y, INK, "tw", delay=round(rnd.uniform(0, 4), 2)) for x, y in rnd.sample(stars, 14))
    flame = [(dx, dy, FIRE2 if dy > -4 or abs(dx) > 1 else FIRE) for dy in range(-2, -9, -1)
             for dx in range(-3 + (-dy) // 3, 4 - (-dy) // 3)]
    o += "".join(px(fx + dx, fy + dy, col, "f1" if i % 2 else "f2") for i, (dx, dy, col) in enumerate(flame))
    o += px(fx + 1, fy - 7, FIRE, "f2") + px(fx - 1, fy - 8, FIRE2, "f1")
    o += px(end + 3, sy + 62, G1, "cur", w=5, h=7)
    o += f'<rect class="shoot" x="40" y="{sy + 6}" width="6" height="1" fill="{hexc(INK)}"/>'
    style = (".tw{animation:tw 4s steps(1) infinite}@keyframes tw{0%,60%{opacity:1}70%{opacity:.1}80%{opacity:1}}"
             ".f1{animation:f 0.6s steps(1) infinite}.f2{animation:f 0.6s steps(1) infinite reverse}"
             "@keyframes f{0%{opacity:1}50%{opacity:0}}"
             ".cur{animation:f 1s steps(1) infinite}"
             ".shoot{opacity:0;animation:sh 9s linear infinite}"
             "@keyframes sh{0%,88%{opacity:0;transform:translate(0,0)}89%{opacity:1}96%{opacity:0;transform:translate(70px,18px)}100%{opacity:0}}")
    svg("header.svg", c, o, style)


def bar(c, x, y, value, total=6):
    for i in range(total):
        c.rect(x + i * 7, y, 6, 6, G1 if i < value else G4)
        if i >= value:
            c.frame(x + i * 7, y, 6, 6, G3)


def sheet():
    c = Canvas(300, 168)
    # Character
    y = window(c, 0, 0, 132, 168, "CHARACTER") + 6
    c.text(6, y, "KAMIL", G1, 2)
    c.text(6, y + 17, "@REASONSX", INK2)
    rows = [("CLASS", "FULL-STACK"), ("TITLE", "WEB DEV GRAD"), ("HOME", "DENMARK"), ("MORALE", "EXCELLENT")]
    for i, (k, v) in enumerate(rows):
        c.text(6, y + 31 + i * 10, k, DIM)
        c.text(48, y + 31 + i * 10, v, G1 if k == "MORALE" else INK)
    sy = y + 74
    c.rect(1, sy, 130, 1, INK)
    c.text(6, sy + 4, "STATS", INK)
    stats = [("FRONTEND", 5), ("BACKEND", 4), ("SECURITY", 3), ("UX/UI", 4), ("COFFEE", 6)]
    for i, (k, v) in enumerate(stats):
        c.text(6, sy + 15 + i * 10, k, INK2)
        bar(c, 66, sy + 15 + i * 10, v)

    # Quest log
    y = window(c, 136, 0, 164, 116, "QUEST LOG") + 6
    c.text(142, y, "ACTIVE", G1)
    c.text(142, y + 11, "> AUTH SERVER", INK)
    for i, line in enumerate(["OAUTH2 / OIDC LOGIN ON", "SPRING AUTHORIZATION", "SERVER: LOGIN PAGES,", "USER SYNC, PASSWORD", "RESET, WELCOME EMAILS."]):
        c.text(148, y + 22 + i * 9, line, INK2)
    c.text(142, y + 70, "COMPLETED", DIM)
    c.text(142, y + 81, "+ WEB DEV DEGREE", INK)
    c.frame(250, y + 79, 44, 11, G1)
    c.text(254, y + 81, "LVL UP", G1)

    # Gear
    y = window(c, 136, 120, 164, 48, "GEAR") + 4
    gear = [("HAND-L", "ANGULAR"), ("HAND-R", "SPRING BOOT"), ("ARMOR", "SPRING SECURITY")]
    for i, (k, v) in enumerate(gear):
        c.text(142, y + i * 10, k, DIM)
        c.text(184, y + i * 10, v, INK)

    o = px(142 + 6 * 13 + 3, 17 + 11, G1, "cur", w=5, h=7)  # cursor after "> AUTH SERVER"
    svg("sheet.svg", c, o, ".cur{animation:f 1s steps(1) infinite}@keyframes f{0%{opacity:1}50%{opacity:0}}")


def footer():
    rnd = random.Random(9)
    c = Canvas(300, 34)
    for y in range(34):
        for x in range(300):
            c.dither(x, y, BG, G4, max(0, (y - 14) / 22))
    for x in range(2, 298):
        if rnd.random() < 0.1:
            pine(c, x, 33, rnd.randrange(8, 16), rnd)
    c.rect(0, 33, 300, 1, G3)
    svg("footer.svg", c)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    header()
    sheet()
    footer()
    for f in sorted(OUT.glob("*.svg")):
        print(f.name, f.stat().st_size // 1024, "KB")
