from .protocol import MTProtocolConsts
from .retcode import MTRetCode

user_defaults = dict(
    Login=0,
    Group="",
    CertSerialNumber=0,  # certificate serial number
    Rights=0,  # MTEnUsersRights
    MQID="",
    Registration=0,  # registration datetime (filled by MT5)
    LastAccess=0,
    LastPassChange=0,
    LastIP="",
    Name="",
    Company="",
    Account="",  # external system account (exchange, ECN, etc)
    Country="",
    Language=0,  # client language (WinAPI LANGID)
    ClientID=0,
    City="",
    State="",
    ZipCode="",
    Address="",
    Phone="",
    Email="",
    ID="",  # additional ID
    Status="",
    Comment="",
    Color=0,
    PhonePassword="",
    Leverage=0,
    Agent=0,  # agent account
    MainPassword="",
    Balance=0,
    Credit=0,
    InterestRate=0,  # accumulated interest rate
    CommissionDaily=0,  # accumulated daily commission
    CommissionMonthly=0,  # accumulated monthly commission
    BalancePrevDay=0,  # previous balance state
    BalancePrevMonth=0,  # previous balance state
    EquityPrevDay=0,  # previous equity state
    EquityPrevMonth=0,  # previous equity state
    TradeAccounts="",  # external trade accounts
    LeadCampaign="",
    LeadSource="",
)


class MTUserProtocol:
    @staticmethod
    def CheckNull(user):
        """check all fields on null"""
        for k, v in user_defaults.items():
            if getattr(user, k) is None:
                setattr(user, k, v)

    @classmethod
    def GetParamAdd(cls, user):
        """Get string of params for sending to MetaTrader 5 server"""
        cls.CheckNull(user)
        return {
            MTProtocolConsts.WEB_PARAM_LOGIN: user.Login,
            MTProtocolConsts.WEB_PARAM_PASS_MAIN: user.MainPassword,
            MTProtocolConsts.WEB_PARAM_PASS_INVESTOR: user.InvestPassword,
            MTProtocolConsts.WEB_PARAM_RIGHTS: user.Rights,
            MTProtocolConsts.WEB_PARAM_GROUP: user.Group,
            MTProtocolConsts.WEB_PARAM_NAME: user.Name,
            MTProtocolConsts.WEB_PARAM_COMPANY: user.Company,
            MTProtocolConsts.WEB_PARAM_LANGUAGE: user.Language,
            MTProtocolConsts.WEB_PARAM_COUNTRY: user.Country,
            MTProtocolConsts.WEB_PARAM_CITY: user.City,
            MTProtocolConsts.WEB_PARAM_STATE: user.State,
            MTProtocolConsts.WEB_PARAM_ZIPCODE: user.ZipCode,
            MTProtocolConsts.WEB_PARAM_ADDRESS: user.Address,
            MTProtocolConsts.WEB_PARAM_PHONE: user.Phone,
            MTProtocolConsts.WEB_PARAM_EMAIL: user.Email,
            MTProtocolConsts.WEB_PARAM_ID: user.ID,
            MTProtocolConsts.WEB_PARAM_STATUS: user.Status,
            MTProtocolConsts.WEB_PARAM_COMMENT: user.Comment,
            MTProtocolConsts.WEB_PARAM_COLOR: user.Color,
            MTProtocolConsts.WEB_PARAM_PASS_PHONE: user.PhonePassword,
            MTProtocolConsts.WEB_PARAM_LEVERAGE: user.Leverage,
            MTProtocolConsts.WEB_PARAM_AGENT: user.Agent,
            MTProtocolConsts.WEB_PARAM_BALANCE: user.Balance,
            MTProtocolConsts.WEB_PARAM_BODYTEXT: "",  # MTJson::Encode($user)
        }

    def GetParamUpdate(user):
        """Get string of params for sending to MetaTrader 5 server"""
        return {
            MTProtocolConsts.WEB_PARAM_LOGIN: user.Login,
            MTProtocolConsts.WEB_PARAM_RIGHTS: user.Rights,
            MTProtocolConsts.WEB_PARAM_GROUP: user.Group,
            MTProtocolConsts.WEB_PARAM_NAME: user.Name,
            MTProtocolConsts.WEB_PARAM_COMPANY: user.Company,
            MTProtocolConsts.WEB_PARAM_LANGUAGE: user.Language,
            MTProtocolConsts.WEB_PARAM_COUNTRY: user.Country,
            MTProtocolConsts.WEB_PARAM_CITY: user.City,
            MTProtocolConsts.WEB_PARAM_STATE: user.State,
            MTProtocolConsts.WEB_PARAM_ZIPCODE: user.ZipCode,
            MTProtocolConsts.WEB_PARAM_ADDRESS: user.Address,
            MTProtocolConsts.WEB_PARAM_PHONE: user.Phone,
            MTProtocolConsts.WEB_PARAM_EMAIL: user.Email,
            MTProtocolConsts.WEB_PARAM_ID: user.ID,
            MTProtocolConsts.WEB_PARAM_STATUS: user.Status,
            MTProtocolConsts.WEB_PARAM_COMMENT: user.Comment,
            MTProtocolConsts.WEB_PARAM_COLOR: user.Color,
            MTProtocolConsts.WEB_PARAM_PASS_PHONE: user.PhonePassword,
            MTProtocolConsts.WEB_PARAM_LEVERAGE: user.Leverage,
            MTProtocolConsts.WEB_PARAM_AGENT: user.Agent,
            MTProtocolConsts.WEB_PARAM_BODYTEXT: "",  # MTJson::Encode($user));
        }


