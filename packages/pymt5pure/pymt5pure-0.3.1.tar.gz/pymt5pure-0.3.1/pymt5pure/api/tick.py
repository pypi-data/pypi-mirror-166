class MTTick:
    # symbol
    Symbol = None
    Digits = None
    # bid price
    Bid = None
    # ask price
    Ask = None
    # last price
    Last = None
    # volume
    Volume = None
    # volume with extended accuracy
    VolumeReal = None


class MTTickAnswer:
    RetCode = "-1"
    TransId = 0
    ConfigJson = None

    def GetArrayFromJson(self, obj):
        """From json get class MTTick"""
        if obj is None:
            return

        self.ConfigJson = obj

        result = []
        for item in obj:
            result.append(MTTickJson.GetFromJson(item))

        return result


class MTTickJson:
    @classmethod
    def GetFromJson(cls, obj):
        """Get MTTick from json object"""
        if obj is None:
            return

        info = MTTick()
        info.Symbol = str(obj["Symbol"])
        info.Digits = int(obj["Digits"])
        info.Bid = float(obj["Bid"])
        info.Ask = float(obj["Ask"])
        info.Last = float(obj["Last"])
        info.Volume = int(obj["Volume"])
        info.VolumeReal = float(obj.get("VolumeReal", obj["Volume"]))
        return info


class MTEnDirection:
    DIR_NONE = 0  # direction unknown
    DIR_UP = 1  # price up
    DIR_DOWN = 2  # price down
    # enumeration borders
    DIR_FIRST = DIR_NONE
    DIR_LAST = DIR_DOWN


class MTTickStat:
    """Tick stat"""

    # symbol
    Symbol = None
    # digits
    Digits = None
    # bid
    Bid = None
    BidLow = None
    BidHigh = None
    BidDir = None
    # ask
    Ask = None
    AskLow = None
    AskHigh = None
    AskDir = None
    # last price
    Last = None
    LastLow = None
    LastHigh = None
    LastDir = None
    # volume
    Volume = None
    VolumeReal = None
    VolumeLow = None
    VolumeLowReal = None
    VolumeHigh = None
    VolumeHighReal = None
    VolumeDir = None
    # trade
    TradeDeals = None
    TradeVolume = None
    TradeVolumeReal = None
    TradeTurnover = None
    TradeInterest = None
    TradeBuyOrders = None
    TradeBuyVolume = None
    TradeBuyVolumeReal = None
    TradeSellOrders = None
    TradeSellVolume = None
    TradeSellVolumeReal = None
    # price
    PriceOpen = None
    PriceClose = None
    PriceChange = None
    PriceVolatility = None
    PriceTheoretical = None


class MTTickStatAnswer:
    RetCode = "-1"
    TransId = 0
    ConfigJson = None

    def GetArrayFromJson(self):
        """From json get class MTTickStat"""
        if self.ConfigJson is None:
            return

        r = list()
        for item in self.ConfigJson:
            r.push(MTTickStatJson.GetFromJson(item))
        return r


class MTTickStatJson:
    @classmethod
    def GetFromJson(cls, obj):
        """Get MTTickState from json object"""
        if obj is None:
            return

        info = MTTickStat()
        info.Symbol = str(obj["Symbol"])
        info.Digits = int(obj["Digits"])
        info.Bid = float(obj["Bid"])
        info.BidLow = float(obj["BidLow"])
        info.BidHigh = float(obj["BidHigh"])
        info.BidDir = int(obj["BidDir"])
        info.Ask = float(obj["Ask"])
        info.AskLow = float(obj["AskLow"])
        info.AskHigh = float(obj["AskHigh"])
        info.AskDir = int(obj["AskDir"])
        info.Last = float(obj["Last"])
        info.LastLow = float(obj["LastLow"])
        info.LastHigh = float(obj["LastHigh"])
        info.LastDir = int(obj["LastDir"])

        info.Volume = int(obj["Volume"])
        info.VolumeReal = float(obj.get("VolumeReal", obj["Volume"]))

        info.VolumeLow = int(obj["VolumeLow"])
        info.VolumeLowReal = float(obj.get("VolumeLowReal", obj["VolumeLow"]))

        info.VolumeHigh = int(obj["VolumeHigh"])
        info.VolumeHighReal = float(
            obj.get("VolumeHighReal", obj["VolumeHigh"])
        )

        info.VolumeDir = int(obj["VolumeDir"])
        info.TradeDeals = int(obj["TradeDeals"])

        info.TradeVolume = int(obj["TradeVolume"])
        info.TradeVolumeReal = float(
            obj.get("TradeVolumeReal", obj["TradeVolume"])
        )

        info.TradeTurnover = int(obj["TradeTurnover"])
        info.TradeInterest = int(obj["TradeInterest"])
        info.TradeBuyOrders = int(obj["TradeBuyOrders"])

        info.TradeBuyVolume = int(obj["TradeBuyVolume"])
        info.TradeBuyVolumeReal = float(
            obj.get("TradeBuyVolumeReal", obj["TradeBuyVolume"])
        )

        info.TradeSellOrders = int(obj["TradeSellOrders"])
        info.TradeSellVolume = int(obj["TradeSellVolume"])
        info.TradeSellVolumeReal = float(
            obj.get("TradeSellVolumeReal", obj["TradeSellVolume"])
        )

        info.PriceOpen = float(obj["PriceOpen"])
        info.PriceClose = float(obj["PriceClose"])
        info.PriceChange = float(obj["PriceChange"])
        info.PriceVolatility = float(obj["PriceVolatility"])
        info.PriceTheoretical = float(obj["PriceTheoretical"])

        return info
