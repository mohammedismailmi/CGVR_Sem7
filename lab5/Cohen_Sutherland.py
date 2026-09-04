from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import sys


# ============================================================
# GLOBAL VARIABLES
# ============================================================

x1 = y1 = x2 = y2 = 0

xmin = ymin = xmax = ymax = 0

clipped_line = None


# ============================================================
# REGION CODE CONSTANTS
# ============================================================

INSIDE = 0       # 0000
LEFT = 1         # 0001
RIGHT = 2        # 0010
BOTTOM = 4       # 0100
TOP = 8          # 1000


# ============================================================
# FIND REGION CODE
# ============================================================

def compute_code(x, y):

    code = INSIDE

    # Point is to the left of window
    if x < xmin:
        code |= LEFT

    # Point is to the right of window
    elif x > xmax:
        code |= RIGHT

    # Point is below window
    if y < ymin:
        code |= BOTTOM

    # Point is above window
    elif y > ymax:
        code |= TOP

    return code


# ============================================================
# PRINT REGION CODE
# ============================================================

def print_code(code):

    return format(code, '04b')


# ============================================================
# COHEN-SUTHERLAND LINE CLIPPING
# ============================================================

def cohen_sutherland(x1, y1, x2, y2):

    code1 = compute_code(x1, y1)
    code2 = compute_code(x2, y2)

    print("\n========================================")
    print("       COHEN-SUTHERLAND ALGORITHM")
    print("========================================")

    print(
        f"\nP1 = ({x1}, {y1})"
    )

    print(
        f"P2 = ({x2}, {y2})"
    )

    print(
        f"P1 Region Code = {print_code(code1)}"
    )

    print(
        f"P2 Region Code = {print_code(code2)}"
    )


    while True:

        # ====================================================
        # CASE 1: TRIVIAL ACCEPT
        # ====================================================

        if code1 == 0 and code2 == 0:

            print("\nResult: LINE ACCEPTED")

            return (
                x1,
                y1,
                x2,
                y2
            )


        # ====================================================
        # CASE 2: TRIVIAL REJECT
        # ====================================================

        elif (code1 & code2) != 0:

            print("\nResult: LINE REJECTED")

            return None


        # ====================================================
        # CASE 3: LINE NEEDS CLIPPING
        # ====================================================

        else:

            print(
                "\nLine crosses clipping boundary..."
            )

            # Select the endpoint outside
            if code1 != 0:

                code_out = code1

            else:

                code_out = code2


            # =================================================
            # FIND INTERSECTION
            # =================================================

            # -------------------------------------------------
            # TOP
            # -------------------------------------------------

            if code_out & TOP:

                x = x1 + (
                    (x2 - x1)
                    * (ymax - y1)
                    / (y2 - y1)
                )

                y = ymax


            # -------------------------------------------------
            # BOTTOM
            # -------------------------------------------------

            elif code_out & BOTTOM:

                x = x1 + (
                    (x2 - x1)
                    * (ymin - y1)
                    / (y2 - y1)
                )

                y = ymin


            # -------------------------------------------------
            # RIGHT
            # -------------------------------------------------

            elif code_out & RIGHT:

                y = y1 + (
                    (y2 - y1)
                    * (xmax - x1)
                    / (x2 - x1)
                )

                x = xmax


            # -------------------------------------------------
            # LEFT
            # -------------------------------------------------

            elif code_out & LEFT:

                y = y1 + (
                    (y2 - y1)
                    * (xmin - x1)
                    / (x2 - x1)
                )

                x = xmin


            print(
                f"Intersection = ({x:.2f}, {y:.2f})"
            )


            # =================================================
            # REPLACE OUTSIDE POINT
            # =================================================

            if code_out == code1:

                x1 = x
                y1 = y

                code1 = compute_code(
                    x1,
                    y1
                )

            else:

                x2 = x
                y2 = y

                code2 = compute_code(
                    x2,
                    y2
                )


# ============================================================
# DRAW TEXT
# ============================================================

def draw_text(x, y, text):

    glRasterPos2f(
        x,
        y
    )

    for character in text:

        glutBitmapCharacter(
            GLUT_BITMAP_HELVETICA_12,
            ord(character)
        )


# ============================================================
# DRAW GRID
# ============================================================

def draw_grid():

    # Dark gray grid
    glColor3f(
        0.15,
        0.15,
        0.15
    )

    glBegin(GL_LINES)

    for i in range(-20, 21):

        # Vertical
        glVertex2f(
            i,
            -20
        )

        glVertex2f(
            i,
            20
        )

        # Horizontal
        glVertex2f(
            -20,
            i
        )

        glVertex2f(
            20,
            i
        )

    glEnd()


    # ========================================================
    # AXES
    # ========================================================

    glColor3f(
        0.65,
        0.65,
        0.65
    )

    glLineWidth(2)

    glBegin(GL_LINES)

    # X-axis
    glVertex2f(
        -20,
        0
    )

    glVertex2f(
        20,
        0
    )

    # Y-axis
    glVertex2f(
        0,
        -20
    )

    glVertex2f(
        0,
        20
    )

    glEnd()

    glLineWidth(1)