class MTEnUsersRights:
    """client rights bit flags"""

    # none
    USER_RIGHT_NONE = 0x0000000000000000
    # client allowed to connect
    USER_RIGHT_ENABLED = 0x0000000000000001
    # client allowed to change password
    USER_RIGHT_PASSWORD = 0x0000000000000002
    # client trading disabled
    USER_RIGHT_TRADE_DISABLED = 0x0000000000000004
    # client is investor
    USER_RIGHT_INVESTOR = 0x0000000000000008
    # client certificate confirmed
    USER_RIGHT_CONFIRMED = 0x0000000000000010
    # trailing stops are allowed
    USER_RIGHT_TRAILING = 0x0000000000000020
    # expert advisors are allowed
    USER_RIGHT_EXPERT = 0x0000000000000040
    # obsolete value
    USER_RIGHT_OBSOLETE = 0x0000000000000080
    # trade reports are allowed
    USER_RIGHT_REPORTS = 0x0000000000000100
    # client is readonly
    USER_RIGHT_READONLY = 0x0000000000000200
    # client must change password at next login
    USER_RIGHT_RESET_PASS = 0x0000000000000400
    # client allowed to use one-time password
    USER_RIGHT_OTP_ENABLED = 0x0000000000000800
    USER_RIGHT_CLIENT_CONFIRMED = 0x0000000000001000
    # client allowed to use sponsored by broker MetaTrader Virtual Hosting
    USER_RIGHT_VIRTUAL_HOSTING = 0x0000000000002000
    # client API are allowed
    USER_RIGHT_API_ENABLED = 0x0000000000004000
    # enumeration borders
    """
    USER_RIGHT_ENABLED |
    USER_RIGHT_PASSWORD |
    USER_RIGHT_TRAILING |
    USER_RIGHT_EXPERT |
    USER_RIGHT_REPORTS
    """
    USER_RIGHT_DEFAULT = 0x0000000000000163
    USER_RIGHT_ALL = 0x0000000000004FFF


