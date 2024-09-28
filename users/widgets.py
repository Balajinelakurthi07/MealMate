from django.forms import widgets
from django.utils.safestring import mark_safe

class CustomPictureImageField(widgets.FileInput):
    def render(self,name,value,attrs=None,**kwargs):
        default_html=super().render(name,value,attrs,**kwargs)
        if value is not None:
            img_html=mark_safe(f'<img src="{value.url}" width="200"/>')
        else:
            img_html = ""
        return f'{img_html}'