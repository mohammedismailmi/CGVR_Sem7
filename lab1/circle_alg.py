import glfw
from OpenGL.GL import *

W, H = 800, 600

def circle_points(xc, yc, x, y):
    return [
        (xc + x, yc + y), (xc - x, yc + y),
        (xc + x, yc - y), (xc - x, yc - y),
        (xc + y, yc + x), (xc - y, yc + x),
        (xc + y, yc - x), (xc - y, yc - x),
    ]

def bresenham_circle(xc, yc, r):
    x, y = 0, r
    d = 3 - 2 * r
    pts = []
    while x <= y:
        pts += circle_points(xc, yc, x, y)
        if d < 0:
            d += 4 * x + 6
        else:
            d += 4 * (x - y) + 10
            y -= 1
        x += 1
    return pts

def draw_points(pts, r, g, b, size=4):
    glColor3f(r, g, b)
    glPointSize(size)
    glBegin(GL_POINTS)
    for x, y in pts:
        glVertex2i(x, y)
    glEnd()

clicks = []  # first click = center, second click = point on circumference

def on_click(window, button, action, mods):
    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
        mx, my = glfw.get_cursor_pos(window)
        clicks.append((int(mx), H - int(my)))
        if len(clicks) > 2:
            clicks.pop(0)

def main():
    if not glfw.init():
        return

    window = glfw.create_window(W, H, "Bresenham Circle", None, None)
    glfw.make_context_current(window)
    glfw.set_mouse_button_callback(window, on_click)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, W, 0, H, -1, 1)
    glMatrixMode(GL_MODELVIEW)

    print("Click center, then click a point on the circle's edge to set radius")

    while not glfw.window_should_close(window):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT)
        glClearColor(0, 0, 0, 1)

        if len(clicks) == 2:
            (xc, yc), (px, py) = clicks
            r = round(((px - xc) ** 2 + (py - yc) ** 2) ** 0.5)
            draw_points(bresenham_circle(xc, yc, r), 0, 1, 0)

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()