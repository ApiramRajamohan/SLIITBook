from django.contrib.auth.backends import ModelBackend
from .models import Account

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