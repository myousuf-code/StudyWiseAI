"""
Shared rate limiter instance.
Import this in routers that need rate limiting.
"""
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
