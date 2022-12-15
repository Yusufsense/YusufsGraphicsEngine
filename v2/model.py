import numpy as np
import glm

class Cube:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.vbo = self.get_vbo()
        self.shader_program = self.get_shader_program("default")
        self.m_model = self.get_model_matrix()
        self.vao = self.get_vao()
        self.on_init()

    def get_model_matrix(self):
        m_model = glm.mat4()
        return m_model
    
    def on_init(self):
        # Pass the projecton matrix from the camera instance and self to the shader
        self.shader_program["m_proj"].write(self.app.camera.m_proj)
        self.shader_program["m_view"].write(self.app.camera.m_view)
        self.shader_program["m_model"].write(self.m_model)
    def update(self):
        m_model = glm.rotate(self.m_model, self.app.time, glm.vec3(0,1,0))
        self.shader_program["m_model"].write(m_model)

    def render(self):
        self.update()
        self.vao.render()

    def destroy(self):
        self.vbo.release()
        self.get_shader_program.release()
        self.vao.release()

    def get_vao(self):
        vao = self.ctx.vertex_array(self.shader_program, [(self.vbo, "3f", "in_position")])
        return vao

    def get_vertex_data(self):
        verticies = [
            (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1),
            (-1, 1, -1), (-1, -1, -1), (1, -1, -1), (1, 1, -1)
        ]

        indicies = [(0, 2, 3), (0, 1, 2), (1, 7, 2), (1, 6, 7), (6, 5, 4), (4, 7, 6), (3, 4, 5), (3, 5, 0), (3, 7, 4),
                    (3, 2, 7), (0, 6, 1)]

        vertex_data = self.get_data(verticies, indicies)
        return vertex_data

    def get_data(self, verticies, indicies):
        data = [verticies[ind] for triangle in indicies for ind in triangle]
        return np.array(data, dtype="f4")

    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo

    def get_shader_program(self, shader_name):
        with open(f"shaders/{shader_name}.vert") as file:
            vertex_shader = file.read()

        with open(f"shaders/{shader_name}.frag") as file:
            fragment_shader = file.read()

        return self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
