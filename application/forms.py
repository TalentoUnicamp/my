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
        exclude = ['hacker']
        labels = {
            'phone': 'Telefone*',
            'gender': 'Gênero*',
            'age': 'Idade*',
            'cpf': 'CPF*',

            'education': 'Educação atual*',
            'enroll_year': 'Ano de ingresso*',
            'school': 'Faculdade*',
            'course': 'Curso*',

            'cv_type': 'Tipo de Currículo',
            'cv': 'URL do Currículo',
            'cv2_type': 'Outro tipo de Currículo',
            'cv2': 'URL de outro Currículo',

            'referrer': f'Como ficou sabendo da {settings.EVENT_NAME}*',
            'first_timer': f'É sua primeira vez na {settings.EVENT_NAME}?*',
            'dream_company': 'Qual sua empresa dos sonhos?',
            'interests': 'Quais são suas áreas de interesse?*',

            'country': 'País',
            'state': 'Estado',
            'city': 'Cidade',
            'can_move': 'Pode se mudar para trabalhar?',
            'time_slots': 'Seus horários livres',
            'extra_courses': 'Cursos ou treinamentos',
            'english_level': 'Nível de inglês',
            'excel_level': 'Nível no Excel',
            'other_languages': 'Outras línguas',
        }

        widgets = {
            'cpf': forms.fields.TextInput(attrs={'placeholder': '111.222.333-45'}),
            'referrer': forms.fields.TextInput(attrs={'placeholder': 'Amigo, Facebook, carta...'}),
            'interests': forms.fields.TextInput(attrs={'placeholder': 'Consultoria, financeiro, pesquisa...'}),
            'time_slots': forms.fields.TextInput(attrs={'placeholder': 'Seg a sexta, 9 às 17...'}),
            'extra_courses': forms.fields.TextInput(attrs={'placeholder': 'Cozinhando 101, Coursera...'}),
            'other_languages': forms.fields.TextInput(attrs={'placeholder': 'Klingon avançado'}),
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

    def clean_school(self):
        school = self.cleaned_data.get('school').strip()
        education = self.cleaned_data.get('education').strip()
        if education not in ['Ensino Fundamental', 'Ensino Médio'] and not school:
            raise forms.ValidationError('Faculdade necessária')
        return school

    def clean_course(self):
        course = self.cleaned_data.get('course').strip()
        education = self.cleaned_data.get('education').strip()
        if education not in ['Ensino Fundamental', 'Ensino Médio'] and not course:
            raise forms.ValidationError('Curso necessário')
        return course

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
