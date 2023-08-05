from pymt5pure.api.utils import MTUtils


class MTEnFillingFlags:
    """allowed filling modes flags"""

    FILL_FLAGS_NONE = 0  # none
    FILL_FLAGS_FOK = 1  # allowed FOK
    FILL_FLAGS_IOC = 2  # allowed IOC
    # flags borders
    FILL_FLAGS_FIRST = FILL_FLAGS_FOK
    FILL_FLAGS_ALL = (
        3  # MTEnFillingFlags.FILL_FLAGS_FOK | MTEnFillingFlags.FILL_FLAGS_IOC;
    )


class MTEnExpirationFlags:
    """allowed order expiration modes flags"""

    TIME_FLAGS_NONE = 0  # none
    TIME_FLAGS_GTC = 1  # allowed Good Till Cancel
    TIME_FLAGS_DAY = 2  # allowed Good Till Day
    TIME_FLAGS_SPECIFIED = 4  # allowed specified expiration date
    TIME_FLAGS_SPECIFIED_DAY = 8  # allowed specified expiration date as day
    # flags borders
    TIME_FLAGS_FIRST = TIME_FLAGS_GTC
    # TIME_FLAGS_GTC|TIME_FLAGS_DAY|TIME_FLAGS_SPECIFIED|TIME_FLAGS_SPECIFIED_DAY
    TIME_FLAGS_ALL = 15


class MTEnOrderFlags:
    """allowed order flags"""

    ORDER_FLAGS_NONE = 0  # none
    ORDER_FLAGS_MARKET = 1  # market orders
    ORDER_FLAGS_LIMIT = 2  # limit orders
    ORDER_FLAGS_STOP = 4  # stop orders
    ORDER_FLAGS_STOP_LIMIT = 8  # stop limit orders
    ORDER_FLAGS_SL = 16  # sl orders
    ORDER_FLAGS_TP = 32  # tp orders
    ORDER_FLAGS_CLOSEBY = 64  # close-by orders
    # all
    ORDER_FLAGS_FIRST = ORDER_FLAGS_MARKET
    # ORDER_FLAGS_MARKET|ORDER_FLAGS_LIMIT|ORDER_FLAGS_STOP|
    # ORDER_FLAGS_STOP_LIMIT|ORDER_FLAGS_SL|ORDER_FLAGS_TP|ORDER_FLAGS_CLOSEBY
    ORDER_FLAGS_ALL = 127


class MTEnTradeMode:
    """allowed trade modes"""

    TRADE_DISABLED = 0  # trade disabled
    TRADE_LONGONLY = 1  # only long positions allowed
    TRADE_SHORTONLY = 2  # only short positions allowed
    TRADE_CLOSEONLY = 3  # only positions closure
    TRADE_FULL = 4  # all trade operations are allowed
    # enumeration borders
    TRADE_FIRST = TRADE_DISABLED
    TRADE_LAST = TRADE_FULL


class EnSectors:
    """economical sectors"""

    SECTOR_UNDEFINED = 0
    SECTOR_BASIC_MATERIALS = 1
    SECTOR_COMMUNICATION_SERVICES = 2
    SECTOR_CONSUMER_CYCLICAL = 3
    SECTOR_CONSUMER_DEFENSIVE = 4
    SECTOR_ENERGY = 5
    SECTOR_FINANCIAL = 6
    SECTOR_HEALTHCARE = 7
    SECTOR_INDUSTRIALS = 8
    SECTOR_REAL_ESTATE = 9
    SECTOR_TECHNOLOGY = 10
    SECTOR_UTILITIES = 11
    SECTOR_CURRENCY = 12
    SECTOR_CURRENCY_CRYPTO = 13
    SECTOR_INDEXES = 14
    SECTOR_COMMODITIES = 15
    # enumeration borders
    SECTOR_FIRST = SECTOR_UNDEFINED
    SECTOR_LAST = SECTOR_COMMODITIES


