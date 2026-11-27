# THE WORLD — 26 November 2026
# Deterministic one-page newspaper image (1024x1024, <1 MiB) summarising
# the world news of Thursday 26 November 2026. Pure PIL, no network,
# no randomness, no timestamps: two runs produce byte-identical output.
# Headlines verified against Reuters, BBC, CNN, USTR, KCNA, Basarnas,
# dailysummaryof and Open Chronicle on 26-27 Nov 2026 (see brief-final).
# Bogor mine figures locked at 13 dead / 13 still trapped (BBC + Reuters,
# confirmed Thursday 26 Nov). Tariff rates are the PROPOSED Section 301
# caps (USTR, 25 Nov) — nothing is in effect yet.

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (17, 17, 17)
RED = (178, 34, 34)
GREY = (90, 86, 78)
RULE = (60, 58, 52)
LIGHT = (232, 226, 212)
BLUE = (28, 68, 128)
GOLD = (184, 134, 11)

FDIR = "/usr/share/fonts/truetype/dejavu"


def font(size, bold=False, serif=False):
    name = "DejaVuSerif-Bold.ttf" if (serif and bold) else \
           "DejaVuSerif.ttf" if serif else \
           "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(FDIR, name), size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, fill=INK):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def kicker(draw, x, y, text, size=15):
    f = font(size, bold=True)
    draw.text((x, y), text.upper(), font=f, fill=RED)
    return y + size + 6


