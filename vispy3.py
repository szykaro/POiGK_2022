from vispy import gloo, app
import numpy as np

vertex = """
    attribute vec2 position;
    attribute vec3 color;
    uniform float scale;
    uniform float alpha;
    uniform float beta;
    varying vec3 vcolor;
    
    void main(){
        float tx = cos(alpha);
        float ty = sin(alpha);
        float x = position.x * cos(beta) - position.y * sin(beta);
        float y = position.x * sin(beta) + position.y * cos(beta);
        vcolor = color;
        gl_Position = vec4((scale * x + tx), (scale * y + ty), 0, 2);
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
        self.program['scale'] = np.cos(self.clock)
        # self.program['scale'] = 1
        self.program['alpha'] = self.clock
        # self.program['alpha'] = 0
        self.program['beta'] = self.clock
        gloo.clear()
        self.update()

    def on_draw(self, event):
        self.program.draw('triangle_strip')

apka = Apka()
app.run()