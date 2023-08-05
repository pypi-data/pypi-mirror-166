class MT5Exception(Exception):
    pass


class InvalidPacket(MT5Exception):
    pass


class ResponseError(MT5Exception):
    pass
