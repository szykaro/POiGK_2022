from vispy import gloo, app
import numpy as np

vertex = """
    attribute vec2 position;
    
    void main(){
        gl_Position = vec4(position, 0, 1);
    }
"""

fragment = """
    uniform vec3 color;

    void main(){
        gl_FragColor = vec4(color, 1);
    }
"""

class Apka(app.Canvas):
    def __init__(self):
        super().__init__(title='Pierwszy program w OpenGL', size=(800, 800))
        self.show()

        self.program = gloo.Program(vertex, fragment, 4)

        self.program['position'] = [(-1, 1),
                                    (1, 1),
                                    (-1, -1),
                                    (1, -1)]
        self.program['color'] = (1, 0, 0)
        gloo.clear()

        self.program.draw('triangle_strip')

    def on_key_press(self, event):
        if event.text == ' ':
            self.program['color'] = np.random.rand(3)
            self.update()

    def on_draw(self, event):
        self.program.draw('triangle_strip')

apka = Apka()
app.run()