class MTUser:
    """User record"""

    EXTERNAL_ID_MAXLEN = 32
    EXTERNAL_ID_LIMIT = 128
    # login
    Login = None
    # group
    Group = None
    # certificate serial number
    CertSerialNumber = None
    # MTEnUsersRights
    Rights = None
    # client's MetaQuotes ID
    MQID = None
    # registration datetime (filled by MT5)
    Registration = None
    # last access datetime (filled by MT5)
    LastAccess = None
    # last password change datetime (filled by MT5)
    LastPassChange = None
    # last ip-address
    LastIP = None
    # name
    Name = None
    # company
    Company = None
    # external system account (exchange, ECN, etc)
    Account = None
    # country
    Country = None
    # client language (WinAPI LANGID)
    Language = None
    # identificator by client
    ClientID = None
    # city
    City = None
    # state
    State = None
    # ZIP code
    ZipCode = None
    # address
    Address = None
    # phone
    Phone = None
    # email
    Email = None
    # additional ID
    ID = None
    # additional status
    Status = None
    # comment
    Comment = None
    # color
    Color = None
    # phone password
    PhonePassword = None
    # leverage
    Leverage = None
    # agent account
    Agent = None
    # balance & credit
    Balance = None
    Credit = None
    # accumulated interest rate
    InterestRate = None
    # accumulated daily and monthly commissions
    CommissionDaily = None
    CommissionMonthly = None
    # previous balance state
    BalancePrevDay = None
    BalancePrevMonth = None
    # previous equity state
    EquityPrevDay = None
    # previous equity state month
    EquityPrevMonth = None
    # external trade accounts
    TradeAccounts = None
    # lead campaign
    LeadCampaign = None
    # lead source
    LeadSource = None
    # main password
    MainPassword = None
    # invest password
    InvestPassword = None

    @staticmethod
    def CreateDefault():
        """Create user with default values"""
        user = MTUser()
        """
        MTEnUsersRights.USER_RIGHT_ENABLED |
        MTEnUsersRights.USER_RIGHT_PASSWORD |
        MTEnUsersRights.USER_RIGHT_TRAILING |
        MTEnUsersRights.USER_RIGHT_EXPERT |
        MTEnUsersRights.USER_RIGHT_API |
        MTEnUsersRights.USER_RIGHT_REPORTS
        """
        user.Rights = 0x1E3
        user.Leverage = 100
        user.Color = 0xFF000000

        return user

    def ExternalAccountAdd(self, gateway_id, account):
        """Add external account to trade account"""
        # checks
        if account == "":
            return MTRetCode.MT_RET_ERR_PARAMS

        if len(account) >= MTUser.EXTERNAL_ID_MAXLEN:
            return MTRetCode.MT_RET_ERR_DATA

        # add new account
        result = self.TradeAccounts + "%u=%s|" % (gateway_id, account)

        # checks and update
        if MTUser.EXTERNAL_ID_LIMIT <= len(result):
            return MTRetCode.MT_RET_ERR_DATA

        self.TradeAccounts = result
        return MTRetCode.MT_RET_OK

    def ExternalAccountUpdate(self, pos: int, gateway_id: int, account: str):
        """Update external account to trade account"""
        # checks
        if account == "":
            return MTRetCode.MT_RET_ERR_PARAMS

        if len(account) >= MTUser.EXTERNAL_ID_MAXLEN:
            return MTRetCode.MT_RET_ERR_DATA

        # update
        tokens = self.TradeAccounts.split("|")
        count = 0
        result = ""
        for token in tokens:
            if len(token) < 1:
                continue

            if pos == count:
                result += "%u=%s|" % (gateway_id, account)

            else:
                result += token + "|"

            count += 1

        # checks and update
        if pos >= count:
            return MTRetCode.MT_RET_ERR_PARAMS

        if MTUser.EXTERNAL_ID_LIMIT <= len(result):
            return MTRetCode.MT_RET_ERR_DATA

        self.TradeAccounts = result
        return MTRetCode.MT_RET_OK

    def ExternalAccountDelete(self, pos):
        """Update external account to trade account"""
        # delete
        tokens = self.TradeAccounts.split("|")
        count = 0
        result = ""
        for token in tokens:
            if len(token) < 1:
                continue
            if pos != count:
                result += token + "|"
            count += 1

        # checks and delete
        if pos >= count:
            return MTRetCode.MT_RET_ERR_PARAMS

        if MTUser.EXTERNAL_ID_LIMIT <= len(result):
            return MTRetCode.MT_RET_ERR_DATA

        self.TradeAccounts = result
        return MTRetCode.MT_RET_OK

    def ExternalAccountClear(self):
        """Clear all external accounts"""
        self.TradeAccounts = ""
        return MTRetCode.MT_RET_OK

    def ExternalAccountTotal(self):
        """Total count of external accounts"""
        tokens = self.TradeAccounts.split("|")
        count = 0
        for token in tokens:
            if len(token) < 1:
                continue
            count += 1

        return count


