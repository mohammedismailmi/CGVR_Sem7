from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import math
import sys


# ============================================================
# GLOBAL VARIABLES
# ============================================================

object_type = 0

points = []
transformed_points = []

composite_matrix = [
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1]
]


# ============================================================
# MATRIX MULTIPLICATION
# ============================================================

def matrix_multiply(A, B):

    result = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]

    for i in range(3):

        for j in range(3):

            for k in range(3):

                result[i][j] += A[i][k] * B[k][j]

    return result


# ============================================================
# MATRIX × POINT
# ============================================================

def transform_point(matrix, point):

    x = point[0]
    y = point[1]

    # Homogeneous coordinate
    vector = [
        [x],
        [y],
        [1]
    ]

    result = [
        [0],
        [0],
        [0]
    ]

    for i in range(3):

        for j in range(1):

            for k in range(3):

                result[i][j] += matrix[i][k] * vector[k][j]

    return (
        result[0][0],
        result[1][0]
    )


# ============================================================
# TRANSLATION MATRIX
# ============================================================

def translation_matrix(tx, ty):

    return [
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ]


# ============================================================
# ROTATION MATRIX
# ============================================================

def rotation_matrix(angle):

    rad = math.radians(angle)

    c = math.cos(rad)
    s = math.sin(rad)

    return [
        [c, -s, 0],
        [s,  c, 0],
        [0,  0, 1]
    ]


# ============================================================
# SCALING MATRIX
# ============================================================

def scaling_matrix(sx, sy):

    return [
        [sx, 0,  0],
        [0,  sy, 0],
        [0,  0,  1]
    ]


# ============================================================
# REFLECTION MATRIX
# ============================================================

def reflection_matrix(choice):

    # Reflection about X-axis
    if choice == 1:

        return [
            [1,  0, 0],
            [0, -1, 0],
            [0,  0, 1]
        ]

    # Reflection about Y-axis
    elif choice == 2:

        return [
            [-1, 0, 0],
            [0,  1, 0],
            [0,  0, 1]
        ]

    # Reflection about origin
    elif choice == 3:

        return [
            [-1, 0, 0],
            [0, -1, 0],
            [0,  0, 1]
        ]

    # Reflection about y = x
    elif choice == 4:

        return [
            [0, 1, 0],
            [1, 0, 0],
            [0, 0, 1]
        ]


# ============================================================
# SHEARING MATRIX
# ============================================================

def shearing_matrix(shx, shy):

    return [
        [1,   shx, 0],
        [shy, 1,   0],
        [0,   0,   1]
    ]


# ============================================================
# PRINT MATRIX
# ============================================================

def print_matrix(matrix):

    print("\nTransformation Matrix:")

    for row in matrix:

        print(
            "[ ",
            f"{row[0]:8.3f}",
            f"{row[1]:8.3f}",
            f"{row[2]:8.3f}",
            " ]"
        )


# ============================================================
# APPLY COMPOSITE MATRIX
# ============================================================

def apply_composite_transformation():

    global transformed_points

    transformed_points = []

    for point in points:

        new_point = transform_point(
            composite_matrix,
            point
        )

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

    glColor3f(
        0.18,
        0.18,
        0.18
    )

    glBegin(GL_LINES)

    for i in range(-20, 21):

        # Vertical
        glVertex2f(i, -20)
        glVertex2f(i, 20)

        # Horizontal
        glVertex2f(-20, i)
        glVertex2f(20, i)

    glEnd()


    # --------------------------------------------------------
    # AXES
    # --------------------------------------------------------

    glColor3f(
        0.75,
        0.75,
        0.75
    )

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

    glColor3f(
        0.9,
        0.9,
        0.9
    )

    draw_text(19, 0.4, "X")
    draw_text(0.3, 19, "Y")


    # --------------------------------------------------------
    # COORDINATES
    # --------------------------------------------------------

    glColor3f(
        0.55,
        0.55,
        0.55
    )

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

    glColor3f(
        0.85,
        0.85,
        0.85
    )

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

    glColor3f(
        0.85,
        0.85,
        0.85
    )

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

    glColor3f(
        0.85,
        0.85,
        0.85
    )

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

    glClear(
        GL_COLOR_BUFFER_BIT
    )

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


    glFlush()


