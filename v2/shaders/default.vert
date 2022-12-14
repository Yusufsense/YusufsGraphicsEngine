#version 330 core

layout (location = 0) in vec3 in_position;

// Matrix projection passed in from model.py on_init function
uniform mat4 m_proj;
uniform mat4 m_view;

void main(){
    gl_Position = m_proj * m_view * vec4(in_position, 1.0);

}