import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
import sys
import math


# =========================================================
# MIDPOINT CIRCLE DRAWING ALGORITHM
# =========================================================

def midpoint_circle(xc, yc, r):

    points = []

    x = 0
    y = r

    # Initial decision parameter
    p = 1 - r

    while x <= y:

        # -------------------------------------------------
        # Eight-way symmetry
        # -------------------------------------------------

        symmetric_points = [

            (xc + x, yc + y),
            (xc - x, yc + y),

            (xc + x, yc - y),
            (xc - x, yc - y),

            (xc + y, yc + x),
            (xc - y, yc + x),

            (xc + y, yc - x),
            (xc - y, yc - x)

        ]

        # Add points
        for point in symmetric_points:

            if point not in points:
                points.append(point)

        # -------------------------------------------------
        # Update decision parameter
        # -------------------------------------------------

        if p < 0:

            # Choose East pixel
            p = p + 2 * x + 3

        else:

            # Choose South-East pixel
            p = p + 2 * (x - y) + 5

            y -= 1

        x += 1

    return points


# =========================================================
# CALCULATE GRAPH RANGE
# =========================================================

def calculate_range(xc, yc, r):

    # Circle boundaries
    min_x = xc - r
    max_x = xc + r

    min_y = yc - r
    max_y = yc + r

    # Add padding
    padding = max(2, r * 0.15)

    min_x -= padding
    max_x += padding

    min_y -= padding
    max_y += padding

    return (
        min_x,
        max_x,
        min_y,
        max_y
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
    # Vertical lines
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
    # Horizontal lines
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

    # X-axis
    if min_y <= 0 <= max_y:

        glVertex2f(
            min_x,
            0
        )

        glVertex2f(
            max_x,
            0
        )

    # Y-axis
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
    # X labels
    # -----------------------------------------------------

    x = start_x

    while x <= max_x:

        label = format_number(x)

        if min_y <= 0 <= max_y:

            draw_text(
                x + range_x * 0.005,
                -range_y * 0.035,
                label
            )

        else:

            draw_text(
                x + range_x * 0.005,
                min_y + range_y * 0.02,
                label
            )

        x += spacing_x

    # -----------------------------------------------------
    # Y labels
    # -----------------------------------------------------

    y = start_y

    while y <= max_y:

        label = format_number(y)

        if min_x <= 0 <= max_x:

            draw_text(
                -range_x * 0.045,
                y + range_y * 0.005,
                label
            )

        else:

            draw_text(
                min_x + range_x * 0.01,
                y + range_y * 0.005,
                label
            )

        y += spacing_y


# =========================================================
# DRAW CIRCLE PIXELS
# =========================================================

def draw_circle_points(points):

    glColor3f(
        0.0,
        1.0,
        0.0
    )

    glPointSize(7.0)

    glBegin(GL_POINTS)

    for x, y in points:

        glVertex2f(
            x,
            y
        )

    glEnd()


# =========================================================
# DRAW CIRCLE CONNECTION
# =========================================================

def draw_circle_connection(points, xc, yc):

    # Sort points by angle around the center
    sorted_points = sorted(
        points,
        key=lambda p: math.atan2(
            p[1] - yc,
            p[0] - xc
        )
    )

    glColor3f(
        1.0,
        1.0,
        1.0
    )

    glLineWidth(3.0)

    glBegin(GL_LINE_LOOP)

    for x, y in sorted_points:

        glVertex2f(
            x,
            y
        )

    glEnd()


# =========================================================
# DRAW CENTER
# =========================================================

def draw_center(xc, yc):

    glColor3f(
        1.0,
        0.0,
        0.0
    )

    glPointSize(12.0)

    glBegin(GL_POINTS)

    glVertex2f(
        xc,
        yc
    )

    glEnd()


# =========================================================
# DRAW RADIUS LINE
# =========================================================

def draw_radius_line(xc, yc, r):

    glColor3f(
        1.0,
        0.5,
        0.0
    )

    glLineWidth(2.0)

    glBegin(GL_LINES)

    glVertex2f(
        xc,
        yc
    )

    glVertex2f(
        xc + r,
        yc
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
    print("     MIDPOINT CIRCLE DRAWING ALGORITHM")
    print("==========================================")
    print()

    xc = int(
        input("Enter center x (xc): ")
    )

    yc = int(
        input("Enter center y (yc): ")
    )

    r = int(
        input("Enter radius: ")
    )

    if r <= 0:

        print(
            "Radius must be greater than 0."
        )

        return

    print()

    print(
        f"Circle center: ({xc}, {yc})"
    )

    print(
        f"Radius: {r}"
    )

    # -----------------------------------------------------
    # Generate circle points
    # -----------------------------------------------------

    points = midpoint_circle(
        xc,
        yc,
        r
    )

    print()
    print(
        f"Number of raster points: {len(points)}"
    )

    print()
    print("Generated points:")

    for i, point in enumerate(points):

        print(
            f"Point {i + 1}: {point}"
        )

    # -----------------------------------------------------
    # Calculate graph range
    # -----------------------------------------------------

    (
        min_x,
        max_x,
        min_y,
        max_y
    ) = calculate_range(
        xc,
        yc,
        r
    )

    # -----------------------------------------------------
    # Initialize GLFW
    # -----------------------------------------------------

    if not glfw.init():

        print(
            "Failed to initialize GLFW"
        )

        sys.exit()

    # -----------------------------------------------------
    # Create window
    # -----------------------------------------------------

    window = glfw.create_window(
        1000,
        800,
        "Midpoint Circle Drawing",
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
    # Background
    # -----------------------------------------------------

    glClearColor(
        0.05,
        0.05,
        0.05,
        1.0
    )

    # -----------------------------------------------------
    # Dynamic coordinate system
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
    # MAIN LOOP
    # -----------------------------------------------------

    while not glfw.window_should_close(
        window
    ):

        glClear(
            GL_COLOR_BUFFER_BIT
        )

        glLoadIdentity()

        # -------------------------------------------------
        # 1. Draw grid
        # -------------------------------------------------

        draw_grid(
            min_x,
            max_x,
            min_y,
            max_y
        )

        # -------------------------------------------------
        # 2. Draw radius
        # -------------------------------------------------

        draw_radius_line(
            xc,
            yc,
            r
        )

        # -------------------------------------------------
        # 3. Draw circle connection
        # -------------------------------------------------

        draw_circle_connection(
            points,
            xc,
            yc
        )

        # -------------------------------------------------
        # 4. Draw raster pixels
        # -------------------------------------------------

        draw_circle_points(
            points
        )

        # -------------------------------------------------
        # 5. Draw center
        # -------------------------------------------------

        draw_center(
            xc,
            yc
        )

        # -------------------------------------------------
        # Display
        # -------------------------------------------------

        glfw.swap_buffers(
            window
        )

        glfw.poll_events()

    # -----------------------------------------------------
    # Cleanup
    # -----------------------------------------------------

    glfw.terminate()


# =========================================================
# PROGRAM ENTRY POINT
# =========================================================

if __name__ == "__main__":

    main()