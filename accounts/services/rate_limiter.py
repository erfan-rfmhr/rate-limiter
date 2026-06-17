from rest_framework import exceptions
from django.utils import timezone


class RateLimiter:
    users = dict()

    @classmethod
    def check(cls, user):
        if not user.username in cls.users:
            cls.users[user.username] = {
                "requests": 0,
                "first_request_at": timezone.now(),
            }

        time_passed = (
            timezone.now() - cls.users[user.username]["first_request_at"]
        ).total_seconds()
        if cls.users[user.username]["requests"] == 5 and time_passed < 60:
            raise exceptions.Throttled
        if time_passed >= 10:
            cls.users[user.username]["requests"] = 0
            cls.users[user.username]["first_request_at"] = timezone.now()
        cls.users[user.username]["requests"] = cls.users[user.username]["requests"] + 1
        print(cls.users)
        return True
