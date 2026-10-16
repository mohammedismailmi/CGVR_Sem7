
import glfw
import numpy as np
from OpenGL.GL import *
import math

# ============================================================
# EXPERIMENT 8: OPENGL VERTEX AND FRAGMENT SHADERS
# Interactive 2D geometric transformations
# ============================================================

BG_COLOR = (0.03, 0.03, 0.04, 1.0)

zoom = 1.0
angle = 0.0
tx, ty = 0.0, 0.0
sx, sy = 1.0, 1.0

animation = False
last_time = 0.0

reflect = False
shear = False
pivot_rotation = False

drag_button = None
last_mouse_x = 0.0
last_mouse_y = 0.0

# Complex polygon
vertices = np.array([
    [-5.0, -3.0],
    [-2.0, -5.0],
    [ 2.0, -4.0],
    [ 5.0, -1.0],
    [ 4.0,  3.0],
    [ 1.0,  5.0],
    [-3.0,  4.0],
    [-5.0,  1.0]
], dtype=np.float32)


# ============================================================
# VERTEX SHADER
# ============================================================

VERTEX_SHADER = """
#version 330 core

layout (location = 0) in vec2 aPos;

uniform mat3 uTransform;

void main()
{
    vec3 position = uTransform * vec3(aPos, 1.0);
    gl_Position = vec4(position.xy, 0.0, 1.0);
}
"""


# ============================================================
# FRAGMENT SHADER
# ============================================================

FRAGMENT_SHADER = """
#version 330 core

uniform vec3 uColor;
out vec4 FragColor;

void main()
{
    FragColor = vec4(uColor, 1.0);
}
"""


# ============================================================
# SHADER COMPILATION AND LINKING
# ============================================================

def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)

    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(shader).decode()
        glDeleteShader(shader)
        raise RuntimeError("Shader compilation failed:\n" + error)

    return shader


def create_shader_program():
    vertex_shader = compile_shader(
        VERTEX_SHADER, GL_VERTEX_SHADER
    )

    fragment_shader = compile_shader(
        FRAGMENT_SHADER, GL_FRAGMENT_SHADER
    )

    program = glCreateProgram()
    glAttachShader(program, vertex_shader)
    glAttachShader(program, fragment_shader)
    glLinkProgram(program)

    if not glGetProgramiv(program, GL_LINK_STATUS):
        error = glGetProgramInfoLog(program).decode()
        raise RuntimeError("Shader linking failed:\n" + error)

    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    return program


# ============================================================
# VERTEX BUFFER OBJECT AND VERTEX ARRAY OBJECT
# ============================================================

def create_object(data):
    data = np.asarray(data, dtype=np.float32)

    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)

    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)

    glBufferData(
        GL_ARRAY_BUFFER,
        data.nbytes,
        data,
        GL_STATIC_DRAW
    )

    glVertexAttribPointer(
        0, 2, GL_FLOAT, GL_FALSE, 0, None
    )
    glEnableVertexAttribArray(0)

    glBindVertexArray(0)
    glBindBuffer(GL_ARRAY_BUFFER, 0)

    return vao, vbo, len(data)


# ============================================================
# HOMOGENEOUS TRANSFORMATION MATRICES
# ============================================================

def translation(x, y):
    return np.array([
        [1, 0, x],
        [0, 1, y],
        [0, 0, 1]
    ], dtype=np.float32)


def rotation(degrees):
    theta = math.radians(degrees)
    c = math.cos(theta)
    s = math.sin(theta)

    return np.array([
        [c, -s, 0],
        [s,  c, 0],
        [0,  0, 1]
    ], dtype=np.float32)


def scaling(x, y):
    return np.array([
        [x, 0, 0],
        [0, y, 0],
        [0, 0, 1]
    ], dtype=np.float32)


def reflection_x():
    return np.array([
        [1,  0, 0],
        [0, -1, 0],
        [0,  0, 1]
    ], dtype=np.float32)


def reflection_y():
    return np.array([
        [-1, 0, 0],
        [ 0, 1, 0],
        [ 0, 0, 1]
    ], dtype=np.float32)


def reflection_y_eq_x():
    return np.array([
        [0, 1, 0],
        [1, 0, 0],
        [0, 0, 1]
    ], dtype=np.float32)


def shearing(shx, shy):
    return np.array([
        [1,   shx, 0],
        [shy, 1,   0],
        [0,   0,   1]
    ], dtype=np.float32)


def rotation_about_pivot(degrees, px, py):
    return (
        translation(px, py)
        @ rotation(degrees)
        @ translation(-px, -py)
    )


# ============================================================
# DRAWING USING SHADERS
# ============================================================

