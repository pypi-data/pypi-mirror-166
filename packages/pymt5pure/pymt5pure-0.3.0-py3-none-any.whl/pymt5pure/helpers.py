from os.path import dirname
from hashlib import md5

module_dir = dirname(__file__)
package_dir = dirname(module_dir)

HASH_CONST = b"WebAPI"


def escape(v: str):
    for a, b in (
        ("\\", r"\\\\"),
        ("=", r"\="),
        ("|", r"\|"),
        ("\n", r"\\\n"),
    ):
        v = v.replace(a, b)
    return v


def hex_to_bytes(v: str) -> bytes:
    return bytes.fromhex(v)


def hash_password(password: str) -> bytes:
    password = md5(password.encode("utf-16le")).digest()
    return md5(password + HASH_CONST).digest()


def hash_password_rand(password: str, rand: str):
    """
    Make SRV_RAND_ANSWER from PASSWORD and SRV_RAND
    Make CLI_RAND_ANSWER from PASSWORD and CLI_RAND
    """
    return md5(hash_password(password) + hex_to_bytes(rand)).hexdigest()


def hash_password_vrand(password: str, vrand: str):
    """
    Make CRYPT_IV from PASSWORD and CRYPT_RAND
    """
    r = hash_password(password)
    for i in range(16):
        # Split to 16-byte pieces
        cr = hex_to_bytes(vrand[2 * 16 * i : 2 * 16 * (i + 1)])
        r = md5(cr + r).digest()
        yield r


def dump_socket_data(v: bytes, filename: str):  # pragma: nocover
    """Dump socket response data for test and debugging"""
    with open(filename, "wb+") as f:
        f.write(v)
