import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import time

# -----------------------------
# Initialize GLFW
# -----------------------------
if not glfw.init():
    raise Exception("Failed to initialize GLFW")

window = glfw.create_window(800, 600, "Rotating Cube", None, None)

if not window:
    glfw.terminate()
    raise Exception("Failed to create GLFW window")

glfw.make_context_current(window)

print("Vendor  :", glGetString(GL_VENDOR).decode())
print("Renderer:", glGetString(GL_RENDERER).decode())
print("Version :", glGetString(GL_VERSION).decode())

# Enable depth testing
glEnable(GL_DEPTH_TEST)

# Projection
glMatrixMode(GL_PROJECTION)
gluPerspective(45, 800 / 600, 0.1, 50.0)

glMatrixMode(GL_MODELVIEW)


def draw_cube():
    glBegin(GL_QUADS)

    # Front (Red)
    glColor3f(1, 0, 0)
    glVertex3f(-1, -1,  1)
    glVertex3f( 1, -1,  1)
    glVertex3f( 1,  1,  1)
    glVertex3f(-1,  1,  1)

    # Back (Green)
    glColor3f(0, 1, 0)
    glVertex3f(-1, -1, -1)
    glVertex3f(-1,  1, -1)
    glVertex3f( 1,  1, -1)
    glVertex3f( 1, -1, -1)

    # Left (Blue)
    glColor3f(0, 0, 1)
    glVertex3f(-1, -1, -1)
    glVertex3f(-1, -1,  1)
    glVertex3f(-1,  1,  1)
    glVertex3f(-1,  1, -1)

    # Right (Yellow)
    glColor3f(1, 1, 0)
    glVertex3f(1, -1, -1)
    glVertex3f(1,  1, -1)
    glVertex3f(1,  1,  1)
    glVertex3f(1, -1,  1)

    # Top (Magenta)
    glColor3f(1, 0, 1)
    glVertex3f(-1, 1, -1)
    glVertex3f(-1, 1,  1)
    glVertex3f( 1, 1,  1)
    glVertex3f( 1, 1, -1)

    # Bottom (Cyan)
    glColor3f(0, 1, 1)
    glVertex3f(-1, -1, -1)
    glVertex3f( 1, -1, -1)
    glVertex3f( 1, -1,  1)
    glVertex3f(-1, -1,  1)

    glEnd()


# -----------------------------
# Main Loop
# -----------------------------
while not glfw.window_should_close(window):

    glfw.poll_events()

    glClearColor(0.1, 0.1, 0.15, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()

    # Move cube away from camera
    glTranslatef(0.0, 0.0, -6.0)

    angle = time.time() * 50

    # Rotate cube
    glRotatef(angle, 1, 0, 0)
    glRotatef(angle * 0.7, 0, 1, 0)
    glRotatef(angle * 0.3, 0, 0, 1)

    draw_cube()

    glfw.swap_buffers(window)

glfw.terminate()