def draw(vao, count, mode, program, matrix, color):
    glUseProgram(program)

    transform_location = glGetUniformLocation(
        program, "uTransform"
    )
    color_location = glGetUniformLocation(
        program, "uColor"
    )

    glUniformMatrix3fv(
        transform_location,
        1,
        GL_TRUE,
        np.asarray(matrix, dtype=np.float32)
    )

    glUniform3f(
        color_location,
        float(color[0]),
        float(color[1]),
        float(color[2])
    )

    glBindVertexArray(vao)
    glDrawArrays(mode, 0, count)
    glBindVertexArray(0)


# ============================================================
# GRID AND AXES
# ============================================================

def create_grid():
    grid_lines = []

    for i in range(-20, 21):
        if i == 0:
            continue

        grid_lines.extend([
            [-20, i], [20, i],
            [i, -20], [i, 20]
        ])

    axes = [
        [-20, 0], [20, 0],
        [0, -20], [0, 20]
    ]

    return create_object(grid_lines), create_object(axes)


# ============================================================
# MOUSE INTERACTION
# ============================================================

def mouse_button_callback(window, button, action, mods):
    global drag_button, last_mouse_x, last_mouse_y

    if action == glfw.PRESS:
        drag_button = button
        last_mouse_x, last_mouse_y = glfw.get_cursor_pos(window)

    elif action == glfw.RELEASE:
        if button == drag_button:
            drag_button = None


def cursor_position_callback(window, xpos, ypos):
    global last_mouse_x, last_mouse_y
    global tx, ty, angle, sx, sy

    if drag_button is None:
        last_mouse_x, last_mouse_y = xpos, ypos
        return

    dx = xpos - last_mouse_x
    dy = ypos - last_mouse_y

    last_mouse_x, last_mouse_y = xpos, ypos

    width, height = glfw.get_window_size(window)

    if width == 0 or height == 0:
        return

    aspect = width / height
    half_height = 20.0 / zoom
    half_width = half_height * aspect

    world_dx = dx * (2.0 * half_width / width)
    world_dy = -dy * (2.0 * half_height / height)

    if drag_button == glfw.MOUSE_BUTTON_LEFT:
        shift_pressed = (
            glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS
            or glfw.get_key(window, glfw.KEY_RIGHT_SHIFT) == glfw.PRESS
        )

        if shift_pressed:
            sx *= math.exp(dx * 0.01)
            sy *= math.exp(-dy * 0.01)

            sx = max(-10.0, min(10.0, sx))
            sy = max(-10.0, min(10.0, sy))

            if abs(sx) < 0.05:
                sx = 0.05 if sx >= 0 else -0.05

            if abs(sy) < 0.05:
                sy = 0.05 if sy >= 0 else -0.05
        else:
            tx += world_dx
            ty += world_dy

    elif drag_button == glfw.MOUSE_BUTTON_RIGHT:
        angle += dx * 0.5


def scroll_callback(window, xoffset, yoffset):
    global zoom

    if yoffset > 0:
        zoom = min(zoom * 1.1, 5.0)
    elif yoffset < 0:
        zoom = max(zoom / 1.1, 0.2)


# ============================================================
# KEYBOARD CONTROLS
# ============================================================

def reset_transformations():
    global angle, tx, ty, sx, sy
    global animation, reflect, shear, pivot_rotation

    angle = 0.0
    tx, ty = 0.0, 0.0
    sx, sy = 1.0, 1.0

    animation = False
    reflect = False
    shear = False
    pivot_rotation = False


def key_callback(window, key, scancode, action, mods):
    global zoom, angle, tx, ty, sx, sy
    global animation, reflect, shear, pivot_rotation

    if action != glfw.PRESS:
        return

    if key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)

    elif key == glfw.KEY_1:
        tx += 2.0
        ty += 1.0

    elif key == glfw.KEY_2:
        angle += 15.0

    elif key == glfw.KEY_3:
        sx *= 1.2
        sy *= 0.8

    elif key == glfw.KEY_4:
        sy *= -1.0

    elif key == glfw.KEY_5:
        sx *= -1.0

    elif key == glfw.KEY_6:
        reflect = not reflect

    elif key == glfw.KEY_7:
        shear = not shear

    elif key == glfw.KEY_8:
        pivot_rotation = not pivot_rotation

    elif key == glfw.KEY_9:
        animation = not animation

    elif key == glfw.KEY_0:
        reset_transformations()

    elif key in (glfw.KEY_EQUAL, glfw.KEY_KP_ADD):
        zoom = min(zoom * 1.1, 5.0)

    elif key in (glfw.KEY_MINUS, glfw.KEY_KP_SUBTRACT):
        zoom = max(zoom / 1.1, 0.2)

    elif key == glfw.KEY_R:
        zoom = 1.0