class EnIndustries:
    """economical industries"""

    INDUSTRY_UNDEFINED = 0

    # Basic Materials
    INDUSTRY_AGRICULTURAL_INPUTS = 1
    INDUSTRY_ALUMINIUM = 2
    INDUSTRY_BUILDING_MATERIALS = 3
    INDUSTRY_CHEMICALS = 4
    INDUSTRY_COKING_COAL = 5
    INDUSTRY_COPPER = 6
    INDUSTRY_GOLD = 7
    INDUSTRY_LUMBER_WOOD = 8
    INDUSTRY_INDUSTRIAL_METALS = 9
    INDUSTRY_PRECIOUS_METALS = 10
    INDUSTRY_PAPER = 11
    INDUSTRY_SILVER = 12
    INDUSTRY_SPECIALTY_CHEMICALS = 13
    INDUSTRY_STEEL = 14
    # enumeration borders
    INDUSTRY_BASIC_MATERIALS_FIRST = 1
    INDUSTRY_BASIC_MATERIALS_LAST = 14
    INDUSTRY_BASIC_MATERIALS_END = 50

    # Communication Services
    INDUSTRY_ADVERTISING = 51
    INDUSTRY_BROADCASTING = 52
    INDUSTRY_GAMING_MULTIMEDIA = 53
    INDUSTRY_ENTERTAINMENT = 54
    INDUSTRY_INTERNET_CONTENT = 55
    INDUSTRY_PUBLISHING = 56
    INDUSTRY_TELECOM = 57
    # enumeration borders
    INDUSTRY_COMMUNICATION_FIRST = 51
    INDUSTRY_COMMUNICATION_LAST = 57
    INDUSTRY_COMMUNICATION_END = 100

    # Consumer Cyclical
    INDUSTRY_APPAREL_MANUFACTURING = 101
    INDUSTRY_APPAREL_RETAIL = 102
    INDUSTRY_AUTO_MANUFACTURERS = 103
    INDUSTRY_AUTO_PARTS = 104
    INDUSTRY_AUTO_DEALERSHIP = 105
    INDUSTRY_DEPARTMENT_STORES = 106
    INDUSTRY_FOOTWEAR_ACCESSORIES = 107
    INDUSTRY_FURNISHINGS = 108
    INDUSTRY_GAMBLING = 109
    INDUSTRY_HOME_IMPROV_RETAIL = 110
    INDUSTRY_INTERNET_RETAIL = 111
    INDUSTRY_LEISURE = 112
    INDUSTRY_LODGING = 113
    INDUSTRY_LUXURY_GOODS = 114
    INDUSTRY_PACKAGING_CONTAINERS = 115
    INDUSTRY_PERSONAL_SERVICES = 116
    INDUSTRY_RECREATIONAL_VEHICLES = 117
    INDUSTRY_RESIDENT_CONSTRUCTION = 118
    INDUSTRY_RESORTS_CASINOS = 119
    INDUSTRY_RESTAURANTS = 120
    INDUSTRY_SPECIALTY_RETAIL = 121
    INDUSTRY_TEXTILE_MANUFACTURING = 122
    INDUSTRY_TRAVEL_SERVICES = 123
    # enumeration borders
    INDUSTRY_CONSUMER_CYCL_FIRST = 101
    INDUSTRY_CONSUMER_CYCL_LAST = 123
    INDUSTRY_CONSUMER_CYCL_END = 150

    # Consumer Defensive
    INDUSTRY_BEVERAGES_BREWERS = 151
    INDUSTRY_BEVERAGES_NON_ALCO = 152
    INDUSTRY_BEVERAGES_WINERIES = 153
    INDUSTRY_CONFECTIONERS = 154
    INDUSTRY_DISCOUNT_STORES = 155
    INDUSTRY_EDUCATION_TRAINIG = 156
    INDUSTRY_FARM_PRODUCTS = 157
    INDUSTRY_FOOD_DISTRIBUTION = 158
    INDUSTRY_GROCERY_STORES = 159
    INDUSTRY_HOUSEHOLD_PRODUCTS = 160
    INDUSTRY_PACKAGED_FOODS = 161
    INDUSTRY_TOBACCO = 162
    # enumeration borders
    INDUSTRY_CONSUMER_DEF_FIRST = 151
    INDUSTRY_CONSUMER_DEF_LAST = 162
    INDUSTRY_CONSUMER_DEF_END = 200

    # Energy
    INDUSTRY_OIL_GAS_DRILLING = 201
    INDUSTRY_OIL_GAS_EP = 202
    INDUSTRY_OIL_GAS_EQUIPMENT = 203
    INDUSTRY_OIL_GAS_INTEGRATED = 204
    INDUSTRY_OIL_GAS_MIDSTREAM = 205
    INDUSTRY_OIL_GAS_REFINING = 206
    INDUSTRY_THERMAL_COAL = 207
    INDUSTRY_URANIUM = 208
    # enumeration borders
    INDUSTRY_ENERGY_FIRST = 201
    INDUSTRY_ENERGY_LAST = 208
    INDUSTRY_ENERGY_END = 250

    # Financial
    INDUSTRY_EXCHANGE_TRADED_FUND = 251
    INDUSTRY_ASSETS_MANAGEMENT = 252
    INDUSTRY_BANKS_DIVERSIFIED = 253
    INDUSTRY_BANKS_REGIONAL = 254
    INDUSTRY_CAPITAL_MARKETS = 255
    INDUSTRY_CLOSE_END_FUND_DEBT = 256
    INDUSTRY_CLOSE_END_FUND_EQUITY = 257
    INDUSTRY_CLOSE_END_FUND_FOREIGN = 258
    INDUSTRY_CREDIT_SERVICES = 259
    INDUSTRY_FINANCIAL_CONGLOMERATE = 260
    INDUSTRY_FINANCIAL_DATA_EXCHANGE = 261
    INDUSTRY_INSURANCE_BROKERS = 262
    INDUSTRY_INSURANCE_DIVERSIFIED = 263
    INDUSTRY_INSURANCE_LIFE = 264
    INDUSTRY_INSURANCE_PROPERTY = 265
    INDUSTRY_INSURANCE_REINSURANCE = 266
    INDUSTRY_INSURANCE_SPECIALTY = 267
    INDUSTRY_MORTGAGE_FINANCE = 268
    INDUSTRY_SHELL_COMPANIES = 269
    # enumeration borders
    INDUSTRY_FINANCIAL_FIRST = 251
    INDUSTRY_FINANCIAL_LAST = 269
    INDUSTRY_FINANCIAL_END = 300

    # Healthcare
    INDUSTRY_BIOTECHNOLOGY = 301
    INDUSTRY_DIAGNOSTICS_RESEARCH = 302
    INDUSTRY_DRUGS_MANUFACTURERS = 303
    INDUSTRY_DRUGS_MANUFACTURERS_SPEC = 304
    INDUSTRY_HEALTHCARE_PLANS = 305
    INDUSTRY_HEALTH_INFORMATION = 306
    INDUSTRY_MEDICAL_FACILITIES = 307
    INDUSTRY_MEDICAL_DEVICES = 308
    INDUSTRY_MEDICAL_DISTRIBUTION = 309
    INDUSTRY_MEDICAL_INSTRUMENTS = 310
    INDUSTRY_PHARM_RETAILERS = 311
    # enumeration borders
    INDUSTRY_HEALTHCARE_FIRST = 301
    INDUSTRY_HEALTHCARE_LAST = 311
    INDUSTRY_HEALTHCARE_END = 350

    # Industrials
    INDUSTRY_AEROSPACE_DEFENSE = 351
    INDUSTRY_AIRLINES = 352
    INDUSTRY_AIRPORTS_SERVICES = 353
    INDUSTRY_BUILDING_PRODUCTS = 354
    INDUSTRY_BUSINESS_EQUIPMENT = 355
    INDUSTRY_CONGLOMERATES = 356
    INDUSTRY_CONSULTING_SERVICES = 357
    INDUSTRY_ELECTRICAL_EQUIPMENT = 358
    INDUSTRY_ENGINEERING_CONSTRUCTION = 359
    INDUSTRY_FARM_HEAVY_MACHINERY = 360
    INDUSTRY_INDUSTRIAL_DISTRIBUTION = 361
    INDUSTRY_INFRASTRUCTURE_OPERATIONS = 362
    INDUSTRY_FREIGHT_LOGISTICS = 363
    INDUSTRY_MARINE_SHIPPING = 364
    INDUSTRY_METAL_FABRICATION = 365
    INDUSTRY_POLLUTION_CONTROL = 366
    INDUSTRY_RAILROADS = 367
    INDUSTRY_RENTAL_LEASING = 368
    INDUSTRY_SECURITY_PROTECTION = 369
    INDUSTRY_SPEALITY_BUSINESS_SERVICES = 370
    INDUSTRY_SPEALITY_MACHINERY = 371
    INDUSTRY_STUFFING_EMPLOYMENT = 372
    INDUSTRY_TOOLS_ACCESSORIES = 373
    INDUSTRY_TRUCKING = 374
    INDUSTRY_WASTE_MANAGEMENT = 375
    # enumeration borders
    INDUSTRY_INDUSTRIALS_FIRST = 351
    INDUSTRY_INDUSTRIALS_LAST = 375
    INDUSTRY_INDUSTRIALS_END = 400

    # Real Estate
    INDUSTRY_REAL_ESTATE_DEVELOPMENT = 401
    INDUSTRY_REAL_ESTATE_DIVERSIFIED = 402
    INDUSTRY_REAL_ESTATE_SERVICES = 403
    INDUSTRY_REIT_DIVERSIFIED = 404
    INDUSTRY_REIT_HEALTCARE = 405
    INDUSTRY_REIT_HOTEL_MOTEL = 406
    INDUSTRY_REIT_INDUSTRIAL = 407
    INDUSTRY_REIT_MORTAGE = 408
    INDUSTRY_REIT_OFFICE = 409
    INDUSTRY_REIT_RESIDENTAL = 410
    INDUSTRY_REIT_RETAIL = 411
    INDUSTRY_REIT_SPECIALITY = 412
    # enumeration borders
    INDUSTRY_REAL_ESTATE_FIRST = 401
    INDUSTRY_REAL_ESTATE_LAST = 412
    INDUSTRY_REAL_ESTATE_END = 450

    # Technology
    INDUSTRY_COMMUNICATION_EQUIPMENT = 451
    INDUSTRY_COMPUTER_HARDWARE = 452
    INDUSTRY_CONSUMER_ELECTRONICS = 453
    INDUSTRY_ELECTRONIC_COMPONENTS = 454
    INDUSTRY_ELECTRONIC_DISTRIBUTION = 455
    INDUSTRY_IT_SERVICES = 456
    INDUSTRY_SCIENTIFIC_INSTRUMENTS = 457
    INDUSTRY_SEMICONDUCTOR_EQUIPMENT = 458
    INDUSTRY_SEMICONDUCTORS = 459
    INDUSTRY_SOFTWARE_APPLICATION = 460
    INDUSTRY_SOFTWARE_INFRASTRUCTURE = 461
    INDUSTRY_SOLAR = 462
    # enumeration borders
    INDUSTRY_TECHNOLOGY_FIRST = 451
    INDUSTRY_TECHNOLOGY_LAST = 462
    INDUSTRY_TECHNOLOGY_END = 500

    # Utilities
    INDUSTRY_UTILITIES_DIVERSIFIED = 501
    INDUSTRY_UTILITIES_POWERPRODUCERS = 502
    INDUSTRY_UTILITIES_RENEWABLE = 503
    INDUSTRY_UTILITIES_REGULATED_ELECTRIC = 504
    INDUSTRY_UTILITIES_REGULATED_GAS = 505
    INDUSTRY_UTILITIES_REGULATED_WATER = 506
    # enumeration borders
    INDUSTRY_UTILITIES_FIRST = 501
    INDUSTRY_UTILITIES_LAST = 506
    INDUSTRY_UTILITIES_END = 550

    # Commodities
    INDUSTRY_COMMODITIES_AGRICULTURAL = 551
    INDUSTRY_COMMODITIES_ENERGY = 552
    INDUSTRY_COMMODITIES_METALS = 553
    INDUSTRY_COMMODITIES_PRECIOUS = 554
    # enumeration borders
    INDUSTRY_COMMODITIES_FIRST = 551
    INDUSTRY_COMMODITIES_LAST = 554
    INDUSTRY_COMMODITIES_END = 600
    # enumeration borders
    INDUSTRY_FIRST = 0
    INDUSTRY_LAST = INDUSTRY_COMMODITIES_LAST


