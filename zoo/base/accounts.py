from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class NoSignupAccountAdapter(DefaultAccountAdapter):
    """Disable open signup."""

    def is_open_for_signup(self, request):
        return False


class OpenSignupSocialAccountAdapter(DefaultSocialAccountAdapter):
    """Enable open signup."""

    def is_open_for_signup(self, request, sociallogin):
        return True