class MTUserAnswer:
    """Class answer from server for requests about user"""

    RetCode = "-1"
    Login = ""
    ConfigJson = None

    def GetFromJson(self):
        """From json get class MTUser"""
        obj = self.ConfigJson
        if obj is None:
            return

        result = MTUser()
        result.Login = int(obj["Login"])
        result.Group = str(obj["Group"])
        result.Rights = int(obj["Rights"])
        result.Name = str(obj["Name"])
        result.Company = str(obj["Company"])
        result.Account = str(obj["Account"])
        result.Country = str(obj["Country"])
        result.Language = int(obj["Language"])
        result.City = str(obj["City"])
        result.State = str(obj["State"])
        result.ZipCode = str(obj["ZipCode"])
        result.Address = str(obj["Address"])
        result.Phone = str(obj["Phone"])
        result.Email = str(obj["Email"])
        result.ClientID = int(obj["ClientID"])
        result.ID = str(obj["ID"])
        result.Status = str(obj["Status"])
        result.Comment = str(obj["Comment"])
        result.Color = int(obj["Color"])
        result.PhonePassword = str(obj["PhonePassword"])
        result.Leverage = int(obj["Leverage"])
        result.Agent = int(obj["Agent"])
        result.CertSerialNumber = int(obj["CertSerialNumber"])
        result.Registration = int(obj["Registration"])
        result.LastAccess = int(obj["LastAccess"])
        result.LastPassChange = int(obj["LastPassChange"])
        result.LastIP = str(obj["LastIP"])
        result.Balance = float(obj["Balance"])
        result.Credit = float(obj["Credit"])
        result.InterestRate = float(obj["InterestRate"])
        result.CommissionDaily = float(obj["CommissionDaily"])
        result.CommissionMonthly = float(obj["CommissionMonthly"])
        result.BalancePrevDay = float(obj["BalancePrevDay"])
        result.BalancePrevMonth = float(obj["BalancePrevMonth"])
        result.EquityPrevDay = float(obj["EquityPrevDay"])
        result.EquityPrevMonth = float(obj["EquityPrevMonth"])
        result.MQID = str(obj["MQID"])
        result.LeadSource = str(obj["LeadSource"])
        result.LeadCampaign = str(obj["LeadCampaign"])
        result.TradeAccounts = str(obj["TradeAccounts"])
        return result


class MTUserLoginsAnswer:
    """class answer from server for requests about user logins"""

    RetCode = "-1"
    ConfigJson = None

    def GetFromJson(self):
        """From json get array logins"""

        objects = self.ConfigJson
        if objects is None:
            return

        return [int(obj) for obj in objects]


class MTUserAccountAnswer:
    """Class answer from server for request user account get"""

    RetCode = "-1"
    Login = ""
    ConfigJson = None

    def GetFromJson(self):
        """From json get class MTUser"""
        obj = self.ConfigJson
        if obj is None:
            return

        result = MTAccount()
        result.Login = int(obj["Leverage"])
        result.CurrencyDigits = int(obj["CurrencyDigits"])
        result.Balance = float(obj["Balance"])
        result.Credit = float(obj["Credit"])
        result.Margin = float(obj["Margin"])
        result.MarginFree = float(obj["MarginFree"])
        result.MarginLevel = float(obj["MarginLevel"])
        result.MarginLeverage = int(obj["MarginLeverage"])
        result.Profit = float(obj["Profit"])
        result.Storage = float(obj["Storage"])
        result.Commission = float(obj["Commission"])
        result.Floating = float(obj["Floating"])
        result.Equity = float(obj["Equity"])
        result.SOActivation = int(obj["SOActivation"])
        result.SOTime = int(obj["SOTime"])
        result.SOLevel = float(obj["SOLevel"])
        result.SOEquity = float(obj["SOEquity"])
        result.SOMargin = float(obj["SOMargin"])

        if "Assets" in obj:
            result.Assets = float(obj["Assets"])

        if "Liabilities" in obj:
            result.Liabilities = float(obj["Liabilities"])

        result.BlockedCommission = float(obj["BlockedCommission"])
        result.BlockedProfit = float(obj["BlockedProfit"])
        result.MarginInitial = float(obj["MarginInitial"])
        result.MarginMaintenance = float(obj["MarginMaintenance"])

        return result


class MTEnSoActivation:
    """activation method"""

    ACTIVATION_NONE = 0
    ACTIVATION_MARGIN_CALL = 1
    ACTIVATION_STOP_OUT = 2

    ACTIVATION_FIRST = ACTIVATION_NONE
    ACTIVATION_LAST = ACTIVATION_STOP_OUT


class MTAccount:
    """Trade account interface"""

    Login = None
    CurrencyDigits = None
    Balance = None
    Credit = None
    Margin = None
    MarginFree = None
    MarginLevel = None
    MarginLeverage = None
    Profit = None  # floating profit
    Storage = None
    Commission = None
    Floating = None  # cumulative floating
    Equity = None
    SOActivation = None  # stop-out activation mode
    SOTime = None  # stop-out activation time
    SOLevel = None  # margin level on stop-out
    SOEquity = None  # equity on stop-out
    SOMargin = None  # margin on stop-out
    Assets = None  # account assets
    Liabilities = None  # account liabilities
    BlockedCommission = None  # blocked daily & monthly commission
    BlockedProfit = None  # blocked fixed profit
    MarginInitial = None  # account initial margin
    MarginMaintenance = None  # account maintenance margin
