from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

USER_TYPE_CHOICES = (
    ('administrator', 'Administrator'),
    ('registrant', 'Registrant'),
)

class UserCreateForm(UserCreationForm):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'name', 'email', 'user_type')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = None
            field.widget.attrs.update({
                'class': 'px-3 py-2 border border-gray-400 rounded-md w-full'
            })
