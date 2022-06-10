from vispy import gloo, app
import numpy as np
from vispy.util import transforms
import cv2

vertex = """
    attribute vec3 position;
    attribute vec2 texcoord;
    varying vec2 vtexcoord;
    uniform mat4 model;
    uniform mat4 view;
    uniform mat4 projection;
    
    void main(){

        vtexcoord = texcoord;
        gl_Position = projection * view * model * vec4(position, 1);
    }
"""

fragment = """
    uniform sampler2D texture;
    varying vec2 vtexcoord;

    void main(){
        gl_FragColor = texture2D(texture, vtexcoord);
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

        self.program['position'] = [[-1, -1, -1], [-1, -1, 1], [-1, 1, 1],
                                    [-1, -1, -1], [-1, 1, -1], [-1, 1, 1],
                                    [-1, -1, -1], [-1, -1, 1], [1, -1, 1],
                                    [-1, -1, -1], [1, -1, -1], [1, -1, 1],
                                    [-1, -1, -1], [-1, 1, -1], [1, 1, -1],
                                    [-1, -1, -1], [1, -1, -1], [1, 1, -1],
                                    [1, 1, 1], [1, 1, -1], [1, -1, -1],
                                    [1, 1, 1], [1, -1, 1], [1, -1, -1],
                                    [1, 1, 1], [1, 1, -1], [-1, 1, -1],
                                    [1, 1, 1], [-1, 1, 1], [-1, 1, -1],
                                    [1, 1, 1], [1, -1, 1], [-1, -1, 1],
                                    [1, 1, 1], [-1, 1, 1], [-1, -1, 1]]
        img = cv2.imread('../poigk_2021/pig.jpeg')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.program['texture'] = img

        self.program['texcoord'] = [[0, 0], [0, 1], [1, 1], [0, 0], [1, 0], [1, 1]] * 6

        self.I = np.arange(36, dtype=np.uint32)

        self.I = gloo.IndexBuffer(self.I)

        self.timer.start()

    def on_timer(self, event):
        self.clock += 1
        self.program['model'] = transforms.rotate(0.5 * self.clock, [1, 0, 0]).dot(
            transforms.rotate(self.clock, [0, 1, 0])
        )
        self.program['view'] = transforms.translate([0, 0, -4])
        self.program['projection'] = transforms.perspective(45, 1, 2, 10)
        gloo.clear()
        self.update()

    def on_draw(self, event):
        self.program.draw('triangles', self.I)

apka = Apka()
app.run()