class MTEnExecutionMode:
    """order execution modes"""

    EXECUTION_REQUEST = 0  # Request Execution
    EXECUTION_INSTANT = 1  # Instant Execution
    EXECUTION_MARKET = 2  # Market Execution
    EXECUTION_EXCHANGE = 3  # Exchange Execution
    # enumeration borders
    EXECUTION_FIRST = EXECUTION_REQUEST
    EXECUTION_LAST = EXECUTION_EXCHANGE


class MTEnCalcMode:
    """profit and margin calculation modes"""

    # market maker modes
    TRADE_MODE_FOREX = 0
    TRADE_MODE_FUTURES = 1
    TRADE_MODE_CFD = 2
    TRADE_MODE_CFDINDEX = 3
    TRADE_MODE_CFDLEVERAGE = 4
    TRADEMODE_FOREX_NO_LEVERAGE = 5
    # market makers enumerations
    TRADE_MODE_MM_FIRST = TRADE_MODE_FOREX
    TRADE_MODE_MM_LAST = TRADEMODE_FOREX_NO_LEVERAGE
    # exchange modes
    TRADE_MODE_EXCH_STOCKS = 32
    TRADE_MODE_EXCH_FUTURES = 33
    TRADE_MODE_EXCH_FUTURES_FORTS = 34
    TRADE_MODE_EXCH_OPTIONS = 35
    TRADE_MODE_EXCH_OPTIONS_MARGIN = 36
    TRADE_MODE_EXCH_BONDS = 37
    TRADE_MODE_EXCH_STOCKS_MOEX = 38
    TRADE_MODE_EXCH_BONDS_MOEX = 39
    # exchange enumerations
    TRADE_MODE_EXCH_FIRST = TRADE_MODE_EXCH_STOCKS
    TRADE_MODE_EXCH_LAST = TRADE_MODE_EXCH_BONDS_MOEX
    # service modes
    TRADE_MODE_SERV_COLLATERAL = 64
    # service enumerations
    TRADE_MODE_SERV_FIRST = TRADE_MODE_SERV_COLLATERAL
    TRADE_MODE_SERV_LAST = TRADE_MODE_SERV_COLLATERAL
    # enumeration borders
    TRADE_MODE_FIRST = TRADE_MODE_FOREX
    TRADE_MODE_LAST = TRADE_MODE_SERV_COLLATERAL


