from django import forms
from .models import New, Category


class AddNewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = "Категория не выбрана"
        self.fields['is_published'].required = False
        self.fields['is_published'].initial = True

    class Meta:
        model = New
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'class-title', 'placeholder': 'Введите заголовок'}),
            'slug': forms.TextInput(attrs={'class': 'class-url', 'placeholder': 'Введите URL'}),
            'content': forms.Textarea(attrs={'cols': 30, 'rows': 10, 'class': 'class-textarea'})
        }


    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise forms.ValidationError("Длина превышает 200 символов.")

        return title

    forms.EmailInput()