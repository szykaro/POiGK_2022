from vispy import app, gloo

vertex = """
    attribute vec2 position;
    varying vec2 v_position;
    void main(){
        v_position = position;
        gl_Position = vec4(position, 0.0, 1.0);
    } """

fragment = """
    float distance(vec2 P, vec2 center, float radius)
    {
        return length(P-center) - radius;
    }

    varying vec2 v_position;
    void main()
    {
        const float epsilon = 0.02;

        float d = distance(v_position, vec2(0.0), 0.5);
        if (d < 0)
            gl_FragColor = vec4(0.0, 0.0, 0.0, 1.0);
        else if (d < epsilon) {
            float color = d / epsilon;
            gl_FragColor = vec4(color, color, color, 1.0);
        }
        else
            gl_FragColor = vec4(1.0, 1.0, 1.0, 1.0);
    } """


class Canvas(app.Canvas):
    def __init__(self):
        super().__init__(size=(64, 64), title="Pierwszy Vispy")
        self.show()

        self.program = gloo.Program(vertex, fragment, count=4)
        self.program['position'] = [(-1, -1), (-1, +1),
                                    (+1, -1), (+1, +1)]

    def on_draw(self, event):
        self.program.draw('triangle_strip')

c = Canvas()
app.run()