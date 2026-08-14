import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
import sys
import math


# =========================================================
# BRESENHAM'S LINE DRAWING ALGORITHM
# =========================================================

def bresenham_line(x1, y1, x2, y2):

    points = []

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    sx = 1 if x2 > x1 else -1
    sy = 1 if y2 > y1 else -1

    err = dx - dy

    x = x1
    y = y1

    while True:

        points.append((x, y))

        if x == x2 and y == y2:
            break

        e2 = 2 * err

        if e2 > -dy:
            err -= dy
            x += sx

        if e2 < dx:
            err += dx
            y += sy

    return points


# =========================================================
# CALCULATE GRAPH RANGE
# =========================================================

def calculate_range(x1, y1, x2, y2):

    min_x = min(x1, x2)
    max_x = max(x1, x2)

    min_y = min(y1, y2)
    max_y = max(y1, y2)

    range_x = max_x - min_x
    range_y = max_y - min_y

    # Handle vertical / horizontal lines
    if range_x == 0:
        range_x = 10

    if range_y == 0:
        range_y = 10

    # Add 15% padding
    padding_x = max(2, range_x * 0.15)
    padding_y = max(2, range_y * 0.15)

    graph_min_x = min_x - padding_x
    graph_max_x = max_x + padding_x

    graph_min_y = min_y - padding_y
    graph_max_y = max_y + padding_y

    return (
        graph_min_x,
        graph_max_x,
        graph_min_y,
        graph_max_y
    )


# =========================================================
# CALCULATE GRID SPACING
# =========================================================

def calculate_grid_spacing(graph_range):

    if graph_range <= 20:
        return 1

    elif graph_range <= 50:
        return 5

    elif graph_range <= 100:
        return 10

    elif graph_range <= 500:
        return 50

    elif graph_range <= 1000:
        return 100

    elif graph_range <= 5000:
        return 500

    elif graph_range <= 10000:
        return 1000

    elif graph_range <= 50000:
        return 5000

    elif graph_range <= 100000:
        return 10000

    else:
        return 100000


# =========================================================
# FORMAT COORDINATE LABEL
# =========================================================

def format_number(value):

    # If effectively an integer
    if abs(value - round(value)) < 0.0001:
        return str(int(round(value)))

    return f"{value:.1f}"


# =========================================================
# DRAW TEXT
# =========================================================

def draw_text(x, y, text):

    glRasterPos2f(x, y)

    for character in text:

        glutBitmapCharacter(
            GLUT_BITMAP_HELVETICA_10,
            ord(character)
        )


# =========================================================
# DRAW GRID
# =========================================================

def draw_grid(
    min_x,
    max_x,
    min_y,
    max_y
):

    range_x = max_x - min_x
    range_y = max_y - min_y

    spacing_x = calculate_grid_spacing(range_x)
    spacing_y = calculate_grid_spacing(range_y)

    # -----------------------------------------------------
    # GRID LINES
    # -----------------------------------------------------

    glColor3f(
        0.25,
        0.25,
        0.25
    )

    glLineWidth(1.0)

    glBegin(GL_LINES)

    # -----------------------------------------------------
    # Vertical grid lines
    # -----------------------------------------------------

    start_x = math.ceil(
        min_x / spacing_x
    ) * spacing_x

    x = start_x

    while x <= max_x:

        glVertex2f(
            x,
            min_y
        )

        glVertex2f(
            x,
            max_y
        )

        x += spacing_x

    # -----------------------------------------------------
    # Horizontal grid lines
    # -----------------------------------------------------

    start_y = math.ceil(
        min_y / spacing_y
    ) * spacing_y

    y = start_y

    while y <= max_y:

        glVertex2f(
            min_x,
            y
        )

        glVertex2f(
            max_x,
            y
        )

        y += spacing_y

    glEnd()

    # =====================================================
    # AXES
    # =====================================================

    glColor3f(
        1.0,
        1.0,
        1.0
    )

    glLineWidth(2.0)

    glBegin(GL_LINES)

    # X axis
    if min_y <= 0 <= max_y:

        glVertex2f(
            min_x,
            0
        )

        glVertex2f(
            max_x,
            0
        )

    # Y axis
    if min_x <= 0 <= max_x:

        glVertex2f(
            0,
            min_y
        )

        glVertex2f(
            0,
            max_y
        )

    glEnd()

    # =====================================================
    # COORDINATE LABELS
    # =====================================================

    glColor3f(
        0.8,
        0.8,
        0.8
    )

    # -----------------------------------------------------
    # X-axis coordinate labels
    # -----------------------------------------------------

    x = start_x

    while x <= max_x:

        label = format_number(x)

        # If X-axis exists, put labels slightly below it
        if min_y <= 0 <= max_y:

            draw_text(
                x + range_x * 0.005,
                -range_y * 0.035,
                label
            )

        else:

            # Put labels near bottom
            draw_text(
                x + range_x * 0.005,
                min_y + range_y * 0.02,
                label
            )

        x += spacing_x

    # -----------------------------------------------------
    # Y-axis coordinate labels
    # -----------------------------------------------------

    y = start_y

    while y <= max_y:

        label = format_number(y)

        # If Y-axis exists, put labels to the left
        if min_x <= 0 <= max_x:

            draw_text(
                -range_x * 0.045,
                y + range_y * 0.005,
                label
            )

        else:

            # Put labels near left side
            draw_text(
                min_x + range_x * 0.01,
                y + range_y * 0.005,
                label
            )

        y += spacing_y


