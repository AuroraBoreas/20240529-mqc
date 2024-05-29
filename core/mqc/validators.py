import typing
from django import forms

class Flavor: pass

def validate_tasty() -> None:
    raise NotImplementedError

class FlavorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].validators.append(validate_tasty)
        self.fields['slug'].validators.append(validate_tasty)
    class Meta:
        model = Flavor

class FlavorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['title'].validators.append(validate_tasty)
        self.fields['slug'].validators.append(validate_tasty)
    class Meta:
        model = Flavor

class DateInputWidget(forms.DateInput):
    input_type = 'date'

from django.db import migrations

"class Migration(migrations.Migration):",
"\tdependencies = [",
"\t\t('${1:app_name}', '${2:op_seq}_${3:alter_user_first_name_max_length}'),",
"\t]",
"\toperations = [",
"\t\tmigrations.RunPython($1, reverse_code=$2),",
"\t]",

