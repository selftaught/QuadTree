from pygame import draw, Rect, Surface


def draw_rect_border(screen: Surface, r: Rect, color) -> None:
    draw.line(screen, color, (r.x, r.y), (r.x + r.w, r.y))
    draw.line(screen, color, (r.x, r.y), (r.x, r.y + r.h))
    draw.line(screen, color, (r.x + r.w, r.y), (r.x + r.w, r.y + r.h))
    draw.line(screen, color, (r.x, r.y + r.h), (r.x + r.w, r.y + r.h))
