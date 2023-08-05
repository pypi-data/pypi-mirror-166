import socket
from time import sleep, time
from uuid import uuid1
from threading import Thread

from pymt5pure.request import Request, Ping, FirstRequest
from pymt5pure.response import Response
from pymt5pure.constants import (
    ACCOUNT_TYPE_MANAGER,
    CMD_AUTH_ANSWER,
    CMD_AUTH_START,
    CRYPT_AES,
    CRYPT_NONE,
    PACKET_HEADER_SIZE,
    MAX_CLIENT_COMMAND,
)
from pymt5pure.exceptions import InvalidPacket
from pymt5pure.helpers import hash_password_rand, dump_socket_data
from pymt5pure.crypter import MT5AES


class KeepaliveMixin:
    ping_interval = 20

    def start_keepalive(self):
        self._keepalive_thread = Thread(
            target=self._keepalive_worker,
            name="MT5ConnKeepAlive",
        )
        self._keepalive_thread.start()

    def _keepalive_worker(self):
        while self.is_connected:
            self.socket.send(Ping().dump())
            sleep(self.__class__.ping_interval)


class MT5Client(KeepaliveMixin):
    def __init__(
        self,
        host: str,
        port: int = 443,
        agent: str = "WebApiExtensionExample",
        version: str = "3211",
        timeout: float = 180,
        is_crypt: bool = True,
        is_debug: bool = False,
    ) -> None:
        self.host = host
        self.port = port
        self.timeout = timeout
        self.agent = agent
        self.version = version
        self.crypter = None
        self.is_crypt = is_crypt
        self.socket = None
        self.is_authorized = False
        self.is_connected = False
        self.is_debug = is_debug

        # fills after authentication
        self.version_access = None
        self.version_trade = None

    def connect(
        self,
        username: str,
        password: str,
        account_type: str = ACCOUNT_TYPE_MANAGER,
    ):
        self.packet_num = 1
        self.socket = socket.create_connection(
            (self.host, self.port), self.timeout
        )
        self.is_connected = True

        # auth start
        self.send(
            FirstRequest(
                CMD_AUTH_START,
                dict(
                    VERSION=self.version,
                    AGENT=self.agent,
                    LOGIN=username,
                    TYPE=account_type,
                    CRYPT_METHOD=CRYPT_AES if self.is_crypt else CRYPT_NONE,
                ),
            )
        )
        startres = self.recv(is_auth=True)

        if startres.cmd != CMD_AUTH_START:
            raise InvalidPacket(
                "Response command mismatch. "
                f"expected: {CMD_AUTH_START} result: {startres.cmd}"
            )

        # request auth answer
        cli_rand = uuid1().hex
        srv_rand = startres.params["SRV_RAND"]
        srv_rand_answer = hash_password_rand(password, srv_rand)
        self.send(
            Request(
                CMD_AUTH_ANSWER,
                dict(SRV_RAND_ANSWER=srv_rand_answer, CLI_RAND=cli_rand),
            )
        )
        answer_res = self.recv(is_auth=True)

        # validate auth answer
        hash_password = hash_password_rand(password, cli_rand)
        cli_rand_answer = answer_res.params["CLI_RAND_ANSWER"]
        if hash_password != cli_rand_answer:
            raise InvalidPacket(
                "Server sent incorrect password hash "
                f"expected: {hash_password} result: {cli_rand_answer}"
            )

        # initiate crypter
        if self.is_crypt:
            self.crypter = MT5AES(
                password=password,
                crypt_rand=answer_res.params["CRYPT_RAND"],
            )

        # set client attributes
        self.is_authorized = True
        self.version_access = answer_res.params.get("VERSION_ACCESS")
        self.version_trade = answer_res.params.get("VERSION_TRADE")

        self.start_keepalive()

    def disconnect(self):
        self.is_connected = False
        self.is_authorized = False
        try:
            self.send(Request("QUIT"))

        except Exception:
            # ignore socket problems
            pass

        finally:
            self.socket.close()

    def send(self, request: Request):
        self.packet_num = (
            1 if self.packet_num >= MAX_CLIENT_COMMAND else self.packet_num + 1
        )
        request.num = self.packet_num
        data = request.dump()

        if self.is_debug:
            dump_socket_data(data, "mt5logs/%s-send.txt" % time())

        return self.socket.sendall(data)

    def recv(self, is_auth: bool = False) -> Response:
        result = b""
        while True:
            # fetch header
            header = self.socket.recv(PACKET_HEADER_SIZE)
            if len(header) == 0:
                # its ping, ignore
                continue

            if len(header) != PACKET_HEADER_SIZE:
                raise InvalidPacket("Packet header size mismatch")

            body_len = int(header[:4], base=16)
            packet_num = int(header[4:8], base=16)
            packet_flag = int(header[8:])

            # fetch body
            read_len = 0
            count_packet = 0
            body = b""
            while read_len < body_len:
                data = self.socket.recv(body_len - read_len)
                read_len += len(data)
                body += data
                count_packet += 1

            if len(body) != body_len:
                raise InvalidPacket("Packet body size mismatch")

            if self.crypter and not is_auth:
                body = self.crypter.decrypt(body)

            if packet_num != self.packet_num:
                if body_len != 0:
                    raise InvalidPacket(
                        "Packet number mismatch. "
                        f"expected: {self.packet_num} result: {packet_num}"
                    )

                # its ping, ignore
                continue

            result += body

            # read to end
            if packet_flag == 0:
                break

        if self.is_debug:
            dump_socket_data(result, "mt5logs/%s-recv.txt" % time())

        return Response(result)

    def run_command(self, cmd, params):
        self.send(
            Request(
                cmd=cmd,
                params=params,
                encrypter=self.crypter.encrypt if self.crypter else None,
            )
        )

    def __call__(self, cmd, **kwargs):
        self.run_command(cmd, kwargs)
        return self.recv()
