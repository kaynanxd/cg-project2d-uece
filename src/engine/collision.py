def point_box(px, py, box):
    """Verifica se ponto (px, py) está dentro da caixa (x, y, w, h)."""
    x, y, w, h = box
    return x <= px <= x + w and y <= py <= y + h

def is_clicked(mouse_pos, button_rect):
    """Verifica se o clique do mouse está dentro de um retângulo do menu."""
    mx, my = mouse_pos
    rx, ry, rw, rh = button_rect
    return rx <= mx <= rx + rw and ry <= my <= ry + rh