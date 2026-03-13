"""
兼容 OpenGL 2.1 的 Image 类
用于在 macOS 等只支持 OpenGL 2.1 的系统上显示背景图片
"""
from OpenGL import GL
import numpy as np
from PIL import Image as PILImage

def create_texture(imagePath: str):
    """创建 OpenGL 纹理"""
    img = PILImage.open(imagePath)
    img = img.convert('RGBA')
    img_data = img.tobytes()
    
    texture = GL.glGenTextures(1)
    GL.glBindTexture(GL.GL_TEXTURE_2D, texture)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
    GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, img.width, img.height, 0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, img_data)
    return texture

def create_program_gl21(vertex_shader, frag_shader):
    """创建 OpenGL 2.1 兼容的着色器程序"""
    def compile_shader(shader_source, shader_type):
        shader = GL.glCreateShader(shader_type)
        GL.glShaderSource(shader, shader_source)
        GL.glCompileShader(shader)
        
        if not GL.glGetShaderiv(shader, GL.GL_COMPILE_STATUS):
            error = GL.glGetShaderInfoLog(shader)
            GL.glDeleteShader(shader)
            raise RuntimeError(f"Shader compilation error: {error}")
        return shader
    
    vs = compile_shader(vertex_shader, GL.GL_VERTEX_SHADER)
    fs = compile_shader(frag_shader, GL.GL_FRAGMENT_SHADER)
    
    program = GL.glCreateProgram()
    GL.glAttachShader(program, vs)
    GL.glAttachShader(program, fs)
    GL.glLinkProgram(program)
    
    if not GL.glGetProgramiv(program, GL.GL_LINK_STATUS):
        error = GL.glGetProgramInfoLog(program)
        GL.glDeleteProgram(program)
        raise RuntimeError(f"Program linking error: {error}")
    
    GL.glDeleteShader(vs)
    GL.glDeleteShader(fs)
    
    return program

class Image:
    """兼容 OpenGL 2.1 的 Image 类"""
    
    def __init__(self, imagePath: str):
        # OpenGL 2.1 兼容的着色器（使用 #version 120）
        vertex_shader = """#version 120
        attribute vec2 a_position;
        attribute vec2 a_texCoord;
        varying vec2 v_texCoord;
        void main() {
            gl_Position = vec4(a_position, 0.0, 1.0);
            v_texCoord = a_texCoord;
        }
        """
        frag_shader = """#version 120
        varying vec2 v_texCoord;
        uniform sampler2D tex;
        uniform float opacity;
        void main() {
            vec4 col = texture2D(tex, v_texCoord);
            gl_FragColor = col;
        }
        """
        
        self.program = create_program_gl21(vertex_shader, frag_shader)
        self.texture = create_texture(imagePath)
        
        # 获取属性位置
        self.attr_position = GL.glGetAttribLocation(self.program, b"a_position")
        self.attr_texCoord = GL.glGetAttribLocation(self.program, b"a_texCoord")
        self.uniform_tex = GL.glGetUniformLocation(self.program, b"tex")
        self.uniform_opacity = GL.glGetUniformLocation(self.program, b"opacity")
        
        # 创建顶点数据
        vertices = np.array([
            -1, 1,
            -1, -1,
            1, -1,
            -1, 1,
            1, -1,
            1, 1,
        ], dtype=np.float32)
        # 翻转 Y 轴纹理坐标以修正图片反转问题
        uvs = np.array([
            0, 0,  # 左上角
            0, 1,  # 左下角
            1, 1,  # 右下角
            0, 0,  # 左上角
            1, 1,  # 右下角
            1, 0   # 右上角
        ], dtype=np.float32)
        
        # 创建 VBO
        self.vbo_vertices = GL.glGenBuffers(1)
        self.vbo_uvs = GL.glGenBuffers(1)
        
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo_vertices)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL.GL_STATIC_DRAW)
        
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo_uvs)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, uvs.nbytes, uvs, GL.GL_STATIC_DRAW)
        
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    
    def Draw(self):
        """绘制图片"""
        GL.glUseProgram(self.program)
        
        # 绑定纹理
        GL.glActiveTexture(GL.GL_TEXTURE0)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture)
        GL.glUniform1i(self.uniform_tex, 0)
        GL.glUniform1f(self.uniform_opacity, 1.0)
        
        # 绑定顶点数据
        GL.glEnableVertexAttribArray(self.attr_position)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo_vertices)
        GL.glVertexAttribPointer(self.attr_position, 2, GL.GL_FLOAT, GL.GL_FALSE, 0, None)
        
        GL.glEnableVertexAttribArray(self.attr_texCoord)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo_uvs)
        GL.glVertexAttribPointer(self.attr_texCoord, 2, GL.GL_FLOAT, GL.GL_FALSE, 0, None)
        
        # 绘制
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 6)
        
        # 清理
        GL.glDisableVertexAttribArray(self.attr_position)
        GL.glDisableVertexAttribArray(self.attr_texCoord)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        GL.glUseProgram(0)

