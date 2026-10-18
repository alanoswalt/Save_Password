"""Create the Windows icon from the app's vector artwork."""

from pathlib import Path

from PIL import Image, ImageDraw


OUTPUT = Path(__file__).with_name("save_password.ico")
SIZES = (16, 24, 32, 48, 64, 128, 256)


def draw_icon(size: int) -> Image.Image:
    scale = 4
    canvas_size = size * scale
    image = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    def point(x: float, y: float) -> tuple[int, int]:
        return round(x * scale), round(y * scale)

    def polygon(points, fill):
        draw.polygon([point(x, y) for x, y in points], fill=fill)

    def ellipse(box, fill):
        draw.ellipse(tuple(value * scale for value in box), fill=fill)

    radius = 54
    draw.rounded_rectangle(
        (8 * scale, 8 * scale, 248 * scale, 248 * scale),
        radius=radius * scale,
        fill="#0B1220",
        outline="#315887",
        width=max(1, 3 * scale),
    )

    shield = [(128, 31), (211, 61), (211, 133), (128, 228), (45, 133), (45, 61)]
    polygon(shield, "#3D8CF4")
    inner_shield = [(128, 48), (194, 72), (194, 132), (128, 208), (62, 132), (62, 72)]
    polygon(inner_shield, "#122743")

    ellipse((105, 94, 151, 140), "#F4F8FF")
    polygon([(116, 126), (140, 126), (146, 178), (110, 178)], "#F4F8FF")
    ellipse((120, 109, 136, 125), "#2D72E8")
    draw.line([point(128, 121), point(128, 147)], fill="#2D72E8", width=7 * scale)

    return image.resize((size, size), Image.Resampling.LANCZOS)


images = [draw_icon(size) for size in SIZES]
images[-1].save(
    OUTPUT,
    format="ICO",
    sizes=[(size, size) for size in SIZES],
    append_images=images[:-1],
)
print(f"Created {OUTPUT}")
