import string
import random
from django.db import models

class ReferralCode(models.Model):
    code = models.CharField(max_length=10, unique=True)

def generate_unique_referral_code(length=10):
    """
    Generates a unique alphanumeric referral code.
    """
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choice(characters) for _ in range(length))

    # Check if the code already exists in the database
    while ReferralCode.objects.filter(code=code).exists():
        code = ''.join(random.choice(characters) for _ in range(length))

    return code

# Usage example
referral_code = generate_unique_referral_code()
new_referral = ReferralCode(code=referral_code)
new_referral.save()