# ============================================================
# INITIALIZATION
# ============================================================

def init():

    glClearColor(
        0.03,
        0.03,
        0.04,
        1
    )

    glMatrixMode(
        GL_PROJECTION
    )

    glLoadIdentity()

    gluOrtho2D(
        -20,
        20,
        -20,
        20
    )

    glMatrixMode(
        GL_MODELVIEW
    )

    glLoadIdentity()


# ============================================================
# INPUT OBJECT
# ============================================================

def get_object():

    global object_type
    global points


    print("\n========================================")
    print("      COMPOSITE TRANSFORMATIONS")
    print("========================================")


    print("\nChoose object:")
    print("1. Point")
    print("2. Line")
    print("3. Triangle")


    object_type = int(
        input("\nEnter choice: ")
    )


    # --------------------------------------------------------
    # POINT
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # LINE
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # TRIANGLE
    # --------------------------------------------------------

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

        print("Invalid choice!")
        sys.exit()


# ============================================================
# COMPOSITE TRANSFORMATION INPUT
# ============================================================

def get_transformations():

    global composite_matrix


    # Start with identity matrix
    composite_matrix = [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]


    print("\n========================================")
    print("       TRANSFORMATION MENU")
    print("========================================")

    print("\nAvailable transformations:")

    print("1. Translation")
    print("2. Rotation")
    print("3. Scaling")
    print("4. Reflection")
    print("5. Shearing")


    number = int(
        input("\nHow many transformations? ")
    )


    for i in range(number):

        print(
            f"\n--- Transformation {i + 1} ---"
        )

        choice = int(
            input(
                "Enter transformation choice: "
            )
        )


        # ====================================================
        # TRANSLATION
        # ====================================================

        if choice == 1:

            tx = float(
                input("Enter tx: ")
            )

            ty = float(
                input("Enter ty: ")
            )

            matrix = translation_matrix(
                tx,
                ty
            )


        # ====================================================
        # ROTATION
        # ====================================================

        elif choice == 2:

            angle = float(
                input(
                    "Enter rotation angle: "
                )
            )

            matrix = rotation_matrix(
                angle
            )


        # ====================================================
        # SCALING
        # ====================================================

        elif choice == 3:

            sx = float(
                input("Enter sx: ")
            )

            sy = float(
                input("Enter sy: ")
            )

            matrix = scaling_matrix(
                sx,
                sy
            )


        # ====================================================
        # REFLECTION
        # ====================================================

        elif choice == 4:

            print("\nReflection options:")

            print("1. X-axis")
            print("2. Y-axis")
            print("3. Origin")
            print("4. y = x")


            reflection_choice = int(
                input(
                    "Enter choice: "
                )
            )


            matrix = reflection_matrix(
                reflection_choice
            )


        # ====================================================
        # SHEARING
        # ====================================================

        elif choice == 5:

            shx = float(
                input("Enter shear in X (shx): ")
            )

            shy = float(
                input("Enter shear in Y (shy): ")
            )


            matrix = shearing_matrix(
                shx,
                shy
            )


        else:

            print("Invalid transformation!")

            continue


        # ====================================================
        # COMPOSITE MATRIX
        # ====================================================

        composite_matrix = matrix_multiply(
            matrix,
            composite_matrix
        )


    # Display final composite matrix

    print_matrix(
        composite_matrix
    )


    # Apply matrix to all points

    apply_composite_transformation()


# ============================================================
# MAIN
# ============================================================

def main():

    get_object()

    get_transformations()


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
        b"Experiment 4 - Composite Transformations"
    )


    init()


    glutDisplayFunc(
        display
    )


    glutMainLoop()


# ============================================================
# RUN PROGRAM
# ============================================================

if __name__ == "__main__":

    main()