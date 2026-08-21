from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import sys


# ============================================================
# GLOBAL VARIABLES
# ============================================================

object_type = 0
transformation = 0

points = []
transformed_points = []


# ============================================================
# TRANSFORMATION FUNCTIONS
# ============================================================

def translation(x, y, tx, ty):
    return x + tx, y + ty


def rotation(x, y, angle):
    rad = math.radians(angle)

    new_x = x * math.cos(rad) - y * math.sin(rad)
    new_y = x * math.sin(rad) + y * math.cos(rad)

    return new_x, new_y


def scaling(x, y, sx, sy):
    return x * sx, y * sy


def reflection(x, y, choice):

    # Reflection about X-axis
    if choice == 1:
        return x, -y

    # Reflection about Y-axis
    elif choice == 2:
        return -x, y

    # Reflection about Origin
    elif choice == 3:
        return -x, -y

    # Reflection about y = x
    elif choice == 4:
        return y, x


# ============================================================
# APPLY TRANSFORMATION
# ============================================================

def apply_transformation():

    global transformed_points

    # Translation
    if transformation == 1:

        tx = float(input("Enter tx: "))
        ty = float(input("Enter ty: "))

        transformed_points = []

        for x, y in points:
            new_point = translation(x, y, tx, ty)
            transformed_points.append(new_point)


    # Rotation
    elif transformation == 2:

        angle = float(input("Enter rotation angle: "))

        transformed_points = []

        for x, y in points:
            new_point = rotation(x, y, angle)
            transformed_points.append(new_point)


    # Scaling
    elif transformation == 3:

        sx = float(input("Enter sx: "))
        sy = float(input("Enter sy: "))

        transformed_points = []

        for x, y in points:
            new_point = scaling(x, y, sx, sy)
            transformed_points.append(new_point)


    # Reflection
    elif transformation == 4:

        print("\nReflection options:")
        print("1. About X-axis")
        print("2. About Y-axis")
        print("3. About Origin")
        print("4. About y = x")

        choice = int(input("Enter choice: "))

        transformed_points = []

        for x, y in points:
            new_point = reflection(x, y, choice)
            transformed_points.append(new_point)


# ============================================================
# DRAW TEXT
# ============================================================

def draw_text(x, y, text):

    glRasterPos2f(x, y)

    for character in text:
        glutBitmapCharacter(
            GLUT_BITMAP_HELVETICA_12,
            ord(character)
        )


# ============================================================
# DRAW GRID
# ============================================================

def draw_grid():

    # --------------------------------------------------------
    # GRID
    # --------------------------------------------------------

    # Dark gray grid
    glColor3f(0.18, 0.18, 0.18)

    glBegin(GL_LINES)

    for i in range(-20, 21):

        # Vertical lines
        glVertex2f(i, -20)
        glVertex2f(i, 20)

        # Horizontal lines
        glVertex2f(-20, i)
        glVertex2f(20, i)

    glEnd()


    # --------------------------------------------------------
    # AXES
    # --------------------------------------------------------

    # Light gray axes
    glColor3f(0.75, 0.75, 0.75)

    glLineWidth(2)

    glBegin(GL_LINES)

    # X-axis
    glVertex2f(-20, 0)
    glVertex2f(20, 0)

    # Y-axis
    glVertex2f(0, -20)
    glVertex2f(0, 20)

    glEnd()

    glLineWidth(1)


    # --------------------------------------------------------
    # AXIS LABELS
    # --------------------------------------------------------

    glColor3f(0.9, 0.9, 0.9)

    draw_text(19, 0.4, "X")
    draw_text(0.3, 19, "Y")


    # --------------------------------------------------------
    # COORDINATE NUMBERS
    # --------------------------------------------------------

    glColor3f(0.55, 0.55, 0.55)

    for i in range(-20, 21):

        if i != 0:

            draw_text(
                i + 0.1,
                0.25,
                str(i)
            )

            draw_text(
                0.25,
                i + 0.1,
                str(i)
            )


# ============================================================
# DRAW POINT
# ============================================================

def draw_point(x, y):

    glPointSize(10)

    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

    glPointSize(1)

    # Coordinate label
    glColor3f(0.85, 0.85, 0.85)

    draw_text(
        x + 0.2,
        y + 0.2,
        f"({x:.1f}, {y:.1f})"
    )


# ============================================================
# DRAW LINE
# ============================================================

def draw_line(p1, p2):

    glBegin(GL_LINES)

    glVertex2f(
        p1[0],
        p1[1]
    )

    glVertex2f(
        p2[0],
        p2[1]
    )

    glEnd()


    # Coordinates
    glColor3f(0.85, 0.85, 0.85)

    draw_text(
        p1[0] + 0.2,
        p1[1] + 0.2,
        f"({p1[0]:.1f}, {p1[1]:.1f})"
    )

    draw_text(
        p2[0] + 0.2,
        p2[1] + 0.2,
        f"({p2[0]:.1f}, {p2[1]:.1f})"
    )


# ============================================================
# DRAW TRIANGLE
# ============================================================

