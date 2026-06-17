from rest_framework import exceptions
from django.utils import timezone
from django.core.cache import cache

import logging

logger = logging.getLogger("api_request")


class RateLimiter:
    @classmethod
    def check(cls, user):
        key = f"rate_limit:{user.username}"
        cached_data = cache.get(key)
        now = timezone.now()

        if not cached_data:
            cached_data = {
                "requests": 0,
                "first_request_at": now,
            }
        else:
            time_passed = (now - cached_data["first_request_at"]).total_seconds()
            if cached_data["requests"] == 5 and time_passed < 60:
                wait_time = 60 - time_passed
                logger.error(
                    f"User {user.username} has reached the rate limit of 5 requests per minute, wait {wait_time} seconds"
                )
                raise exceptions.Throttled
            if time_passed >= 10:
                cached_data["requests"] = 0
                cached_data["first_request_at"] = now

        cached_data["requests"] += 1
        cache.set(key, cached_data, timeout=60)
        return True
