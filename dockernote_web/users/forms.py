from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.forms import (
    CharField,
    EmailField,
    Form,
    ModelChoiceField,
    ModelForm,
    PasswordInput,
    ValidationError,
)

from .models import Profile


class CustomUserCreationForm(UserCreationForm):
    """
    A custom user creation form based on Django's UserCreationForm.

    This form updates the attributes of its fields and uses a custom list of
    fields.
    """
    class Meta:
        model = User
        fields = [
            'first_name',
            'email',
            'username',
            'password1',
            'password2']
        labels = {
            'first_name': 'Imię',
            'email': 'Adres email',
            'username': 'Nazwa użytkownika',
            'password1': 'Hasło',
            'password2': 'Potwierdź hasło',
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize the form and update its fields' attributes.

        :param args: Variable length argument list.
        :param kwargs: Arbitrary keyword arguments.
        """
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class ProfileForm(ModelForm):
    """
    A form for creating and editing Profile instances.
    """
    email = EmailField(required=True)

    class Meta:
        model = Profile
        fields = ['city', 'age', 'bio', 'profile_image', 'gender']
        labels = {
            'city': 'Lokalizacja',
            'age': 'Wiek',
            'bio': 'O mnie',
            'profile_image': 'Zdjęcie profilowe',
            'gender': 'Płeć',
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize the form, set the initial email value, and update its
        fields' attributes.

        :param args: Variable length argument list.
        :param kwargs: Arbitrary keyword arguments.
        """
        super(ProfileForm, self).__init__(*args, **kwargs)
        if self.instance.user:
            self.fields['email'].initial = self.instance.user.email

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

    def save(self, commit=True):
        """
        Save the form.

        :param commit: Whether to save the form to the database.
        :type commit: bool
        :return: The saved Profile instance.
        :rtype: Profile
        """
        profile = super(ProfileForm, self).save(commit=False)
        profile.user.email = self.cleaned_data['email'].lower()
        if commit:
            profile.save()
            profile.user.save()
        return profile


class ChangePasswordForm(Form):
    """
    A form for changing a user's password.
    """
    old_password = CharField(
        label="Aktualne hasło",
        widget=PasswordInput(attrs={'autocomplete': 'current-password'}))

    new_password1 = CharField(
        label="Nowe hasło",
        widget=PasswordInput(attrs={'autocomplete': 'new-password'}),
        validators=[validate_password]
    )
    new_password2 = CharField(
        label="Potwierdź nowe hasło",
        widget=PasswordInput(attrs={'autocomplete': 'new-password'})
    )

    def __init__(self, user, *args, **kwargs):
        """
        Initialize the form and update its fields' attributes.

        :param user: The User instance whose password will be changed.
        :type user: User
        :param args: Variable length argument list.
        :param kwargs: Arbitrary keyword arguments.
        """
        self.user = user
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

    def save(self, commit=True):
        """
        Change the user's password and save the User instance.

        :param commit: Whether to save the form to the database.
        :type commit: bool
        :return: The updated User instance.
        :rtype: User
        """
        password = self.cleaned_data['new_password1']
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user

