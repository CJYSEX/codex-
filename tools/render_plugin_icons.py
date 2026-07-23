from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SIZE = 512


def rounded(draw, box, radius, fill):
    draw.rounded_rectangle(box, radius=radius, fill=fill)


def document(path, color):
    image = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    rounded(draw, (0, 0, 511, 511), 112, color)
    draw.polygon([(146, 92), (312, 92), (366, 146), (366, 420), (146, 420)], fill="white")
    draw.polygon([(312, 92), (312, 162), (366, 162)], fill="#BFDBFE")
    for y, width in [(232, 144), (286, 144), (340, 102)]:
        draw.line((184, y, 184 + width, y), fill=color, width=24)
    image.save(path)


def pdf(path, color):
    image = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    rounded(draw, (0, 0, 511, 511), 112, color)
    draw.polygon([(146, 92), (312, 92), (366, 146), (366, 420), (146, 420)], fill="white")
    draw.polygon([(312, 92), (312, 162), (366, 162)], fill="#FECACA")
    draw.arc((180, 198, 318, 338), 205, 345, fill=color, width=22)
    draw.line((184, 350, 328, 350), fill=color, width=22)
    image.save(path)


def spreadsheet(path, color):
    image = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    rounded(draw, (0, 0, 511, 511), 112, color)
    rounded(draw, (112, 106, 400, 406), 20, "white")
    draw.rectangle((144, 164, 368, 362), fill="#DCFCE7")
    for y in (230, 296):
        draw.line((144, y, 368, y), fill=color, width=18)
    for x in (218, 292):
        draw.line((x, 164, x, 362), fill=color, width=18)
    draw.line((144, 132, 368, 132), fill="#86EFAC", width=26)
    image.save(path)


def presentation(path, color):
    image = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    rounded(draw, (0, 0, 511, 511), 112, color)
    rounded(draw, (104, 114, 408, 340), 18, "white")
    draw.line((256, 340, 256, 398), fill="white", width=24)
    draw.line((188, 398, 324, 398), fill="white", width=24)
    draw.rectangle((154, 230, 202, 292), fill="#FED7AA", outline=color, width=12)
    draw.rectangle((232, 180, 280, 292), fill="#FED7AA", outline=color, width=12)
    draw.rectangle((310, 204, 358, 292), fill="#FED7AA", outline=color, width=12)
    draw.line((138, 340, 374, 340), fill="#FED7AA", width=14)
    image.save(path)


def main():
    assets = {
        "cjysa-documents": (document, "#2563EB"),
        "cjysa-pdf": (pdf, "#DC2626"),
        "cjysa-spreadsheets": (spreadsheet, "#107C41"),
        "cjysa-presentations": (presentation, "#C43E1C"),
    }
    for plugin, (builder, color) in assets.items():
        target = ROOT / "plugins" / plugin / "assets"
        target.mkdir(parents=True, exist_ok=True)
        builder(target / "icon.png", color)
        builder(target / "logo.png", color)
        print(target / "icon.png")


if __name__ == "__main__":
    main()
