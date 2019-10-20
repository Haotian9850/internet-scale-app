from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import re

class MajusculeValidator:
    def validate(self, password, user=None):

        caps = re.search("[A-Z]", password)
        if not caps:
            raise ValidationError(
                _("Password must contain a majuscule."),
                code='No majuscule',
                params=None,
            )

    def get_help_text(self):
        return _(
            "Password must contain a majuscule."
        )

class NumberValidator:
    def validate(self, password, user=None):

        nums = re.search("[0-9]", password)
        if not nums:
            raise ValidationError(
                _("Password must contain a number."),
                code='No number',
                params=None,
            )

    def get_help_text(self):
        return _(
            "Password must contain a number."
        )