# =========================================================
# DRAW BRESENHAM POINTS
# =========================================================

def draw_bresenham_points(points):

    # Green pixels
    glColor3f(
        0.0,
        1.0,
        0.0
    )

    glPointSize(12.0)

    glBegin(GL_POINTS)

    for x, y in points:

        glVertex2f(
            x,
            y
        )

    glEnd()


# =========================================================
# DRAW WHITE CONNECTION
# =========================================================

def draw_connecting_line(points):

    glColor3f(
        1.0,
        1.0,
        1.0
    )

    glLineWidth(4.0)

    glBegin(GL_LINE_STRIP)

    for x, y in points:

        glVertex2f(
            x,
            y
        )

    glEnd()


# =========================================================
# DRAW ENDPOINTS
# =========================================================

def draw_endpoints(
    x1,
    y1,
    x2,
    y2
):

    glColor3f(
        1.0,
        0.0,
        0.0
    )

    glPointSize(12.0)

    glBegin(GL_POINTS)

    glVertex2f(
        x1,
        y1
    )

    glVertex2f(
        x2,
        y2
    )

    glEnd()


# =========================================================
# MAIN
# =========================================================

def main():

    # -----------------------------------------------------
    # Initialize GLUT
    # -----------------------------------------------------

    glutInit(sys.argv)

    # -----------------------------------------------------
    # USER INPUT
    # -----------------------------------------------------

    print()
    print("==========================================")
    print("     BRESENHAM'S LINE DRAWING ALGORITHM")
    print("==========================================")
    print()

    x1 = int(input("Enter x1: "))
    y1 = int(input("Enter y1: "))

    x2 = int(input("Enter x2: "))
    y2 = int(input("Enter y2: "))

    print()

    print(
        f"Line: ({x1}, {y1}) -> ({x2}, {y2})"
    )

    # -----------------------------------------------------
    # BRESENHAM
    # -----------------------------------------------------

    points = bresenham_line(
        x1,
        y1,
        x2,
        y2
    )

    print()
    print("Bresenham pixels:")
    print()

    for i, point in enumerate(points):

        print(
            f"Pixel {i + 1}: {point}"
        )

    # -----------------------------------------------------
    # GRAPH RANGE
    # -----------------------------------------------------

    (
        min_x,
        max_x,
        min_y,
        max_y
    ) = calculate_range(
        x1,
        y1,
        x2,
        y2
    )

    print()
    print("Graph range:")
    print(
        f"X: {min_x:.1f} -> {max_x:.1f}"
    )
    print(
        f"Y: {min_y:.1f} -> {max_y:.1f}"
    )

    # -----------------------------------------------------
    # GRID SPACING
    # -----------------------------------------------------

    grid_x = calculate_grid_spacing(
        max_x - min_x
    )

    grid_y = calculate_grid_spacing(
        max_y - min_y
    )

    print(
        f"X grid spacing: {grid_x}"
    )

    print(
        f"Y grid spacing: {grid_y}"
    )

    # -----------------------------------------------------
    # INITIALIZE GLFW
    # -----------------------------------------------------

    if not glfw.init():

        print(
            "Failed to initialize GLFW"
        )

        sys.exit()

    # -----------------------------------------------------
    # CREATE WINDOW
    # -----------------------------------------------------

    window = glfw.create_window(
        1000,
        800,
        "Bresenham Line Drawing",
        None,
        None
    )

    if not window:

        glfw.terminate()

        print(
            "Failed to create GLFW window"
        )

        sys.exit()

    glfw.make_context_current(
        window
    )

    # -----------------------------------------------------
    # BACKGROUND
    # -----------------------------------------------------

    glClearColor(
        0.05,
        0.05,
        0.05,
        1.0
    )

    # -----------------------------------------------------
    # DYNAMIC COORDINATE SYSTEM
    # -----------------------------------------------------

    glMatrixMode(
        GL_PROJECTION
    )

    glLoadIdentity()

    glOrtho(
        min_x,
        max_x,
        min_y,
        max_y,
        -1,
        1
    )

    glMatrixMode(
        GL_MODELVIEW
    )

    glLoadIdentity()

    # -----------------------------------------------------
    # RENDERING LOOP
    # -----------------------------------------------------

    while not glfw.window_should_close(
        window
    ):

        glClear(
            GL_COLOR_BUFFER_BIT
        )

        glLoadIdentity()

        # -------------------------------------------------
        # 1. GRID + COORDINATES
        # -------------------------------------------------

        draw_grid(
            min_x,
            max_x,
            min_y,
            max_y
        )

        # -------------------------------------------------
        # 2. WHITE LINE THROUGH EVERY BRESENHAM POINT
        # -------------------------------------------------

        draw_connecting_line(
            points
        )

        # -------------------------------------------------
        # 3. GREEN BRESENHAM PIXELS
        # -------------------------------------------------

        draw_bresenham_points(
            points
        )

        # -------------------------------------------------
        # 4. RED START/END POINTS
        # -------------------------------------------------

        draw_endpoints(
            x1,
            y1,
            x2,
            y2
        )

        # -------------------------------------------------
        # DISPLAY
        # -------------------------------------------------

        glfw.swap_buffers(
            window
        )

        glfw.poll_events()

    # -----------------------------------------------------
    # CLEANUP
    # -----------------------------------------------------

    glfw.terminate()


# =========================================================
# PROGRAM ENTRY POINT
# =========================================================

if __name__ == "__main__":

    main()