# ============================================================
# DRAW CLIPPING WINDOW
# ============================================================

def draw_clipping_window():

    # White clipping rectangle
    glColor3f(
        1.0,
        1.0,
        1.0
    )

    glLineWidth(3)

    glBegin(GL_LINE_LOOP)

    glVertex2f(
        xmin,
        ymin
    )

    glVertex2f(
        xmax,
        ymin
    )

    glVertex2f(
        xmax,
        ymax
    )

    glVertex2f(
        xmin,
        ymax
    )

    glEnd()

    glLineWidth(1)


    # Window labels

    glColor3f(
        0.8,
        0.8,
        0.8
    )

    draw_text(
        xmin,
        ymin - 0.7,
        f"({xmin},{ymin})"
    )

    draw_text(
        xmax,
        ymax + 0.3,
        f"({xmax},{ymax})"
    )


# ============================================================
# DRAW ORIGINAL LINE
# ============================================================

def draw_original_line():

    glColor3f(
        0.0,
        1.0,
        1.0
    )

    glLineWidth(3)

    glBegin(GL_LINES)

    glVertex2f(
        x1,
        y1
    )

    glVertex2f(
        x2,
        y2
    )

    glEnd()

    glLineWidth(1)


    # End-point labels

    glColor3f(
        0.8,
        0.8,
        0.8
    )

    draw_text(
        x1 + 0.2,
        y1 + 0.2,
        f"P1 ({x1:.1f},{y1:.1f})"
    )

    draw_text(
        x2 + 0.2,
        y2 + 0.2,
        f"P2 ({x2:.1f},{y2:.1f})"
    )


# ============================================================
# DRAW CLIPPED LINE
# ============================================================

def draw_clipped_line():

    if clipped_line is None:

        return


    cx1, cy1, cx2, cy2 = clipped_line


    # Orange
    glColor3f(
        1.0,
        0.55,
        0.0
    )

    glLineWidth(5)

    glBegin(GL_LINES)

    glVertex2f(
        cx1,
        cy1
    )

    glVertex2f(
        cx2,
        cy2
    )

    glEnd()

    glLineWidth(1)


    # Clipped endpoint labels

    glColor3f(
        1.0,
        0.75,
        0.3
    )

    draw_text(
        cx1 + 0.2,
        cy1 - 0.5,
        f"({cx1:.2f},{cy1:.2f})"
    )

    draw_text(
        cx2 + 0.2,
        cy2 + 0.2,
        f"({cx2:.2f},{cy2:.2f})"
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
    # CLIPPING WINDOW
    # ========================================================

    draw_clipping_window()


    # ========================================================
    # ORIGINAL LINE
    # ========================================================

    draw_original_line()


    # ========================================================
    # CLIPPED LINE
    # ========================================================

    draw_clipped_line()


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
        "CYAN = ORIGINAL LINE"
    )


    glColor3f(
        1.0,
        0.55,
        0.0
    )

    draw_text(
        -19,
        18,
        "ORANGE = CLIPPED LINE"
    )


    glColor3f(
        1.0,
        1.0,
        1.0
    )

    draw_text(
        -19,
        17,
        "WHITE = CLIPPING WINDOW"
    )


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
# GET INPUT
# ============================================================

def get_input():

    global x1, y1
    global x2, y2

    global xmin, ymin
    global xmax, ymax

    global clipped_line


    print("\n========================================")
    print("      COHEN-SUTHERLAND CLIPPING")
    print("========================================")


    # ========================================================
    # LINE
    # ========================================================

    print("\nEnter line coordinates:")

    x1 = float(
        input("x1: ")
    )

    y1 = float(
        input("y1: ")
    )

    x2 = float(
        input("x2: ")
    )

    y2 = float(
        input("y2: ")
    )


    # ========================================================
    # CLIPPING WINDOW
    # ========================================================

    print("\nEnter clipping window:")

    xmin = float(
        input("xmin: ")
    )

    ymin = float(
        input("ymin: ")
    )

    xmax = float(
        input("xmax: ")
    )

    ymax = float(
        input("ymax: ")
    )


    # ========================================================
    # CALCULATE REGION CODES
    # ========================================================

    code1 = compute_code(
        x1,
        y1
    )

    code2 = compute_code(
        x2,
        y2
    )


    print("\n----------------------------------------")

    print(
        f"P1 Region Code = {print_code(code1)}"
    )

    print(
        f"P2 Region Code = {print_code(code2)}"
    )


    # ========================================================
    # CLIP LINE
    # ========================================================

    clipped_line = cohen_sutherland(
        x1,
        y1,
        x2,
        y2
    )


    if clipped_line is not None:

        print("\n----------------------------------------")

        print(
            "Final Clipped Line:"
        )

        print(
            f"({clipped_line[0]:.2f}, "
            f"{clipped_line[1]:.2f})"
        )

        print(
            f"({clipped_line[2]:.2f}, "
            f"{clipped_line[3]:.2f})"
        )


# ============================================================
# MAIN
# ============================================================

def main():

    get_input()


    glutInit(
        sys.argv
    )


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
        b"Experiment 5 - Cohen Sutherland Line Clipping"
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