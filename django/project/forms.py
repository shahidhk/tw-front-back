from django.forms import ModelForm, Form

from djangoAPI.models import *


class DesignProjectForm(ModelForm):
    class Meta:
        model = DesignProjectTbl
        fields = '__all__'
        # labels = {'due_back': _('New renewal date')}
        # help_texts = {'due_back': _('Enter a date between now and 4 weeks (default 3).')}
        # exclude = []
