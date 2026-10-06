"""Dibuja una vista sencilla del grafo del autómata en PNG."""
from __future__ import annotations

from io import BytesIO
import math
from PIL import Image, ImageDraw, ImageFont

from automata import Automaton


def draw_automaton(machine: Automaton) -> bytes:
    width, height, radius = 820, max(340, 150 + 100 * math.ceil(len(machine.states) / 5)), 36
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("arial.ttf", 15)
        small = ImageFont.truetype("arial.ttf", 13)
    except OSError:
        font = ImageFont.load_default()
        small = font
    count = len(machine.states)
    center = (width / 2, height / 2)
    orbit = min(width * 0.40, max(90, height * 0.40))
    positions = {
        state: (center[0] + orbit * math.cos(-math.pi / 2 + 2 * math.pi * i / count),
                center[1] + orbit * math.sin(-math.pi / 2 + 2 * math.pi * i / count))
        for i, state in enumerate(machine.states)
    }
    groups: dict[tuple[str, str], list[str]] = {}
    for (source, symbol), targets in machine.transitions.items():
        for target in targets:
            groups.setdefault((source, target), []).append("λ" if not symbol else symbol)
    for (source, target), symbols in groups.items():
        x1, y1 = positions[source]
        x2, y2 = positions[target]
        if source == target:
            box = (x1 - 26, y1 - 68, x1 + 26, y1 - 16)
            draw.arc(box, 0, 310, fill="#344563", width=2)
            draw.polygon([(x1 + 23, y1 - 44), (x1 + 14, y1 - 42), (x1 + 21, y1 - 35)], fill="#344563")
            label_x, label_y = x1 + 29, y1 - 64
        else:
            dx, dy = x2 - x1, y2 - y1
            length = max(1, math.hypot(dx, dy))
            ux, uy = dx / length, dy / length
            start = (x1 + ux * radius, y1 + uy * radius)
            end = (x2 - ux * (radius + 8), y2 - uy * (radius + 8))
            draw.line((start, end), fill="#344563", width=2)
            angle = math.atan2(end[1] - start[1], end[0] - start[0])
            tip = end
            left = (tip[0] - 12 * math.cos(angle - .45), tip[1] - 12 * math.sin(angle - .45))
            right = (tip[0] - 12 * math.cos(angle + .45), tip[1] - 12 * math.sin(angle + .45))
            draw.polygon([tip, left, right], fill="#344563")
            label_x = (start[0] + end[0]) / 2
            label_y = (start[1] + end[1]) / 2 - 17
        draw.text((label_x, label_y), ", ".join(sorted(symbols)), fill="#172b4d", font=small, anchor="mm")
    for state, (x, y) in positions.items():
        if state == machine.initial:
            draw.line((x - radius - 38, y, x - radius - 2, y), fill="#344563", width=2)
            draw.polygon([(x - radius, y), (x - radius - 12, y - 7), (x - radius - 12, y + 7)], fill="#344563")
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill="#f4f7fb", outline="#344563", width=2)
        if state in machine.accepting:
            draw.ellipse((x - radius + 5, y - radius + 5, x + radius - 5, y + radius - 5), outline="#344563", width=1)
        draw.text((x, y), state, fill="#172b4d", font=font, anchor="mm")
    output = BytesIO()
    image.save(output, format="PNG")
    return output.getvalue()
