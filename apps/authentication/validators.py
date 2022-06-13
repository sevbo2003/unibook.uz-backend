from rest_framework.validators import ValidationError


def validate_user(string):
    if len(string) not in range(5, 15):
        raise ValidationError("Username must be between 5 and 15 characters long.")
    elif not string.isalpha():
        raise ValidationError("Username must contains only letters.")
    else:
        return string