def draw_triangle(p1, p2, p3):

    glBegin(GL_LINE_LOOP)

    glVertex2f(
        p1[0],
        p1[1]
    )

    glVertex2f(
        p2[0],
        p2[1]
    )

    glVertex2f(
        p3[0],
        p3[1]
    )

    glEnd()


    # Coordinates
    glColor3f(0.85, 0.85, 0.85)

    draw_text(
        p1[0] + 0.2,
        p1[1] + 0.2,
        f"({p1[0]:.1f}, {p1[1]:.1f})"
    )

    draw_text(
        p2[0] + 0.2,
        p2[1] + 0.2,
        f"({p2[0]:.1f}, {p2[1]:.1f})"
    )

    draw_text(
        p3[0] + 0.2,
        p3[1] + 0.2,
        f"({p3[0]:.1f}, {p3[1]:.1f})"
    )


# ============================================================
# DISPLAY
# ============================================================

def display():

    # Dark background
    glClearColor(
        0.03,
        0.03,
        0.04,
        1.0
    )

    glClear(GL_COLOR_BUFFER_BIT)

    glLoadIdentity()


    # ========================================================
    # GRID
    # ========================================================

    draw_grid()


    # ========================================================
    # ORIGINAL OBJECT
    # CYAN
    # ========================================================

    glColor3f(
        0.0,
        1.0,
        1.0
    )

    glLineWidth(3)

    if object_type == 1:

        draw_point(
            points[0][0],
            points[0][1]
        )

    elif object_type == 2:

        draw_line(
            points[0],
            points[1]
        )

    elif object_type == 3:

        draw_triangle(
            points[0],
            points[1],
            points[2]
        )


    # ========================================================
    # TRANSFORMED OBJECT
    # ORANGE
    # ========================================================

    glColor3f(
        1.0,
        0.55,
        0.0
    )

    glLineWidth(3)

    if object_type == 1:

        draw_point(
            transformed_points[0][0],
            transformed_points[0][1]
        )

    elif object_type == 2:

        draw_line(
            transformed_points[0],
            transformed_points[1]
        )

    elif object_type == 3:

        draw_triangle(
            transformed_points[0],
            transformed_points[1],
            transformed_points[2]
        )


    glLineWidth(1)


    # ========================================================
    # LEGEND
    # ========================================================

    glColor3f(
        0.0,
        1.0,
        1.0
    )

    draw_text(
        -19,
        19,
        "CYAN = ORIGINAL"
    )


    glColor3f(
        1.0,
        0.55,
        0.0
    )

    draw_text(
        -19,
        18,
        "ORANGE = TRANSFORMED"
    )


    # ========================================================
    # DISPLAY
    # ========================================================

    glFlush()


# ============================================================
# INITIALIZATION
# ============================================================

def init():

    # Dark background
    glClearColor(
        0.03,
        0.03,
        0.04,
        1.0
    )

    glMatrixMode(GL_PROJECTION)

    glLoadIdentity()

    gluOrtho2D(
        -20,
        20,
        -20,
        20
    )

    glMatrixMode(GL_MODELVIEW)

    glLoadIdentity()


# ============================================================
# INPUT
# ============================================================

def get_input():

    global object_type
    global transformation
    global points


    print("\n======================================")
    print("       2D TRANSFORMATION")
    print("======================================")


    # ========================================================
    # OBJECT SELECTION
    # ========================================================

    print("\nChoose object:")
    print("1. Point")
    print("2. Line")
    print("3. Triangle")

    object_type = int(
        input("\nEnter choice: ")
    )


    # ========================================================
    # POINT
    # ========================================================

    if object_type == 1:

        print("\nEnter point coordinates:")

        x = float(
            input("x: ")
        )

        y = float(
            input("y: ")
        )

        points = [
            (x, y)
        ]


    # ========================================================
    # LINE
    # ========================================================

    elif object_type == 2:

        print("\nEnter first point:")

        x1 = float(
            input("x1: ")
        )

        y1 = float(
            input("y1: ")
        )


        print("\nEnter second point:")

        x2 = float(
            input("x2: ")
        )

        y2 = float(
            input("y2: ")
        )

        points = [
            (x1, y1),
            (x2, y2)
        ]


    # ========================================================
    # TRIANGLE
    # ========================================================

    elif object_type == 3:

        print("\nEnter first point:")

        x1 = float(
            input("x1: ")
        )

        y1 = float(
            input("y1: ")
        )


        print("\nEnter second point:")

        x2 = float(
            input("x2: ")
        )

        y2 = float(
            input("y2: ")
        )


        print("\nEnter third point:")

        x3 = float(
            input("x3: ")
        )

        y3 = float(
            input("y3: ")
        )

        points = [
            (x1, y1),
            (x2, y2),
            (x3, y3)
        ]


    else:

        print("Invalid object choice!")
        sys.exit()


    # ========================================================
    # TRANSFORMATION SELECTION
    # ========================================================

    print("\nChoose transformation:")
    print("1. Translation")
    print("2. Rotation")
    print("3. Scaling")
    print("4. Reflection")

    transformation = int(
        input("\nEnter choice: ")
    )


    # Apply transformation
    apply_transformation()


# ============================================================
# MAIN
# ============================================================

def main():

    get_input()


    glutInit(sys.argv)

    glutInitDisplayMode(
        GLUT_SINGLE |
        GLUT_RGB
    )


    glutInitWindowSize(
        900,
        700
    )


    glutInitWindowPosition(
        100,
        50
    )


    glutCreateWindow(
        b"2D Transformations - OpenGL"
    )


    init()


    glutDisplayFunc(
        display
    )


    glutMainLoop()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()