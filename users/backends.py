from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

UserModel = get_user_model()
class EmailBackend(ModelBackend):
    """
    Authenticates against settings.AUTH_USER_MODEL.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try: 
            # This basically queries the database in search of a match ti the username
            user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username))

        # Now I need to create an exception incase there is no such username or email in the database:
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
            return

        except UserModel.MultipleObjectsReturned:
            user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username)).order_by('id').first()

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
