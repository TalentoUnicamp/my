from django import forms
from .models import Application
from django.conf import settings
from settings.models import Settings
import re


class ApplicationForm(forms.ModelForm):
    """ApplicationForm
    Base form for the creation and editing of applications
    """
    first_name = forms.CharField(max_length=50, required=True, label='Primeiro nome*')
    last_name = forms.CharField(max_length=50, required=True, label='Sobrenome*')
    email = forms.EmailField(required=True, label='Email*')

    class Meta:
        model = Application
        fields = ['first_name', 'last_name', 'email', 'phone', 'gender', 'age', 'university', 'enroll_year', 'diet', 'special_needs', 'shirt_size', 'shirt_style', 'cv_type', 'cv', 'cv2_type', 'cv2', 'description', 'essay']
        labels = {
            'phone': 'Telefone',
            'gender': 'Gênero*',
            'age': 'Idade*',
            'university': 'Universidade*',
            'enroll_year': 'Ano de Ingresso*',
            'diet': 'Restrição alimentar',
            'special_needs': 'Necessidades especiais',
            'shirt_size': 'Tamanho da Camisa*',
            'shirt_style': 'Estilo da Camisa*',
            'cv_type': 'Tipo de Currículo',
            'cv': 'URL do Currículo',
            'cv2_type': 'Outro tipo de Currículo',
            'cv2': 'URL de outro Currículo',
            'description': 'Eu me descreveria como...*',
            'essay': 'Por que você quer participar do {}?*'.format(settings.EVENT_NAME),
        }

        widgets = {
            'description': forms.fields.TextInput(attrs={'placeholder': 'iOS Master, Data Scientist, Hacker, Designer...'}),
            'special_needs': forms.fields.TextInput(attrs={'placeholder': 'Só responder se tiver'}),
            'diet': forms.fields.TextInput(attrs={'placeholder': 'Só responder se tiver'}),
        }

    def clean_cv(self):
        cv = self.cleaned_data['cv']
        if cv == '' or cv is None:
            return ''
        cv_type = self.cleaned_data['cv_type']
        if cv_type == 'LI' and cv.find('linkedin.com/in/') < 0:
            cv = "https://linkedin.com/in/{}".format(cv)
        if cv_type == 'GH' and cv.find('github.com/') < 0:
            cv = "https://github.com/{}".format(cv)
        if cv.find("://") < 0:
            cv = "https://{}".format(cv)
        return cv

    def clean_cv2(self):
        cv = self.cleaned_data['cv2']
        if cv == '' or cv is None:
            return ''
        cv_type = self.cleaned_data['cv2_type']
        if cv_type == 'LI' and cv.find('linkedin.com/in/') < 0:
            cv = "https://linkedin.com/in/{}".format(cv)
        if cv_type == 'GH' and cv.find('github.com/') < 0:
            cv = "https://github.com/{}".format(cv)
        if cv.find("://") < 0:
            cv = "https://{}".format(cv)
        return cv

    def clean_email(self):
        email = self.cleaned_data['email']
        pattern = re.compile("^temp_[0-9]+@email.com$")
        if pattern.match(email):
            raise forms.ValidationError('Você precisa fornecer um email válido!')
        return email

    def save(self, commit=True, hacker=None):
        data = self.cleaned_data
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']

        user = hacker.profile.user

        user.first_name = first_name
        user.last_name = last_name
        user.save()
        if email != user.email:
            user.profile.change_email(email)

        instance = forms.ModelForm.save(self, False)
        instance.hacker = hacker
        if commit:
            instance.save()
        if Settings.get().auto_admit_hackers():
            hacker.admit(False)
        return instance
