from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from bonde.models import User as UserBonde


has_superuser = ['igor@nossas.org', 'igr.exe@gmail.com']


class BondePermissionAdapter(DefaultSocialAccountAdapter):

    # def save_user(self, request, sociallogin, form=None):
    #     return super().save_user(request, sociallogin, form)

    def save_user(self, request, sociallogin, form=None):
        user = super(BondePermissionAdapter, self).save_user(request, sociallogin, form)

        bonde_user = UserBonde.objects.get(email=user.email)

        if bonde_user:
            user.is_staff = True
            user.is_superuser = bonde_user.is_admin or False
            user.save()
        
        return user

    # def save_user(self, request, user, form, commit=True):


    #     user = super(BondePermissionAdapter, self).save_user(request, user, form, commit=False)

    #     import ipdb;ipdb.set_trace()

    #     if user.email in has_superuser:
    #         user.is_staff = True
    #         user.save()
        
    #     return user

        #     def save_user(self, request, user, form, commit=True):
        # """
        # Saves a new `User` instance using information provided in the
        # signup form.
        # """
        # from .utils import user_email, user_field, user_username

        # data = form.cleaned_data
        # first_name = data.get("first_name")
        # last_name = data.get("last_name")
        # email = data.get("email")
        # username = data.get("username")
        # user_email(user, email)
        # user_username(user, username)
        # if first_name:
        #     user_field(user, "first_name", first_name)
        # if last_name:
        #     user_field(user, "last_name", last_name)
        # if "password1" in data:
        #     user.set_password(data["password1"])
        # else:
        #     user.set_unusable_password()
        # self.populate_username(request, user)
        # if commit:
        #     # Ability not to commit makes it easier to derive from
        #     # this adapter by adding
        #     user.save()
        # return user

        # return super().save_user(request, user, form, commit)