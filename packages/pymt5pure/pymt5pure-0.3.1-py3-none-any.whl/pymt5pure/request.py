from pymt5pure.helpers import escape
from pymt5pure.constants import PACKET_BODY_MAXSIZE, FIRST_PACKET_PREFIX


class Request:
    def __init__(
        self,
        cmd: str = None,
        params: dict = None,
        num: int = 0,
        flag: int = 0,
        encrypter=None,
    ):
        self.cmd = cmd
        self.params = params
        self.num = num
        self.flag = flag
        self.encrypter = encrypter

    @staticmethod
    def format_body(cmd: str, params: dict = None) -> str:
        def wrapper():
            yield cmd
            if params:
                for k, v in params.items():
                    yield f"{k}={escape(str(v))}"
            yield "\r\n"

        return "|".join(wrapper())

    @staticmethod
    def format_header(bodylen: int, num: int = 0, flag: int = 0) -> str:
        h1 = "{:04x}".format(bodylen)
        h2 = "{:04x}".format(num)
        h3 = str(flag)
        return f"{h1}{h2}{h3}"

    def dump(self) -> bytes:
        cls = self.__class__

        cmd = self.cmd
        body = cls.format_body(cmd, self.params).encode("utf-16le")
        if self.encrypter:
            body = self.encrypter(body)

        bodylen = len(body)
        assert bodylen < PACKET_BODY_MAXSIZE

        header = cls.format_header(bodylen, self.num, self.flag)
        return header.encode() + body


class FirstRequest(Request):
    def dump(self) -> bytes:
        return FIRST_PACKET_PREFIX.encode() + super().dump()


class Ping(Request):
    def dump(self) -> bytes:
        header = self.__class__.format_header(0, self.num, self.flag)
        return header.encode()
