from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation


class AccountForm(forms.ModelForm):
    """Form for updating username, email, and optionally password."""

    new_password = forms.CharField(required=False, widget=forms.PasswordInput)
    confirm_password = forms.CharField(required=False, widget=forms.PasswordInput)

    class Meta:
        """Bind to the User model, exposing only username and email."""

        model = get_user_model()
        fields = ["username", "email"]

    def clean_new_password(self):
        """Run Django's password validators on the new password."""
        password = self.cleaned_data.get("new_password")
        if password:
            password_validation.validate_password(password, self.instance)
        return password

    def clean(self):
        """Validate that the two password fields match."""
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        if new_password and new_password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")
        return cleaned_data

    def save(self, *, commit=True):
        """Persist changes, setting the password hash when provided."""
        user = super().save(commit=False)
        if self.cleaned_data.get("new_password"):
            user.set_password(self.cleaned_data["new_password"])
        if commit:
            user.save()
        return user
