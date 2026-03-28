from django import forms
from allauth.account.forms import SignupForm
from phonenumber_field.formfields import PhoneNumberField

class CustomSignupForm(SignupForm):
    phone_number = PhoneNumberField(
        widget=forms.TextInput(attrs={
            'placeholder': '+380', 
            'class': 'input-field',
            'id': 'phone_signup'
        }),
        label='Номер телефону'
    )

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        # Зберігаємо номер телефону в сесії або профілі (опціонально)
        return user