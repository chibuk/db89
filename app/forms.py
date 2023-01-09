import re
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from app.models import City, Document


class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['name']

    def clean_name(self):
        data = self.cleaned_data['name']
        text = ''
        for word in data.split():
            if re.match(r'^([А-я]+)-*([А-я]+)$', word):
                text += word.title() + " "
            else:
                raise ValidationError('Только слова, пробелы или дефис.')
        return text.strip()

class DocumentForm(ModelForm):
    class Meta:
        model = Document
        fields = '__all__'