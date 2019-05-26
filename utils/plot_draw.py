from PIL import Image, ImageDraw


class PlotDraw:
    path = ''
    size = ()
    draw_object = {}

    def __init__(self, fp, size):
        self.path = fp
        self.size = size

    def set_draw_object(self, do):
        """
        Sets the coordinates for plotting the actual line.
        :param actual: List of tuples (x, y)
        :return:
        """
        self.draw_object = do

    def draw_image(self):
        img = Image.new('RGB', self.size, color='white')

        draw = ImageDraw.Draw(img)

        projected = self.draw_object['projected']
        draw.line(projected, fill='blue', width=1)

        actual = self.draw_object['actual']
        draw.line(actual, fill='red', width=1)

        hor_grid_lines = self.draw_object['hor_grid_lines']
        for hl in hor_grid_lines:
            draw.line(hl, fill='gray', width=1)

        border_lines = self.draw_object['border_lines']
        for bl in border_lines:
            draw.line(bl, fill='black', width=2)

        vert_grid_lines = self.draw_object['vert_grid_lines']
        for vl in vert_grid_lines:
            draw.line(vl, fill='gray', width=1)

        img.save(self.path, quality=100)
        img.resize((self.size[0]*2, self.size[1]*2), Image.ANTIALIAS)
        img.close()