class MTEnGTCMode:
    """orders expiration modes"""

    ORDERS_GTC = 0
    ORDERS_DAILY = 1
    ORDERS_DAILY_NO_STOPS = 2
    # enumeration borders
    ORDERS_FIRST = ORDERS_GTC
    ORDERS_LAST = ORDERS_DAILY_NO_STOPS


class MTEnTickFlags:
    """tick collection flags"""

    TICK_REALTIME = 1  # allow realtime tick apply
    TICK_COLLECTRAW = 2  # allow to collect raw ticks
    TICK_FEED_STATS = 4  # allow to receive price statisticks from datafeeds
    TICK_NEGATIVE_PRICES = 8  # allow to receive negative prices
    # flags borders
    TICK_NONE = 0
    # TICK_REALTIME | TICK_COLLECTRAW | TICK_FEED_STATS | TICK_NEGATIVE_PRICES
    TICK_ALL = 15


class MTEnChartMode:
    """chart mode"""

    CHART_MODE_BID_PRICE = 0
    CHART_MODE_LAST_PRICE = 1
    CHART_MODE_OLD = 255
    # enumeration borders
    CHART_MODE_FIRST = CHART_MODE_BID_PRICE
    CHART_MODE_LAST = CHART_MODE_OLD


class MTEnMarginFlags:
    """margin check modes"""

    MARGIN_FLAGS_NONE = 0  # none
    MARGIN_FLAGS_CHECK_PROCESS = 1  # check margin after dealer confirmation
    MARGIN_FLAGS_CHECK_SLTP = 2  # check margin on SL-TP trigger
    MARGIN_FLAGS_HEDGE_LARGE_LEG = (
        4  # check margin for hedged positions using large leg
    )
    # enumeration borders
    MARGIN_FLAGS_FIRST = MARGIN_FLAGS_NONE
    MARGIN_FLAGS_LAST = MARGIN_FLAGS_HEDGE_LARGE_LEG


class MTEnSwapMode:
    """swaps calculation modes"""

    SWAP_DISABLED = 0
    SWAP_BY_POINTS = 1
    SWAP_BY_SYMBOL_CURRENCY = 2
    SWAP_BY_MARGIN_CURRENCY = 3
    SWAP_BY_GROUP_CURRENCY = 4
    SWAP_BY_INTEREST_CURRENT = 5
    SWAP_BY_INTEREST_OPEN = 6
    SWAP_REOPEN_BY_CLOSE_PRICE = 7
    SWAP_REOPEN_BY_BID = 8
    SWAP_BY_PROFIT_CURRENCY = 9
    # enumeration borders
    SWAP_FIRST = SWAP_DISABLED
    SWAP_LAST = SWAP_BY_PROFIT_CURRENCY


class MTEnInstantMode:
    """Instant Execution Modes"""

    INSTANT_CHECK_NORMAL = 0
    # begin and end of check
    INSTANT_CHECK_FIRST = INSTANT_CHECK_NORMAL
    INSTANT_CHECK_LAST = INSTANT_CHECK_NORMAL


class MTEnRequestFlags:
    """Request Execution Flags"""

    REQUEST_FLAGS_NONE = 0  # node
    REQUEST_FLAGS_ORDER = (
        1  # trade orders should be additional confirmed after quotation
    )
    # flags borders
    REQUEST_FLAGS_ALL = REQUEST_FLAGS_ORDER


