SOCKET_RECV_BUFSIZE = 2048

# The serial number must be within the range 0000-FFFF:
# 0-3FFF (0-16383) — client commands.
MAX_CLIENT_COMMAND = 16383

PACKET_HEADER_SIZE = 9
PACKET_BODY_MAXSIZE = 65 * 1024 * 1024

# the flag indicates that the command has an extension.
# If a command does not fit into one packet, it is split into several packets,
# in each of which except for the last one this flag is transmitted.
PACKET_FLAG_HAS_EXTENSION = 1

FIRST_PACKET_PREFIX = "MT5WEBAPI"

ACCOUNT_TYPE_MANAGER = "MANAGER"

CRYPT_NONE = "NONE"
CRYPT_AES = "AES256OFB"

# commands
CMD_PING = "PING"
CMD_AUTH_START = "AUTH_START"
CMD_AUTH_ANSWER = "AUTH_ANSWER"

MT_RET_OK = 0
