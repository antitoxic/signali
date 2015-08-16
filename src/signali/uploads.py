import uuid
import os

from django.utils.deconstruct import deconstructible

@deconstructible
class Uploader(object):

    def __init__(self, base_path='files'):
        self.base_path = base_path

    def __call__(self, instance, filename):
        filename, ext = filename.rsplit('.', 1)
        filename = "{}-{}.{}".format(filename, uuid.uuid4(), ext)
        return os.path.join(self.base_path, filename)