class MTEnTradeFlags:
    """common trade flags"""

    TRADE_FLAGS_NONE = 0  # none
    TRADE_FLAGS_PROFIT_BY_MARKET = 1  # convert fx profit using market prices
    TRADE_FLAGS_ALLOW_SIGNALS = 2  # allow trade signals for symbol
    # flags borders
    TRADE_FLAGS_ALL = (
        3  # TRADE_FLAGS_PROFIT_BY_MARKET | TRADE_FLAGS_ALLOW_SIGNALS
    )
    TRADE_FLAGS_DEFAULT = TRADE_FLAGS_ALLOW_SIGNALS


class MTEnMarginRateTypes:
    """Margin Rate Types"""

    MARGIN_RATE_BUY = 0
    MARGIN_RATE_SELL = 1
    MARGIN_RATE_BUY_LIMIT = 2
    MARGIN_RATE_SELL_LIMIT = 3
    MARGIN_RATE_BUY_STOP = 4
    MARGIN_RATE_SELL_STOP = 5
    MARGIN_RATE_BUY_STOP_LIMIT = 6
    MARGIN_RATE_SELL_STOP_LIMIT = 7
    # enumeration borders
    MARGIN_RATE_FIRST = MARGIN_RATE_BUY
    MARGIN_RATE_LAST = MARGIN_RATE_SELL_STOP_LIMIT


class MTEnOptionMode:
    """Options Mode"""

    OPTION_MODE_EUROPEAN_CALL = 0
    OPTION_MODE_EUROPEAN_PUT = 1
    OPTION_MODE_AMERICAN_CALL = 2
    OPTION_MODE_AMERICAN_PUT = 3
    # enumeration borders
    OPTION_MODE_FIRST = OPTION_MODE_EUROPEAN_CALL
    OPTION_MODE_LAST = OPTION_MODE_AMERICAN_PUT


class MTEnSpliceType:
    """Splice Type"""

    SPLICE_NONE = 0
    SPLICE_UNADJUSTED = 1
    SPLICE_ADJUSTED = 2
    # enumeration borders
    SPLICE_FIRST = SPLICE_NONE
    SPLICE_LAST = SPLICE_ADJUSTED


class MTEnSpliceTimeType:
    """Splice Time Type"""

    SPLICE_TIME_EXPIRATION = 0
    # enumeration borders
    SPLICE_TIME_FIRST = SPLICE_TIME_EXPIRATION
    SPLICE_TIME_LAST = SPLICE_TIME_EXPIRATION


class MTConSymbol:
    def __init__(self) -> None:
        self.CurrencyBase = "USD"
        self.CurrencyProfit = "USD"
        self.CurrencyMargin = "USD"
        self.Digits = 4
        self.TickBookDepth = 0
        self.TickFlags = MTEnTickFlags.TICK_REALTIME
        self.FilterDiscard = 500
        self.FilterSoftTicks = 10
        self.FilterHardTicks = 10
        self.FilterHard = 500
        self.FilterSoft = 100
        self.FilterSpreadMax = 0
        self.FilterSpreadMin = 0
        self.TradeMode = MTEnTradeMode.TRADE_FULL
        self.TradeFlags = MTEnTradeFlags.TRADE_FLAGS_DEFAULT
        self.Spread = 0
        self.SpreadBalance = 0
        self.TickValue = 0
        self.TickSize = 0
        self.ContractSize = 100000
        self.GTCMode = MTEnGTCMode.ORDERS_GTC
        self.CalcMode = MTEnCalcMode.TRADE_MODE_FOREX
        self.QuotesTimeout = 0
        self.PriceSettle = 0
        self.PriceLimitMax = 0
        self.PriceLimitMin = 0
        self.TimeStart = 0
        self.TimeExpiration = 0
        self.SpreadDiff = 0
        self.SpreadDiffBalance = 0
        self.StopsLevel = 5
        self.FreezeLevel = 0
        self.ExecMode = MTEnExecutionMode.EXECUTION_INSTANT
        self.FillFlags = MTEnFillingFlags.FILL_FLAGS_FOK
        self.ExpirFlags = MTEnExpirationFlags.TIME_FLAGS_ALL
        self.REFlags = MTEnRequestFlags.REQUEST_FLAGS_NONE
        self.RETimeout = 7
        self.IETimeout = 7
        self.IESlipProfit = 2
        self.IESlipLosing = 2
        self.IEVolumeMax = 0
        self.IECheckMode = MTEnInstantMode.INSTANT_CHECK_NORMAL
        self.VolumeMin = 0
        self.VolumeMax = 100000
        self.VolumeMaxExt = MTUtils.ToNewVolume(self.VolumeMax)
        self.VolumeStep = 10000
        self.VolumeStepExt = MTUtils.ToNewVolume(self.VolumeStep)
        self.VolumeLimit = 0
        self.MarginFlags = MTEnMarginFlags.MARGIN_FLAGS_NONE
        self.MarginInitial = 0
        self.MarginMaintenance = 0
        self.MarginRateInitial = self.GetDefaultMarginRate()
        self.MarginRateMaintenance = self.GetDefaultMarginRate()
        self.MarginRateLiquidity = 0
        self.MarginHedged = 0
        self.MarginRateCurrency = 0
        # DEPRECATED
        self.MarginLong = 1
        self.MarginShort = 1
        self.MarginLimit = 0
        self.MarginStop = 0
        self.MarginStopLimit = 0

        self.SwapMode = MTEnSwapMode.SWAP_DISABLED
        self.SwapLong = 0
        self.SwapShort = 0
        self.Swap3Day = 3
        self.OrderFlags = MTEnOrderFlags.ORDER_FLAGS_ALL
        self.OptionsMode = MTEnOptionMode.OPTION_MODE_EUROPEAN_CALL
        self.PriceStrike = 0

        self.FaceValue = 0
        self.AccruedInterest = 0
        self.SpliceType = MTEnSpliceType.SPLICE_NONE
        self.SpliceTimeType = MTEnSpliceTimeType.SPLICE_TIME_EXPIRATION
        self.SpliceTimeDays = 0

        self.IEFlags = 0
        self.Category = ""
        self.Exchange = ""
        self.CFI = ""
        self.Sector = EnSectors.SECTOR_UNDEFINED
        self.Industry = EnIndustries.INDUSTRY_UNDEFINED
        self.Country = ""
        self.SubscriptionsDelay = 15

    @classmethod
    def GetDefaultMarginRate(cls):
        return {
            MTEnMarginRateTypes.MARGIN_RATE_BUY: 0.0,
            MTEnMarginRateTypes.MARGIN_RATE_SELL: 0.0,
            MTEnMarginRateTypes.MARGIN_RATE_BUY_LIMIT: 0.0,
            MTEnMarginRateTypes.MARGIN_RATE_SELL_LIMIT: 0.0,
            MTEnMarginRateTypes.MARGIN_RATE_BUY_STOP: 0.0,
            MTEnMarginRateTypes.MARGIN_RATE_SELL_STOP: 0.0,
            MTEnMarginRateTypes.MARGIN_RATE_BUY_STOP_LIMIT: 0.0,
            MTEnMarginRateTypes.MARGIN_RATE_SELL_STOP_LIMIT: 0.0,
        }


