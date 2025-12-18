from django import forms

from .models import UserProfile


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["full_name", "company_name", "phone", "about", "avatar"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Автоматически добавляем класс Bootstrap ко всем полям
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
            self.fields[field].required = (
                False  # Делаем поля необязательными, чтобы не блокировать сохранение
            )
