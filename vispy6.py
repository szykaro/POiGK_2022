from vispy import app, gloo
from vispy.util.transforms import *

vertex = """
attribute vec3 position;
attribute vec3 color;
uniform vec3 mask;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
varying vec4 v_color;

void main()
{
    gl_Position = projection * view * model * vec4(position, 1);
    v_color = vec4(mask * color, 1);
}
"""

fragment = """
varying vec4 v_color;
void main()
{
    gl_FragColor = v_color;
}
"""


class Canvas(app.Canvas):

    def __init__(self):
        super().__init__(size=(800, 800), title='Pierwszy Cube')
        gloo.set_state(depth_test=True)

        self.program = gloo.Program(vertex, fragment)
        self.program['position'] = [[1, 1, 1], [-1, 1, 1], [-1, -1, 1], [1, -1, 1],
                                [1, -1, -1], [1, 1, -1], [-1, 1, -1], [-1, -1, -1]]
        self.program['color'] = [[0, 1, 1], [0, 0, 1], [0, 0, 0], [0, 1, 0],
                                [1, 1, 0], [1, 1, 1], [1, 0, 1], [1, 0, 0]]
        self.program['model'] = np.eye(4, dtype=np.float32)
        self.program['view'] = translate(offset=(0, 0, -5))
        self.program['projection'] = perspective(fovy=45, aspect=1, znear=2, zfar=10)

        self.phi = 0
        self.theta = 0

        I = [0, 1, 2,
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
        self.I = gloo.IndexBuffer(I)

        L = [0, 1,
             1, 2,
             2, 3,
             3, 0,
             4, 7,
             7, 6,
             6, 5,
             5, 4,
             0, 5,
             1, 6,
             2, 7,
             3, 4]
        self.L = gloo.IndexBuffer(L)

        self.timer = app.Timer('auto', self.on_timer)
        self.timer.start()

        self.show()

    def on_draw(self, event):
        gloo.clear()
        self.program['mask'] = [1, 1, 1]
        self.program.draw('triangles', self.I)
        self.program['mask'] = [0, 0, 0]
        self.program.draw('lines', self.L)

    def on_timer(self, event):
        self.phi += 1
        self.theta += 0.5
        self.program['model'] = np.dot(rotate(angle=self.phi, axis=(0, 1, 0)),
                                       rotate(angle=self.theta, axis=(0, 0, 1)))
        self.update()


c = Canvas()
app.run()
