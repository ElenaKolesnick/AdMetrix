from django import forms
from .models import UserProfile
from django.contrib.auth.models import User

class ProfileUpdateForm(forms.ModelForm):
    # Поле email не входит в модель Profile, поэтому объявляем его отдельно
    email = forms.EmailField(label="Электронная почта", required=False)

    class Meta:
        model = UserProfile
        # Список полей, которые сохраняются напрямую в UserProfile
        fields = [
            'full_name', 'company_name', 'phone', 'about', 
            'avatar', 'website', 'industry', 'timezone'
        ]
        widgets = {
            'about': forms.Textarea(attrs={'rows': 3}),
            'avatar': forms.FileInput(), # Для корректной стилизации загрузки файла
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 1. Заполняем email из связанной модели User при загрузке формы
        if self.instance and self.instance.user:
            self.fields['email'].initial = self.instance.user.email

        # 2. Словарь плейсхолдеров для удобства пользователей
        placeholders = {
            'full_name': 'Имя Фамилия',
            'company_name': 'Название компании',
            'phone': '+7 (XXX) XXX-XX-XX',
            'email': 'mail@example.com',
            'website': 'https://ваш-сайт.рф',
            'industry': 'Напр. Gamedev',
            'about': 'Расскажите немного о себе или проекте...',
        }

        # 3. Автоматическое добавление Bootstrap-классов и плейсхолдеров всем полям
        for field_name, field in self.fields.items():
            # Добавляем стандартный класс Volt/Bootstrap (кроме аватара, если нужно сохранить кастомный стиль)
            if field_name != 'avatar':
                field.widget.attrs.update({'class': 'form-control'})
            
            # Добавляем плейсхолдер, если он есть в словаре
            if field_name in placeholders:
                field.widget.attrs.update({'placeholder': placeholders[field_name]})

    def save(self, commit=True):
        """Переопределяем сохранение, чтобы обновить email в модели User"""
        profile = super().save(commit=False)
        email = self.cleaned_data.get('email')
        
        if email and profile.user:
            profile.user.email = email
            if commit:
                profile.user.save()
        
        if commit:
            profile.save()
        return profile

class CSVImportForm(forms.Form):
    """Форма для импорта маркетинговых данных"""
    csv_file = forms.FileField(
        label="Выберите файл",
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.csv, .xlsx'})
    )