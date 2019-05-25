from PIL import Image, ImageDraw


class PlotDraw:
    path = ''

    def __init__(self, fp, size):
        self.path = fp
        img = Image.new('RGBA', size, color='white')
        img.save(fp)
        img.close()

    def draw_image(self):
        im = Image.open(self.path)
        draw = ImageDraw.Draw(im, mode='RGBA')
        draw.line((0, 0) + im.size, fill=128)
        draw.line((0, im.size[1], im.size[0], 0), fill=128)
        del draw
