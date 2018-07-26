from django import forms
from django.conf import settings
from django.template.defaultfilters import filesizeformat
from settings.models import Settings
from .models import Application
from .boto_helper import upload
import re


def format_phone(phone):
    phone = str(phone).strip()
    numbers = re.sub('[^0-9]', '', phone)
    pattern = re.compile(r"^\(?0?\d{2}\)?\s{0,}?\d{4,5}-?\d{4}$")
    if pattern.match(phone) is None:
        return None
    # (011)98888-8888 | (011)8888-8888
    if re.match(r"^0\d{2}\d{4,5}\d{4}$", numbers):
        if len(numbers) == 11:
            # (011)8888-8888
            numbers = f"({numbers[1:3]}){numbers[3:7]}-{numbers[7:11]}"
        else:
            # (011)98888-8888
            numbers = f"({numbers[1:3]}){numbers[3:8]}-{numbers[8:12]}"
    # (11)98888-8888 | (11)8888-8888
    else:
        if len(numbers) == 10:
            # (11)8888-8888
            numbers = f"({numbers[0:2]}){numbers[2:6]}-{numbers[6:10]}"
        else:
            # (11)98888-8888
            numbers = f"({numbers[0:2]}){numbers[2:7]}-{numbers[7:11]}"
    return numbers


class ContentTypeRestrictedFileField(forms.FileField):

    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop("content_types")
        self.max_upload_size = kwargs.pop("max_upload_size")

        super().__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        file = super().clean(*args, **kwargs)

        try:
            content_type = file.content_type
            if content_type in self.content_types:
                if file.size > self.max_upload_size:
                    raise forms.ValidationError(f'O tamanho máximo permitido é {filesizeformat(self.max_upload_size)}. Tamanho atual: {filesizeformat(file.size)}')
            else:
                raise forms.ValidationError('Arquivo deve ser um PDF.')
        except AttributeError:
            pass

        return file


class ApplicationForm(forms.ModelForm):
    """ApplicationForm
    Base form for the creation and editing of applications
    """
    first_name = forms.CharField(max_length=50, required=True, label='Primeiro nome*')
    last_name = forms.CharField(max_length=50, required=True, label='Sobrenome*')
    email = forms.EmailField(required=True, label='Email*')
    file_cv = ContentTypeRestrictedFileField(
        allow_empty_file=False,
        content_types=['application/pdf'],
        max_upload_size=10485760,
        label="Arquivo com CV",
        required=False
    )

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

            'file_cv': 'Arquivo com CV',
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
            'phone': forms.fields.TextInput(attrs={'placeholder': '(42)98888-8888'}),
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

    def clean_phone(self):
        phone = str(self.cleaned_data['phone']).strip()
        numbers = re.sub('[^0-9]', '', phone)
        pattern = re.compile(r"^\(?0?\d{2}\)?\s{0,}?\d{4,5}-?\d{4}$")
        if pattern.match(phone) is None:
            message = 'Celular inválido!'
            if len(numbers) < 10:
                message = "Será que falta o DDD?"
            raise forms.ValidationError(message)
        numbers = format_phone(phone)
        return numbers

    def clean_school(self):
        school = self.cleaned_data.get('school', '')
        education = self.cleaned_data.get('education', '')
        if education not in ['Ensino Fundamental', 'Ensino Médio'] and not school:
            raise forms.ValidationError('Faculdade necessária')
        return school

    def clean_course(self):
        course = self.cleaned_data.get('course', '')
        education = self.cleaned_data.get('education', '')
        if education not in ['Ensino Fundamental', 'Ensino Médio'] and not course:
            raise forms.ValidationError('Curso necessário')
        return course

    def upload(self, data=None):
        file = data
        if not file:
            return
        try:
            url = upload(file.temporary_file_path())
        except Exception as e:
            raise forms.ValidationError("Erro fazendo upload do arquivo")
        return url

    def clean(self):
        data = super().clean()
        if data.get('cv_type') == 'UP':
            file = data.get('file_cv', None)
            url = self.upload(file)
            if not url:
                self.add_error('cv_type', 'Nenhum arquivo encontrado')
                raise forms.ValidationError('Nenhum arquivo encontrado')
            data['cv'] = url
        return data

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
