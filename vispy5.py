from vispy import gloo, app
import numpy as np
from vispy.util import transforms

vertex = """
    attribute vec3 position;
    attribute vec3 color;
    uniform mat4 model;
    uniform mat4 view;
    uniform mat4 projection;
    varying vec3 vcolor;
    
    void main(){

        vcolor = color;
        gl_Position = projection * view * model * vec4(position, 1);
    }
"""

fragment = """
    varying vec3 vcolor;

    void main(){
        gl_FragColor = vec4(vcolor, 1);
    }
"""

class Apka(app.Canvas):
    def __init__(self):
        super().__init__(title='Pierwszy program w OpenGL', size=(800, 800))
        gloo.set_state(depth_test=True)
        self.show()

        self.clock = 0

        self.timer = app.Timer('auto', self.on_timer)

        self.program = gloo.Program(vertex, fragment)

        self.program['position'] = [[(1, 1, 1),
                                     (-1, 1, 1),
                                     (-1, -1, 1),
                                     (1, -1, 1),
                                     (1, -1, -1),
                                     (1, 1, -1),
                                     (-1, 1, -1),
                                     (-1, -1, -1)]]
        self.program['color'] = [(1, 0, 0),
                                 (0, 1, 0),
                                 (0, 0, 1),
                                 (1, 1, 0),
                                 (1, 0, 1),
                                 (0, 1, 1),
                                 (1, 1, 1),
                                 (0, 0, 0)]
        self.I = [0, 1, 2,
                  0, 2, 3,
                  0, 3, 4,
                  0, 4, 5,
                  0, 5, 6,
                  0, 6, 1,
                  1, 6, 7,
                  1, 7, 2,
                  7, 4, 3,
                  7, 3, 2,
                  4, 7, 6,
                  4, 6, 5]

        self.I = gloo.IndexBuffer(self.I)


        self.timer.start()

    def on_timer(self, event):
        self.clock += 1
        self.program['model'] = transforms.rotate(self.clock, [1, 0, 0]).dot(
            transforms.rotate(2 * self.clock, [0, 1, 0])
        )
        self.program['view'] = transforms.translate([0, 0, -4])
        self.program['projection'] = transforms.perspective(90, 1, 2, 10)
        gloo.clear()
        self.update()

    def on_draw(self, event):
        self.program.draw('triangles', self.I)

apka = Apka()
app.run()