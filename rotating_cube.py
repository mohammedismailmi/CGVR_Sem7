
# rotating_cube.py
# Modern OpenGL rotating cube for macOS (Apple Silicon)
import glfw
from OpenGL.GL import *
import numpy as np
import ctypes
import math

VERTEX_SHADER = """
#version 330 core
layout(location=0) in vec3 aPos;
layout(location=1) in vec3 aColor;

out vec3 vColor;

uniform mat4 MVP;

void main()
{
    gl_Position = MVP * vec4(aPos,1.0);
    vColor = aColor;
}
"""

FRAGMENT_SHADER = """
#version 330 core
in vec3 vColor;
out vec4 FragColor;
void main()
{
    FragColor = vec4(vColor,1.0);
}
"""

vertices = np.array([
# positions        # colors
-1,-1,-1, 1,0,0,
 1,-1,-1, 0,1,0,
 1, 1,-1, 0,0,1,
-1, 1,-1, 1,1,0,
-1,-1, 1, 1,0,1,
 1,-1, 1, 0,1,1,
 1, 1, 1, 1,1,1,
-1, 1, 1, 0.5,0.5,0.5,
],dtype=np.float32)

indices=np.array([
0,1,2,2,3,0,
4,5,6,6,7,4,
0,4,7,7,3,0,
1,5,6,6,2,1,
3,2,6,6,7,3,
0,1,5,5,4,0
],dtype=np.uint32)

def compile_shader(src,typ):
    s=glCreateShader(typ)
    glShaderSource(s,src)
    glCompileShader(s)
    if not glGetShaderiv(s,GL_COMPILE_STATUS):
        raise RuntimeError(glGetShaderInfoLog(s).decode())
    return s

def perspective(fovy,aspect,n,f):
    t=math.tan(fovy/2)
    return np.array([
        [1/(aspect*t),0,0,0],
        [0,1/t,0,0],
        [0,0,(f+n)/(n-f),(2*f*n)/(n-f)],
        [0,0,-1,0]
    ],dtype=np.float32)

def translate(z):
    m=np.eye(4,dtype=np.float32)
    m[2,3]=z
    return m

def rot_x(a):
    c,s=math.cos(a),math.sin(a)
    return np.array([[1,0,0,0],[0,c,-s,0],[0,s,c,0],[0,0,0,1]],dtype=np.float32)

def rot_y(a):
    c,s=math.cos(a),math.sin(a)
    return np.array([[c,0,s,0],[0,1,0,0],[-s,0,c,0],[0,0,0,1]],dtype=np.float32)

if not glfw.init():
    raise RuntimeError("GLFW init failed")

glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR,3)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR,3)
glfw.window_hint(glfw.OPENGL_PROFILE,glfw.OPENGL_CORE_PROFILE)
glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT,GL_TRUE)

win=glfw.create_window(800,600,"Rotating Cube",None,None)
if not win:
    glfw.terminate()
    raise RuntimeError("Window creation failed")

glfw.make_context_current(win)

vs=compile_shader(VERTEX_SHADER,GL_VERTEX_SHADER)
fs=compile_shader(FRAGMENT_SHADER,GL_FRAGMENT_SHADER)

prog=glCreateProgram()
glAttachShader(prog,vs)
glAttachShader(prog,fs)
glLinkProgram(prog)
if not glGetProgramiv(prog,GL_LINK_STATUS):
    raise RuntimeError(glGetProgramInfoLog(prog).decode())

vao=glGenVertexArrays(1)
vbo=glGenBuffers(1)
ebo=glGenBuffers(1)

glBindVertexArray(vao)

glBindBuffer(GL_ARRAY_BUFFER,vbo)
glBufferData(GL_ARRAY_BUFFER,vertices.nbytes,vertices,GL_STATIC_DRAW)

glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,ebo)
glBufferData(GL_ELEMENT_ARRAY_BUFFER,indices.nbytes,indices,GL_STATIC_DRAW)

stride=6*4
glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,stride,ctypes.c_void_p(0))
glEnableVertexAttribArray(0)
glVertexAttribPointer(1,3,GL_FLOAT,GL_FALSE,stride,ctypes.c_void_p(12))
glEnableVertexAttribArray(1)

glEnable(GL_DEPTH_TEST)

loc=glGetUniformLocation(prog,"MVP")
proj=perspective(math.radians(45),800/600,0.1,100)

while not glfw.window_should_close(win):
    glfw.poll_events()
    glClearColor(0.1,0.1,0.15,1)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    t=glfw.get_time()
    model=rot_y(t)@rot_x(t*0.7)
    view=translate(-5)
    mvp=proj@view@model

    glUseProgram(prog)
    glUniformMatrix4fv(loc,1,GL_TRUE,mvp)

    glBindVertexArray(vao)
    glDrawElements(GL_TRIANGLES,len(indices),GL_UNSIGNED_INT,None)

    glfw.swap_buffers(win)

glfw.terminate()
