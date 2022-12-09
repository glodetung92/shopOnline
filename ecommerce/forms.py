from allauth.account.forms import (
	SignupForm,
	LoginForm,
	ResetPasswordForm,
	CustomResetPasswordKeyForm,
	ChangePasswordForm,
	AddEmailForm,
	SetPasswordForm
)


class CustomSignupForm(SignupForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		for field in self.fields.values():
			field.widget.attrs['class'] = 'form-control'
