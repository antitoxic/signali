import math

from PIL import Image, ImageColor
from sorl.thumbnail.engines.pil_engine import Engine


class SignaliPilEngine(Engine):
    def create(self, image, geometry, options):
        image = super().create(image, geometry, options)
        image = self.overlay(image, geometry, options)
        image = self.watermark(image, geometry, options)
        return image

    def overlay(self, image, geometry, options):
        if 'overlay' in options:
            overlay = ImageColor.getrgb(options['overlay'])
            if 'overlay_opacity' in options:
                overlay = overlay + (int(options['overlay_opacity']*255),)
            overlay = Image.new('RGBA', image.size, overlay)
            return Image.alpha_composite(image.convert('RGBA'), overlay)
        return image

    def watermark(self, image, geometry, options):
        if 'watermark' in options:
            watermark = Image.open(options['watermark'])
            watermark_overlay = Image.new('RGBA', image.size, (0,0,0,0))
            width = int(geometry[0]*0.5)
            height = watermark.size[1]*(width/watermark.size[0])
            watermark.thumbnail((width, height), Image.ANTIALIAS)
            left = int((geometry[0]-width)/2)
            top = int((geometry[1]-height)/2)
            watermark_overlay.paste(watermark, (left, top))
            return Image.alpha_composite(image.convert('RGBA'), watermark_overlay)
        return image
