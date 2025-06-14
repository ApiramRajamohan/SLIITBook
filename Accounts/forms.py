from django.contrib.auth.backends import ModelBackend
from .models import Account
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

class EmailorUsernameBackend(ModelBackend):
    def authenticate(self,request,username=None,password=None):
        if username is None:
            print("username is None")
            return None
            
        try:
            if '@' in username:
                #login with email
                user = Account.objects.get(email = username)
            else:
                #login with username
                user = Account.objects.get(username = username)
        except Account.DoesNotExist:
            print("Account is not exist")
            return None
            
        if user.check_password(password):
            return user
            
        print("Incorrect Password")
        return None

#https://docs.djangoproject.com/en/5.1/topics/auth/customizing/
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label = 'Password',widget=forms.PasswordInput)
    password2 = forms.CharField(
    label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = Account
        fields = ['email','username','Fname','Lname','Mname','Address','dob','department','Gender','role']
        
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("confirmPassword")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2
        
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
        
class LoginForm(forms.ModelForm):
    username_or_email = forms.CharField(max_length=254,label = "Username or Email")
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username_or_email = cleaned_data.get('username_or_email')
        password = cleaned_data.get("password")
        if not username_or_email:
            raise ValidationError("Incorrect Username / Email")
        if not password:
            raise ValidationError("Incorrect Password")

        return cleaned_data  

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = Account
        fields = ['email', 'username', 'Fname', 'Lname', 'Mname', 'Address', 'dob', 'department', 'Gender', 'is_active', 'is_admin']
    