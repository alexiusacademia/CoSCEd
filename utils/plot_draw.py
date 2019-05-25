from PIL import Image, ImageDraw


class PlotDraw:
    path = ''
    size = ()
    projected = []
    actual = []

    def __init__(self, fp, size):
        self.path = fp
        self.size = size

    def set_projected(self, projected):
        """
        Sets the coordinates for plotting the projected line.
        :param projected: List of tuples (x, y)
        :return:
        """
        self.projected = projected

    def set_actual(self, actual):
        """
        Sets the coordinates for plotting the actual line.
        :param actual: List of tuples (x, y)
        :return:
        """
        self.actual = actual

    def draw_image(self):
        img = Image.new('RGB', self.size, color='white')

        draw = ImageDraw.Draw(img)

        draw.line(self.projected, fill='blue', width=1)
        draw.line(self.actual, fill='red', width=1)

        img.save(self.path, quality=100)
        img.resize((self.size[0]*2, self.size[1]*2), Image.ANTIALIAS)
        img.close()
