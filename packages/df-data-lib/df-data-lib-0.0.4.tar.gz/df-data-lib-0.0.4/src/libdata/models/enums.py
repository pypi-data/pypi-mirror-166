from enum import Enum


class AccountType(str, Enum):
    free = "free"
    paid = "paid"


class Role(str, Enum):
    admin = "admin"
    customer = "customer"


class AuthType(str, Enum):
    default = "default"
    otp = "otp"


class AppType(str, Enum):
    default = "default"
    marketplace = "marketplace"
