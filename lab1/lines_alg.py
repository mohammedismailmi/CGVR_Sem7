import glfw
from OpenGL.GL import *

W, H = 800, 600

def dda(x0, y0, x1, y1):
    dx, dy = x1 - x0, y1 - y0
    steps = max(abs(dx), abs(dy))
    if steps == 0:
        return [(x0, y0)]
    xi, yi = dx / steps, dy / steps
    x, y = x0, y0
    pts = []
    for i in range(steps + 1):
        pts.append((round(x), round(y)))
        x += xi
        y += yi
    return pts

def bresenham(x0, y0, x1, y1):
    dx, dy = abs(x1 - x0), abs(y1 - y0)
    sx = 1 if x1 > x0 else -1
    sy = 1 if y1 > y0 else -1
    x, y = x0, y0
    pts = []

    if dx > dy:
        err = dx / 2
        for i in range(dx + 1):
            pts.append((x, y))
            x += sx
            err -= dy
            if err < 0:
                y += sy
                err += dx
    else:
        err = dy / 2
        for i in range(dy + 1):
            pts.append((x, y))
            y += sy
            err -= dx
            if err < 0:
                x += sx
                err += dy
    return pts

def draw_points(pts, r, g, b, size=4):
    glColor3f(r, g, b)
    glPointSize(size)
    glBegin(GL_POINTS)
    for x, y in pts:
        glVertex2i(x, y)
    glEnd()

clicks = []

def on_click(window, button, action, mods):
    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
        mx, my = glfw.get_cursor_pos(window)
        clicks.append((int(mx), H - int(my)))  # flip y to match GL coords
        if len(clicks) > 2:
            clicks.pop(0)

def main():
    if not glfw.init():
        return

    window = glfw.create_window(W, H, "DDA vs Bresenham", None, None)
    glfw.make_context_current(window)
    glfw.set_mouse_button_callback(window, on_click)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, W, 0, H, -1, 1)
    glMatrixMode(GL_MODELVIEW)

    print("Click two points to draw a line (DDA=red, Bresenham=green)")

    while not glfw.window_should_close(window):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT)
        glClearColor(0, 0, 0, 1)

        if len(clicks) == 2:
            (x0, y0), (x1, y1) = clicks
            offset = 10
            dda_pts = [(x, y + offset) for x, y in dda(x0, y0, x1, y1)]
            draw_points(dda_pts, 1, 0, 0)
            draw_points(bresenham(x0, y0, x1, y1), 0, 1, 0)

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()