from rest_framework.throttling import UserRateThrottle

class DonationThrottle(UserRateThrottle):
    scope = 'donation'