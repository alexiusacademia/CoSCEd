import drawSvg as draw


class PlotSvg:
    draw_object = {}

    def __init__(self, draw_object):
        self.draw_object = draw_object

    def get_projected(self):
        projected = self.draw_object['projected']
        return projected

    def get_actual(self):
        actual = self.draw_object['actual']