def hline(draw, x0, x1, y, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def headline(draw, x, y, text, size, max_w, leading=None, serif=True):
    f = font(size, bold=True, serif=serif)
    lead = leading or int(size * 1.12)
    return para(draw, x, y, text, f, max_w, lead)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 26                      # margin
    R = W - M                   # right edge

    # ---- frame ----
    d.rectangle([10, 10, W - 11, H - 11], outline=RULE, width=3)
    d.rectangle([16, 16, W - 17, H - 17], outline=RULE, width=1)

    # ---- masthead ----
    title = "THE WORLD"
    tf = font(76, bold=True, serif=True)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 26), title, font=tf, fill=INK)
    hline(d, M, R, 116, width=3)
    hline(d, M, R, 121, width=1)
    df = font(16, bold=True)
    d.text((M, 130), "THURSDAY, 26 NOVEMBER 2026", font=df, fill=INK)
    right = "WORLD NEWS IN ONE IMAGE"
    d.text((R - d.textlength(right, font=df), 130), right, font=df, fill=INK)
    d.text((M, 152), "No. 330  ·  Price: One Read  ·  Printed in pixels, not paper",
           font=font(13), fill=GREY)
    hline(d, M, R, 176, width=2)

    # ================= LEAD (left) =================
    lx, lw = M, 612
    y = 192
    y = kicker(d, lx, y, "Trade war — proposed, not yet law")
    y = headline(d, lx, y, "TRUMP'S NEW TARIFFS HIT 14 ECONOMIES", 36, lw)
    y += 6
    y = para(d, lx, y,
             "Washington proposes Section 301 tariffs on 14 trading partners "
             "— about half of the world economy. Nothing is in effect yet: "
             "public comments are due 5 January, hearings open 25 January.",
             font(16), lw, 20)
    y += 8
    # grouped bar chart of proposed top rates
    d.text((lx, y), "PROPOSED TOP RATES", font=font(13, bold=True), fill=GREY)
    y += 18
    bars = [
        ("Vietnam", 35, "35%"),
        ("India", 25, "25%"),
        ("China & Singapore", 20, "20%  *"),
        ("Indonesia, Malaysia, Thailand, Bangladesh, Cambodia", 18, "18%"),
        ("EU, Japan, S. Korea, Switzerland, Taiwan", 15, "15%"),
    ]
    bx0, bw = lx + 8, 430
    for label, val, shown in bars:
        d.text((bx0, y), label, font=font(12), fill=INK)
        d.rectangle([bx0, y + 14, bx0 + bw, y + 23], outline=RULE, width=1)
        d.rectangle([bx0 + 1, y + 15, bx0 + 1 + int((bw - 2) * val / 35.0),
                     y + 22], fill=RED)
        d.text((bx0 + bw + 8, y + 12), shown, font=font(13, bold=True), fill=INK)
        y += 26
    d.text((lx, y + 2), "* China rises to 40% if the trade-truce talks fail.",
           font=font(12), fill=GREY)

    # ================= GULF (right) =================
    gx, gw = 664, R - 664
    y = 192
    y = kicker(d, gx, y, "Gulf in flames — day two")
    y = headline(d, gx, y, "HOUTHIS CLAIM SAUDI'S BIGGEST REFINERY HIT", 30, gw)
    y += 4
    y = para(d, gx, y,
             "Houthis claim drones hit Ras Tanura — Saudi Arabia's largest "
             "refinery, 550,000 barrels a day. Satellite images show thick "
             "black smoke over the plant.",
             font(15), gw, 20)
    # refinery visual: towers + smoke plume
    vx, vy, vw, vh = gx, y + 6, gw, 80
    d.rectangle([vx, vy, vx + vw, vy + vh], fill=(223, 216, 200),
                outline=RULE, width=1)
    base = vy + vh - 14
    for tx, th in [(vx + 24, 52), (vx + 58, 66), (vx + 96, 44),
                   (vx + 132, 60), (vx + 168, 48)]:
        d.rectangle([tx, base - th, tx + 16, base], fill=(70, 66, 60))
        d.rectangle([tx + 4, base - th - 8, tx + 12, base - th], fill=(70, 66, 60))
    d.rectangle([vx + 196, base - 34, vx + 214, base], fill=(70, 66, 60))
    # smoke puffs
    for cx, cy, r in [(vx + 66, vy + 22, 15), (vx + 84, vy + 12, 19),
                      (vx + 106, vy + 20, 14), (vx + 96, vy + 30, 12)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 116, 108))
    d.text((vx + 228, vy + 8), "RAS\nTANURA", font=font(11, bold=True), fill=INK)
    y = vy + vh + 10
    y = para(d, gx, y,
             "Riyadh says 4 drones were shot down and no one was hurt. "
             "Brent crude jumped 3.5% to $94.61 a barrel.",
             font(15), gw, 20)

    hline(d, M, R, 534, width=2)

    # ================= MIDDLE BAND =================
    my = 548
    half = (R - M - 24) // 2
    # Ukraine (left)
    x = M
    y = kicker(d, x, my, "War in Ukraine — strikes both ways")
    y = headline(d, x, y, "KYIV MALL HIT AS UKRAINE STRIKES AIR BASE", 24, half)
    y += 2
    y = para(d, x, y,
             "Kyiv says its drones wrecked 5 jets at Savasleyka air base, "
             "300 km east of Moscow. Russia hit a Kyiv shopping mall in "
             "reply: 7 hurt.",
             font(15), half, 19)
    # 5 jet silhouettes
    jx, jy = x, y + 8
    for i in range(5):
        cx = jx + 18 + i * 92
        # fuselage: pointed nose, tapered tail
        d.polygon([(cx - 28, jy + 17), (cx + 24, jy + 17), (cx + 32, jy + 20),
                   (cx + 24, jy + 23), (cx - 28, jy + 23)], fill=(70, 66, 60))
        # swept main wing
        d.polygon([(cx - 6, jy + 17), (cx + 4, jy + 2), (cx + 10, jy + 2),
                   (cx + 6, jy + 17)], fill=(70, 66, 60))
        # tail fin
        d.polygon([(cx - 26, jy + 17), (cx - 20, jy + 6), (cx - 14, jy + 6),
                   (cx - 16, jy + 17)], fill=(70, 66, 60))
    d.text((x, jy + 34), "3 MiG-31  +  2 Su-34  —  claimed destroyed",
           font=font(12), fill=GREY)
    # Kim (right)
    x = M + half + 24
    y = kicker(d, x, my, "North Korea")
    y = headline(d, x, y, "KIM: EXPAND TACTICAL NUKES", 24, half)
    y += 2
    y = para(d, x, y,
             "Kim Jong Un orders tactical nuclear weapons spread to more "
             "units and missions, KCNA reports. Denying the North's nuclear "
             "status, he warns, is \u201can open declaration of war.\u201d",
             font(15), half, 19)
    # missile visual
    mx, myy = x, y + 8
    d.rectangle([mx, myy, mx + half, myy + 40], fill=(223, 216, 200),
                outline=RULE, width=1)
    d.polygon([(mx + 30, myy + 28), (mx + 150, myy + 28), (mx + 178, myy + 20),
               (mx + 150, myy + 12), (mx + 30, myy + 12)], fill=(70, 66, 60))
    d.polygon([(mx + 178, myy + 20), (mx + 196, myy + 20), (mx + 178, myy + 12)],
              fill=RED)
    d.polygon([(mx + 60, myy + 12), (mx + 74, myy + 2), (mx + 82, myy + 12)],
              fill=(70, 66, 60))
    d.polygon([(mx + 60, myy + 28), (mx + 74, myy + 38), (mx + 82, myy + 28)],
              fill=(70, 66, 60))
    d.text((mx + 216, myy + 12), "TACTICAL\nNUKES", font=font(11, bold=True),
           fill=INK)

    hline(d, M, R, 748, width=2)

    # ================= BOTTOM BAND: 3 boxes =================
    by = 762
    bw3 = (R - M - 32) // 3
    boxes = [
        ("EU SUMMIT IN BRUSSELS",
         "€45BN MORE FOR UKRAINE",
         "Leaders clash over a €1.7 trillion EU budget and €45bn more in "
         "loans for Ukraine in 2027 — on top of €90bn already agreed."),
        ("BANGKOK OIL DEPOT BLAST",
         "FIREBALL AT BANGCHAK DEPOT",
         "A blast rocks the Bangchak oil depot in eastern Bangkok. "
         "Evacuations ordered; the fire is under control within an hour. "
         "Cause under investigation."),
        ("BOGOR GOLD MINE, INDONESIA",
         "13 DEAD, 13 STILL TRAPPED",
         "13 miners are confirmed dead and 13 are still trapped 100 m down "
         "in a flooded illegal gold mine in Bogor, West Java. Heavy rain "
         "halted the rescue on Thursday."),
    ]
    for i, (kick, head, body) in enumerate(boxes):
        x = M + i * (bw3 + 16)
        d.rectangle([x, by, x + bw3, by + 140], outline=RULE, width=1)
        ix, iy = x + 10, by + 8
        kicker(d, ix, iy, kick, size=12)
        headline(d, ix, iy + 20, head, 17, bw3 - 20, leading=18)
        para(d, ix, iy + 58, body, font(12), bw3 - 20, 15)

    # ================= ALSO TODAY =================
    ay = 914
    hline(d, M, R, ay, width=2)
    d.text((M, ay + 8), "ALSO TODAY", font=font(14, bold=True), fill=RED)
    items = [
        "SPACEX: FCC clears 1m satellites for data centres",
        "EBOLA in DR Congo passes 12,000 cases",
        "SPAIN votes Sunday — snap election called",
        "GAZA: Israeli strikes kill at least 9 overnight",
        "MACY'S 100th parade moved to Saturday",
        "DURAN DURAN guitarist Andy Taylor dies at 65",
    ]
    colw = (R - M - 40) // 3
    for i, it in enumerate(items):
        x = M + (i % 3) * (colw + 20)
        yy = ay + 30 + (i // 3) * 18
        d.text((x, yy), "▪  " + it, font=font(12), fill=INK)

    # ---- footer ----
    hline(d, M, R, 978, width=1)
    d.text((M, 986),
           "Sources: Reuters · BBC · CNN · USTR · KCNA · Basarnas · dailysummaryof · Open Chronicle — "
           "verified 26–27 Nov 2026",
           font=font(11), fill=GREY)

    out = "/output/entry.png"
    os.makedirs("/output", exist_ok=True)
    img.save(out, "PNG", optimize=True)
    print("saved", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