class MTSymbolAnswer:
    """get symbol info"""

    RetCode = "-1"
    ConfigJson = ""

    @classmethod
    def GetFromJson(cls, obj: dict) -> MTConSymbol:
        if obj is None:
            return None

        result = MTConSymbol()
        result.Symbol = str(obj["Symbol"])
        result.Path = str(obj["Path"])
        result.ISIN = str(obj["ISIN"])
        result.Description = str(obj["Description"])
        result.International = str(obj["International"])
        result.Basis = str(obj["Basis"])
        result.Source = str(obj["Source"])
        result.Page = str(obj["Page"])
        result.CurrencyBase = str(obj["CurrencyBase"])
        result.CurrencyBaseDigits = int(obj["CurrencyBaseDigits"])
        result.CurrencyProfit = str(obj["CurrencyProfit"])
        result.CurrencyProfitDigits = int(obj["CurrencyProfitDigits"])
        result.CurrencyMargin = str(obj["CurrencyMargin"])
        result.CurrencyMarginDigits = int(obj["CurrencyMarginDigits"])
        result.Color = int(obj["Color"])
        result.ColorBackground = int(obj["ColorBackground"])
        result.Digits = int(obj["Digits"])
        result.Point = float(obj["Point"])
        result.Multiply = float(obj["Multiply"])
        result.TickFlags = int(obj["TickFlags"])
        result.TickBookDepth = int(obj["TickBookDepth"])
        result.ChartMode = int(obj["TickChartMode"])
        result.FilterSoft = int(obj["FilterSoft"])
        result.FilterSoftTicks = int(obj["FilterSoftTicks"])
        result.FilterHard = int(obj["FilterHard"])
        result.FilterHardTicks = int(obj["FilterHardTicks"])
        result.FilterDiscard = int(obj["FilterDiscard"])
        result.FilterSpreadMax = int(obj["FilterSpreadMax"])
        result.FilterSpreadMin = int(obj["FilterSpreadMin"])
        result.FilterGap = int(obj["FilterGap"])
        result.FilterGapTicks = int(obj["FilterGapTicks"])
        result.TradeMode = int(obj["TradeMode"])
        result.TradeFlags = int(obj["TradeFlags"])
        result.CalcMode = int(obj["CalcMode"])
        result.ExecMode = int(obj["ExecMode"])
        result.GTCMode = int(obj["GTCMode"])
        result.FillFlags = int(obj["FillFlags"])
        result.ExpirFlags = int(obj["ExpirFlags"])
        result.OrderFlags = int(obj["OrderFlags"])
        result.Spread = int(obj["Spread"])
        result.SpreadBalance = int(obj["SpreadBalance"])
        result.SpreadDiff = int(obj["SpreadDiff"])
        result.SpreadDiffBalance = int(obj["SpreadDiffBalance"])
        result.TickValue = float(obj["TickValue"])
        result.TickSize = float(obj["TickSize"])
        result.ContractSize = float(obj["ContractSize"])
        result.StopsLevel = int(obj["StopsLevel"])
        result.FreezeLevel = int(obj["FreezeLevel"])
        result.QuotesTimeout = int(obj["QuotesTimeout"])

        result.VolumeMin = int(obj["VolumeMin"])
        result.VolumeMinExt = int(
            obj.get("VolumeMinExt", MTUtils.ToNewVolume(obj["VolumeMin"]))
        )

        result.VolumeMax = int(obj["VolumeMax"])
        result.VolumeMaxExt = int(
            obj.get("VolumeMaxExt", MTUtils.ToNewVolume(obj["VolumeMax"]))
        )

        result.VolumeStep = int(obj["VolumeStep"])
        result.VolumeStepExt = int(
            obj.get("VolumeStepExt", MTUtils.ToNewVolume(obj["VolumeStep"]))
        )

        result.VolumeLimit = int(obj["VolumeLimit"])
        result.VolumeLimitExt = int(
            obj.get("VolumeLimitExt", MTUtils.ToNewVolume(obj["VolumeLimit"]))
        )

        ##
        result.MarginFlags = int(obj["MarginFlags"])
        result.MarginInitial = float(obj["MarginInitial"])
        result.MarginMaintenance = float(obj["MarginMaintenance"])
        result.MarginRateLiquidity = float(obj["MarginLiquidity"])
        result.MarginHedged = float(obj["MarginHedged"])
        result.MarginRateCurrency = float(obj["MarginCurrency"])
        ##
        cls.SetMarginRateInitial(result, obj)
        result.MarginRateMaintenance = cls.GetMarginRateMaintenance(obj)
        ##
        result.SwapMode = int(obj["SwapMode"])
        result.SwapLong = float(obj["SwapLong"])
        result.SwapShort = float(obj["SwapShort"])
        result.Swap3Day = int(obj["Swap3Day"])
        result.TimeStart = int(obj["TimeStart"])
        result.TimeExpiration = int(obj["TimeExpiration"])
        # data of session
        result.SessionsQuotes = cls.GetSessions(obj["SessionsQuotes"])
        result.SessionsTrades = cls.GetSessions(obj["SessionsTrades"])

        ##
        result.REFlags = int(obj["REFlags"])
        result.RETimeout = int(obj["RETimeout"])
        result.IECheckMode = int(obj["IECheckMode"])
        result.IETimeout = int(obj["IETimeout"])
        result.IESlipProfit = int(obj["IESlipProfit"])
        result.IESlipLosing = int(obj["IESlipLosing"])

        result.IEVolumeMax = int(obj["IEVolumeMax"])
        result.IEVolumeMaxExt = int(
            obj.get("IEVolumeMaxExt", MTUtils.ToNewVolume(obj["IEVolumeMax"]))
        )

        result.PriceSettle = float(obj["PriceSettle"])
        result.PriceLimitMax = float(obj["PriceLimitMax"])
        result.PriceLimitMin = float(obj["PriceLimitMin"])
        result.PriceStrike = float(obj["PriceStrike"])

        # support both name old or new
        if "OptionMode" in obj:
            result.OptionsMode = int(obj["OptionMode"])

        elif "OptionsMode" in obj:
            result.OptionsMode = int(obj["OptionsMode"])

        #
        result.FaceValue = float(obj["FaceValue"])
        result.AccruedInterest = float(obj["AccruedInterest"])
        result.SpliceType = int(obj["SpliceType"])
        result.SpliceTimeType = int(obj["SpliceTimeType"])
        result.SpliceTimeDays = int(obj["SpliceTimeDays"])
        result.IEFlags = int(obj.get("IEFlags", 0))
        result.Category = str(obj.get("Category", ""))
        result.Exchange = str(obj.get("Exchange", ""))
        result.CFI = str(obj.get("CFI", ""))
        result.Sector = int(obj.get("Sector", 0))
        result.Industry = int(obj.get("Industry", 0))
        result.Country = str(obj.get("Country", ""))
        result.SubscriptionsDelay = int(obj.get("SubscriptionsDelay", 0))

        return result

    @classmethod
    def SetMarginRateInitial(cls, symbol, obj):
        """get data for MarginRateInitial"""
        result = MTConSymbol.GetDefaultMarginRate()
        new = False

        if "MarginInitialBuy" in obj:
            result[MTEnMarginRateTypes.MARGIN_RATE_BUY] = float(
                obj["MarginInitialBuy"]
            )
            new = True

        if "MarginInitialSell" in obj:
            result[MTEnMarginRateTypes.MARGIN_RATE_SELL] = float(
                obj["MarginInitialSell"]
            )
            new = True

        if "MarginInitialBuyLimit" in obj:
            result[MTEnMarginRateTypes.MARGIN_RATE_BUY_LIMIT] = float(
                obj["MarginInitialBuyLimit"]
            )
            new = True

        if "MarginInitialSellLimit" in obj:
            result[MTEnMarginRateTypes.MARGIN_RATE_SELL_LIMIT] = float(
                obj["MarginInitialSellLimit"]
            )
            new = True

        if "MarginInitialBuyStop" in obj:
            result[MTEnMarginRateTypes.MARGIN_RATE_BUY_STOP] = float(
                obj["MarginInitialBuyStop"]
            )
            new = True

        if "MarginInitialSellStop" in obj:
            result[MTEnMarginRateTypes.MARGIN_RATE_SELL_STOP] = float(
                obj["MarginInitialSellStop"]
            )
            new = True

        if "MarginInitialBuyStopLimit" in obj:
            result[MTEnMarginRateTypes.MARGIN_RATE_BUY_STOP_LIMIT] = float(
                obj["MarginInitialBuyStopLimit"]
            )
            new = True

        if "MarginInitialSellStopLimit" in obj:
            result[MTEnMarginRateTypes.MARGIN_RATE_SELL_STOP_LIMIT] = float(
                obj["MarginInitialSellStopLimit"]
            )
            new = True

        if not new:
            cls.OldMarginRateInitialConvert(symbol, obj)

        else:
            symbol.MarginRateInitial = result
            cls.OldMarginRateInitialSet(symbol, obj)

    @classmethod
    def OldMarginRateInitialConvert(cls, symbol, obj):
        """convert from deprecated values to actual"""
        result = MTConSymbol.GetDefaultMarginRate()

        if "MarginLong" in obj:
            symbol.MarginLong = float(obj["MarginLong"])
            result[MTEnMarginRateTypes.MARGIN_RATE_BUY] = float(
                obj["MarginLong"]
            )

        if "MarginShort" in obj:
            symbol.MarginShort = float(obj["MarginShort"])
            result[MTEnMarginRateTypes.MARGIN_RATE_SELL] = float(
                obj["MarginShort"]
            )

        if "MarginLimit" in obj:
            symbol.MarginLimit = float(obj["MarginLimit"])
            result[MTEnMarginRateTypes.MARGIN_RATE_BUY_LIMIT] = (
                symbol.MarginLimit * symbol.MarginLong
            )
            result[MTEnMarginRateTypes.MARGIN_RATE_SELL_LIMIT] = (
                symbol.MarginLimit * symbol.MarginShort
            )

        if "MarginStop" in obj:
            symbol.MarginStop = float(obj["MarginStop"])
            result[MTEnMarginRateTypes.MARGIN_RATE_BUY_STOP] = (
                symbol.MarginStop * symbol.MarginLong
            )
            result[MTEnMarginRateTypes.MARGIN_RATE_SELL_STOP] = (
                symbol.MarginStop * symbol.MarginShort
            )

        if "MarginStopLimit" in obj:
            symbol.MarginStopLimit = float(obj["MarginStopLimit"])
            result[MTEnMarginRateTypes.MARGIN_RATE_BUY_STOP_LIMIT] = (
                symbol.MarginStopLimit * symbol.MarginLong
            )
            result[MTEnMarginRateTypes.MARGIN_RATE_SELL_STOP_LIMIT] = (
                symbol.MarginStopLimit * symbol.MarginShort
            )

        symbol.MarginRateInitial = result

    @classmethod
    def OldMarginRateInitialSet(cls, symbol, obj):
        """set deprecated values for compatibility"""
        symbol.MarginLong = symbol.MarginRateInitial[
            MTEnMarginRateTypes.MARGIN_RATE_BUY
        ]
        symbol.MarginShort = symbol.MarginRateInitial[
            MTEnMarginRateTypes.MARGIN_RATE_SELL
        ]

        marginLimitLong = 0
        marginStopLong = 0
        marginStopLimitLong = 0

        marginLimitShort = 0
        marginStopShort = 0
        marginStopLimitShort = 0

        if symbol.MarginLong != 0:
            marginLimitLong = (
                symbol.MarginRateInitial[
                    MTEnMarginRateTypes.MARGIN_RATE_BUY_LIMIT
                ]
                / symbol.MarginLong
            )
            marginStopLong = (
                symbol.MarginRateInitial[
                    MTEnMarginRateTypes.MARGIN_RATE_BUY_STOP
                ]
                / symbol.MarginLong
            )
            marginStopLimitLong = (
                symbol.MarginRateInitial[
                    MTEnMarginRateTypes.MARGIN_RATE_BUY_STOP_LIMIT
                ]
                / symbol.MarginLong
            )

        if symbol.MarginShort != 0:
            marginLimitShort = (
                symbol.MarginRateInitial[
                    MTEnMarginRateTypes.MARGIN_RATE_SELL_LIMIT
                ]
                / symbol.MarginShort
            )
            marginStopShort = (
                symbol.MarginRateInitial[
                    MTEnMarginRateTypes.MARGIN_RATE_SELL_STOP
                ]
                / symbol.MarginShort
            )
            marginStopLimitShort = (
                symbol.MarginRateInitial[
                    MTEnMarginRateTypes.MARGIN_RATE_SELL_STOP_LIMIT
                ]
                / symbol.MarginShort
            )

        symbol.MarginLimit = max(marginLimitLong, marginLimitShort)
        symbol.MarginStop = max(marginStopLong, marginStopShort)
        symbol.MarginStopLimit = max(marginStopLimitLong, marginStopLimitShort)

    def GetMarginRateMaintenance(obj):
        """get data for MarginRateMaintenance"""
        result = MTConSymbol.GetDefaultMarginRate()

        # set data
        if "MarginMaintenanceBuy" in obj:
            result[MTEnMarginRateTypes.MARGIN_RATE_BUY] = float(
                obj["MarginMaintenanceBuy"]
            )

        if "MarginMaintenanceSell" in obj:
            result[MTEnMarginRateTypes.MARGIN_RATE_SELL] = float(
                obj["MarginMaintenanceSell"]
            )

        if "MarginMaintenanceBuyLimit" in obj:
            result[MTEnMarginRateTypes.MARGIN_RATE_BUY_LIMIT] = float(
                obj["MarginMaintenanceBuyLimit"]
            )

        if "MarginMaintenanceSellLimit" in obj:
            result[MTEnMarginRateTypes.MARGIN_RATE_SELL_LIMIT] = float(
                obj["MarginMaintenanceSellLimit"]
            )

        if "MarginMaintenanceBuyStop" in obj:
            result[MTEnMarginRateTypes.MARGIN_RATE_BUY_STOP] = float(
                obj["MarginMaintenanceBuyStop"]
            )

        if "MarginMaintenanceSellStop" in obj:
            result[MTEnMarginRateTypes.MARGIN_RATE_SELL_STOP] = float(
                obj["MarginMaintenanceSellStop"]
            )

        if "MarginMaintenanceBuyStopLimit" in obj:
            result[MTEnMarginRateTypes.MARGIN_RATE_BUY_STOP_LIMIT] = float(
                obj["MarginMaintenanceBuyStopLimit"]
            )

        if "MarginMaintenanceSellStopLimit" in obj:
            result[MTEnMarginRateTypes.MARGIN_RATE_SELL_STOP_LIMIT] = float(
                obj["MarginMaintenanceSellStopLimit"]
            )

        return result

    @staticmethod
    def GetSessions(list_):
        if not len(list_):
            return

        result = dict()
        i = 0
        for sessions in list_:
            if not len(sessions) or not sessions[0]:
                result[i] = None
                i += 1
                continue

            result[i] = list()
            for session in sessions:
                sess = MTConSymbolSession()
                sess.Open = session['Open']
                sess.Close = session['Close']
                result[i].append(sess)

            i += 1

        return result


class MTConSymbolSession:
    """Symbol trade and quotes sessions config"""

    Open = None
    Close = None


class MTSymbolTotalAnswer:
    """ Answer on request symbol_total """
    RetCode = '-1'
    Total = 0
