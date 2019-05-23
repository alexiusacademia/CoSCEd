import drawSvg as draw


class PlotSvg:
    draw_object = {}
    width = 0
    height = 0

    def __init__(self, draw_object, w, h):
        """
        Initialization
        :param draw_object: The object to plot. Contains projected, actual and other plot features.
        :param width: Width of the canvas to plot.
        :param height: Height of the canvas to plot.
        """
        self.draw_object = draw_object
        self.width = w
        self.height = h

    def get_projected(self):
        projected = self.draw_object['projected']
        return projected

    def get_actual(self):
        actual = self.draw_object['actual']
        return actual

    def save_png(self, path=''):
        d = draw.Drawing(self.width, self.height, origin=(0, 0))
        actual = self.get_actual()

        print(actual)