# ============================================================
# PRINT MENU
# ============================================================

def print_menu():
    print("""
==================================================
 EXPERIMENT 8: VERTEX AND FRAGMENT SHADERS
==================================================
MOUSE:
 Left-click + drag       : Translate
 Right-click + drag      : Rotate
 Shift + left-drag       : Scale
 Mouse wheel             : Zoom

KEYBOARD:
 1 : Translate
 2 : Rotate 15 degrees
 3 : Non-uniform scaling
 4 : Reflect about X-axis
 5 : Reflect about Y-axis
 6 : Toggle reflection about y = x
 7 : Toggle shearing
 8 : Toggle rotation about pivot (3, 2)
 9 : Toggle continuous rotation
 0 : Reset transformations
 + / - : Zoom
 R : Reset zoom
 ESC : Exit
==================================================
""")


# ============================================================
# MAIN OPENGL LOOP
# ============================================================

def main():
    global angle, last_time

    if not glfw.init():
        raise RuntimeError("GLFW initialization failed.")

    # Request OpenGL 3.3 Core Profile.
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(
        glfw.OPENGL_PROFILE,
        glfw.OPENGL_CORE_PROFILE
    )

    # Needed for modern OpenGL contexts on macOS.
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)

    window = glfw.create_window(
        1000, 800,
        "Experiment 8 - Interactive OpenGL Shaders",
        None, None
    )

    if not window:
        glfw.terminate()
        raise RuntimeError(
            "Could not create window. Check OpenGL support."
        )

    glfw.make_context_current(window)
    glfw.swap_interval(1)

    glfw.set_key_callback(window, key_callback)
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_cursor_pos_callback(window, cursor_position_callback)
    glfw.set_scroll_callback(window, scroll_callback)

    program = create_shader_program()

    polygon_vao, polygon_vbo, polygon_count = create_object(vertices)

    (grid_vao, grid_vbo, grid_count), (
        axes_vao, axes_vbo, axes_count
    ) = create_grid()

    glClearColor(*BG_COLOR)
    glDisable(GL_DEPTH_TEST)

    print_menu()
    last_time = glfw.get_time()

    try:
        while not glfw.window_should_close(window):
            current_time = glfw.get_time()
            dt = current_time - last_time
            last_time = current_time

            if animation:
                angle += 60.0 * dt

            width, height = glfw.get_framebuffer_size(window)

            if height == 0 or width == 0:
                glfw.poll_events()
                continue

            glViewport(0, 0, width, height)
            glClear(GL_COLOR_BUFFER_BIT)

            aspect = width / height
            half_height = 20.0 / zoom
            half_width = half_height * aspect

            # Projection from world coordinates to clip coordinates.
            projection = np.array([
                [1.0 / half_width, 0, 0],
                [0, 1.0 / half_height, 0],
                [0, 0, 1]
            ], dtype=np.float32)

            # Grid and axes remain stationary.
            draw(
                grid_vao, grid_count, GL_LINES,
                program, projection, (0.15, 0.15, 0.15)
            )

            draw(
                axes_vao, axes_count, GL_LINES,
                program, projection, (0.65, 0.65, 0.65)
            )

            # Composite transformation matrix.
            model = (
                translation(tx, ty)
                @ rotation(angle)
                @ scaling(sx, sy)
            )

            if reflect:
                model = reflection_y_eq_x() @ model

            if shear:
                model = shearing(0.3, 0.0) @ model

            if pivot_rotation:
                model = (
                    rotation_about_pivot(15, 3, 2)
                    @ model
                )

            final_matrix = projection @ model

            # Filled polygon.
            draw(
                polygon_vao, polygon_count, GL_TRIANGLE_FAN,
                program, final_matrix, (0.0, 0.55, 0.85)
            )

            # Polygon outline.
            draw(
                polygon_vao, polygon_count, GL_LINE_LOOP,
                program, final_matrix, (0.4, 0.9, 1.0)
            )

            glfw.swap_buffers(window)
            glfw.poll_events()

    finally:
        glDeleteBuffers(1, [polygon_vbo])
        glDeleteVertexArrays(1, [polygon_vao])

        glDeleteBuffers(1, [grid_vbo])
        glDeleteVertexArrays(1, [grid_vao])

        glDeleteBuffers(1, [axes_vbo])
        glDeleteVertexArrays(1, [axes_vao])

        glDeleteProgram(program)
        glfw.terminate()


if __name__ == "__main__":
    main()
