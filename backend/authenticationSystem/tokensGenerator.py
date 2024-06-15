from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.crypto import constant_time_compare
from django.utils.http import base36_to_int
from django.utils import timezone
from datetime import datetime, timedelta, timezone as dt_timezone


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
     
    def _num_to_timestamp(self, num):
        """
        Converts a base36 encoded number to a timestamp.
        """
        try:
            return int(num, 36)
        except ValueError:
            raise ValueError("Invalid base36 encoded timestamp")
        
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + str(timestamp) + str(user.is_active)
        )
    
    def check_token(self, user, token):
        if not (user and token):
            return False

        try:
            # Parse the token to get timestamp and check if token has expired
            ts_b36, _ = token.split("-")
            ts = self._num_to_timestamp(ts_b36)
            token_timestamp = datetime.fromtimestamp(ts, tz=dt_timezone.utc)
             # calculate expiration time
            expiration_time= timezone.now()-timezone.timedelta(hours=5)
            # check if time limit has passed 
            if token_timestamp < expiration_time:
                return True
            else:
                  return False
            
        except (TypeError, ValueError, OverflowError):
            return False
  


class CustomPasswordResetTokenGenerator(PasswordResetTokenGenerator):
     
    def _num_to_timestamp(self, num):
        """
        Converts a base36 encoded number to a timestamp.
        """
        try:
            return int(num, 36)
        except ValueError:
            raise ValueError("Invalid base36 encoded timestamp")

    def _make_hash_value(self, user, timestamp):
        """
        Generate a hash value based on the user's pk, timestamp, and active status.
        """
        return (
            str(user.pk) + str(timestamp) + str(user.is_active)
        )

    def check_token(self, user, token):
        if not (user and token):
            return False

        try:
            # Parse the token to get timestamp and check if token has expired
            ts_b36, _ = token.split("-")
            ts = self._num_to_timestamp(ts_b36)
            token_timestamp = datetime.fromtimestamp(ts, tz=dt_timezone.utc)
             # calculate expiration time
            expiration_time= timezone.now()-timezone.timedelta(hours=2)
            # check if time limit has passed 
            if token_timestamp < expiration_time:
                return True
            else:
                  return False
            
        except (TypeError, ValueError, OverflowError):
            return False
    
# Create an instance of the custom password reset token generator
password_reset_token = CustomPasswordResetTokenGenerator()
account_activation_token = AccountActivationTokenGenerator()
