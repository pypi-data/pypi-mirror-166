"""
DISCLAIMER:
    This module's code-style is based on official PHP and C# implementation.
"""

# flake8: noqa
from .symbol import *
from .group import *
from .tick import *
from .user import *
from .group import *


class MT5Api:
    def __init__(self, client) -> None:
        self.client = client

    def symbol_create(self):  # pragma:nocover
        """
        Create an object of a symbol.
        """
        raise NotImplementedError

    def symbol_add(self):  # pragma:nocover
        """
        Add or change a symbol configuration on the server.
        """
        raise NotImplementedError

    def symbol_delete(self):  # pragma:nocover
        """
        Delete a symbol configuration with the specified name.
        """
        raise NotImplementedError

    def symbol_next(self, pos: int = 0):
        """
        Get the configuration of a symbol by its index in the list of symbols
        of the platform.
        """
        resp = self.client("SYMBOL_NEXT", INDEX=pos)
        return MTSymbolAnswer.GetFromJson(resp.json)

    def symbol_total(self):
        """
        Get the number of symbols created on the trade server.
        """
        resp = self.client("SYMBOL_TOTAL")
        symbol_answer = MTSymbolTotalAnswer()
        symbol_answer.RetCode = resp.params["RETCODE"]
        symbol_answer.Total = int(resp.params["TOTAL"])
        return symbol_answer.Total

    def symbol_get(self, name: str):
        """
        Get the symbol configuration by its name.
        """
        resp = self.client("SYMBOL_GET", NAME=name)
        return MTSymbolAnswer.GetFromJson(resp.json)

    def symbol_get_group(self, symbol, group):
        """
        Get an individual configuration of a symbol for a group by the name
        of the symbol.
        """
        resp = self.client("SYMBOL_GET_GROUP", SYMBOL=symbol, GROUP=group)
        return MTSymbolAnswer.GetFromJson(resp.json)

    def tick_last(self, symbol: str):
        """
        Get the current prices of symbols.
        """
        resp = self.client("TICK_LAST", SYMBOL=symbol)
        tick_answer = MTTickAnswer()
        tick_answer.RetCode = resp.params["RETCODE"]
        tick_answer.TransId = resp.params["TRANS_ID"]
        tick_answer.ConfigJson = resp.json
        return tick_answer.GetArrayFromJson()

    def tick_last_group(self, symbol: str, group: str):
        """
        Get the current prices of symbols taking into account conversion
        for the specified group.
        """
        resp = self.client("TICK_LAST_GROUP", SYMBOL=symbol, GROUP=group)
        tick_answer = MTTickAnswer()
        tick_answer.RetCode = resp.params["RETCODE"]
        tick_answer.TransId = resp.params["TRANS_ID"]
        tick_answer.ConfigJson = resp.json
        return tick_answer.GetArrayFromJson()

    def tick_stat(self, symbol: str):
        """
        Get statistical data of symbols.
        """
        resp = self.client("TICK_STAT", SYMBOL=symbol)
        tick_stat_answer = MTTickStatAnswer()
        tick_stat_answer.RetCode = resp.params["RETCODE"]
        tick_stat_answer.TransId = resp.params["TRANS_ID"]
        tick_stat_answer.ConfigJson = resp.json
        return tick_stat_answer.GetArrayFromJson()

    def group_add(self, *kwargs):
        """
        Add or change a group configuration on the server.
        """
        return self.client("GROUP_ADD", BODY_TEXT=group).json

    def group_delete(self):
        """
        Delete a group configuration with the specified name.
        """
        raise NotImplementedError

    def group_total(self):  # pragma:nocover
        """
        Get the number of groups created on the trade server.
        """
        resp = self.client("GROUP_TOTAL")
        answer = MTGroupTotalAnswer()
        answer.RetCode = resp.params["RETCODE"]
        answer.Total = int(resp.params["TOTAL"])
        return answer.Total

    def group_next(self):  # pragma:nocover
        """
        Get the group configuration by its index in the list of groups of
        the platform.
        """
        raise NotImplementedError

    def group_get(self):  # pragma:nocover
        """
        Get the group configuration by its name.
        """
        raise NotImplementedError

    def user_add(self):  # pragma:nocover
        """
        Create a client account on the server.
        """
        raise NotImplementedError

    def user_update(self):  # pragma:nocover
        """
        Change a client account on the server.
        """
        raise NotImplementedError

    def user_delete(self):  # pragma:nocover
        """
        Delete a client account on the server.
        """
        raise NotImplementedError

    def user_get(self):  # pragma:nocover
        """
        Get information about a client by the login.
        """
        raise NotImplementedError

    def user_password_check(self):  # pragma:nocover
        """
        Check a client's password.
        """
        raise NotImplementedError

    def user_password_change(self):  # pragma:nocover
        """
        Change a client's password.
        """
        raise NotImplementedError

    def user_account_get(self):  # pragma:nocover
        """
        Get information about a client's trading account.
        """
        raise NotImplementedError

    def user_logins(self, group: str):
        """
        Returns a list of logins of the clients who are included in
        the specified group.
        """
        resp = self.client("USER_LOGINS", GROUP=group)
        answer = MTUserLoginsAnswer()
        answer.RetCode = resp.params["RETCODE"]
        answer.ConfigJson = resp.json
        return answer.GetFromJson()
