from contact import apps as conttactapps
from watson import search as watson

class SignaliAreaConfig(conttactapps.ContactConfig):
    name = 'signali_location'

    def ready(self):
        Area = self.get_model("Area")
        watson.register(
            Area.objects.public_base(),
            fields=("title",),
            store=("id",)
        )
