from typing import Mapping
from pyDes import des, ECB, PAD_PKCS5


class LoginException(Exception):
    def __init__(self, errorInfo: str):
        super().__init__(self)
        self.errorInfo = errorInfo

    def __str__(self) -> str:
        return self.errorInfo


def desEncrypt(string: str, key: str):
    if len(key) > 8:
        key = key[:8]
    encryptor = des(key, ECB, key, padmode=PAD_PKCS5)
    result_bytes = encryptor.encrypt(string.encode('utf-8'))
    return result_bytes.hex()


def getCookieString(cookies: Mapping):
    return "; ".join([(x + "=" + y) for (x, y) in cookies.items()])
