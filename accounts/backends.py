from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

class AuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        print('here')
        UserModel = get_user_model()
        print(username)
        try:
            user = UserModel.objects.get(Q(username=username) | Q(email=username) )
            
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None