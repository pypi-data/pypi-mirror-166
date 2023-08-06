from django.forms.widgets import TextInput

from django_modals.fields import FieldEx


class ColourPickerFieldEx(FieldEx):
    @staticmethod
    def get_prepended_appended_template_name(template_pack):
        return "django_modals/widgets/colour_picker_append.html"


class ColourPickerWidget(TextInput):
    template_name = 'django_modals/widgets/colour_picker.html'
    crispy_kwargs = {'field_class': 'col-sm-3',
                     'appended_text': ' ',
                     'input_size': 'input-group-sm'}
    crispy_field_class = ColourPickerFieldEx
