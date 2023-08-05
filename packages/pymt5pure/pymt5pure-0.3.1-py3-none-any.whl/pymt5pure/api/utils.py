import binascii

from random import randint
from pymt5pure import helpers


class MTUtils:
    @staticmethod
    def GetFromHex(str_hex):
        """Parsing hex string to string"""
        return str_hex.decode("hex")

    @staticmethod
    def GetHexFromBytes(v: bytes) -> bytes:
        """From bytes to hex"""
        return binascii.hexlify(v).decode()

    @staticmethod
    def GetHexFromString(v: str):
        """From string to hex"""
        return binascii.hexlify(v.encode()).decode()

    @staticmethod
    def GetRandomHex(length: int) -> str:
        # Get random string hex format
        return "".join(["%02x" % randint(0, 254) for _ in range(length)])

    @staticmethod
    def GetHashFromPassword(password: str, randcode: str):
        """Get hash from password"""
        return helpers.hash_password_rand(password, randcode)

    @staticmethod
    def Quotes(v: str) -> str:
        r"""add \ for special symbols: =, |, \n, \ """
        return helpers.escape(v)

    @staticmethod
    def ToOldVolume(new_volume) -> int:
        """Convert new 8-digits volume to old 4-digits format"""
        return int(new_volume) / 10000

    @staticmethod
    def ToNewVolume(old_volume) -> int:
        """Convert old 4-digits volume to new 8-digits format"""
        return int(old_volume) * 10000
