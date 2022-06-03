from vispy import gloo, app
import numpy as np
from vispy.util import transforms

vertex = """
    attribute vec2 position;
    attribute vec3 color;
    uniform mat4 scale;
    uniform mat4 rot;
    uniform mat4 trans;
    uniform mat4 scale_scene;
    varying vec3 vcolor;
    
    void main(){

        vcolor = color;
        gl_Position = scale_scene * trans * rot * scale * vec4(position, 0.9, 1);
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
        self.show()

        self.clock = 0

        self.timer = app.Timer('auto', self.on_timer)

        self.program = gloo.Program(vertex, fragment, 4)

        self.program['position'] = [(-1, 1),
                                    (1, 1),
                                    (-1, -1),
                                    (1, -1)]
        self.program['color'] = [(1, 0, 0),
                                 (0, 1, 0),
                                 (0, 0, 1),
                                 (1, 1, 0)]

        self.timer.start()

    def on_timer(self, event):
        self.clock += 1/60
        self.program['scale'] = transforms.scale([np.cos(self.clock), np.cos(self.clock), 1])
        self.program['trans'] = transforms.translate([np.cos(self.clock), np.sin(self.clock), 0])
        self.program['rot'] = transforms.rotate(60 * self.clock, [0, 0, 1])
        self.program['scale_scene'] = transforms.scale([0.5, 0.5, 1])
        gloo.clear()
        self.update()

    def on_draw(self, event):
        self.program.draw('triangle_strip')

apka = Apka()
app.run()