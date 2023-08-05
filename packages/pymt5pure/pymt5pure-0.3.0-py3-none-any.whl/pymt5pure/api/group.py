# flake8:noqa
from pymt5pure.api.symbol import MTEnOrderFlags, MTEnMarginRateTypes


class MTGroupTotalAnswer:
    """Answer on request group_total"""

    RetCode = "-1"
    Total = 0


class MTEnGroupSymbolPermissions:
    PERMISSION_NONE = 0
    PERMISSION_BOOK = 1
    # enumeration borders
    PERMISSION_DEFAULT = PERMISSION_BOOK
    PERMISSION_ALL = PERMISSION_BOOK


class MTConGroupSymbol:
    DEFAULT_VALUE_UINT = 0xFFFFFFFF
    DEFAULT_VALUE_INT = 0x7FFFFFFF
    DEFAULT_VALUE_UINT64 = 0xFFFFFFFFFFFFFFFF
    DEFAULT_VALUE_INT64 = 0x7FFFFFFFFFFFFFFF
    DEFAULT_VALUE_DOUBLE = 1.7976931348623158e308

    def __init__(self) -> None:
        self.TradeMode = MTConGroupSymbol.DEFAULT_VALUE_UINT
        self.ExecMode = MTConGroupSymbol.DEFAULT_VALUE_UINT
        self.FillFlags = MTConGroupSymbol.DEFAULT_VALUE_UINT
        self.ExpirFlags = MTConGroupSymbol.DEFAULT_VALUE_UINT
        self.OrderFlags = MTEnOrderFlags.ORDER_FLAGS_NONE
        self.SpreadDiff = MTConGroupSymbol.DEFAULT_VALUE_INT
        self.SpreadDiffBalance = MTConGroupSymbol.DEFAULT_VALUE_INT
        self.StopsLevel = MTConGroupSymbol.DEFAULT_VALUE_INT
        self.FreezeLevel = MTConGroupSymbol.DEFAULT_VALUE_INT
        self.VolumeMin = MTConGroupSymbol.DEFAULT_VALUE_UINT64
        self.VolumeMinExt = MTConGroupSymbol.DEFAULT_VALUE_UINT64
        self.VolumeMax = MTConGroupSymbol.DEFAULT_VALUE_UINT64
        self.VolumeMaxExt = MTConGroupSymbol.DEFAULT_VALUE_UINT64
        self.VolumeStep = MTConGroupSymbol.DEFAULT_VALUE_UINT64
        self.VolumeStepExt = MTConGroupSymbol.DEFAULT_VALUE_UINT64
        self.VolumeLimit = MTConGroupSymbol.DEFAULT_VALUE_UINT64
        self.VolumeLimitExt = MTConGroupSymbol.DEFAULT_VALUE_UINT64
        self.MarginFlags = MTConGroupSymbol.DEFAULT_VALUE_UINT
        self.MarginInitial = MTConGroupSymbol.DEFAULT_VALUE_DOUBLE
        self.MarginMaintenance = MTConGroupSymbol.DEFAULT_VALUE_DOUBLE
        self.MarginRateInitial = {
            MTEnMarginRateTypes.MARGIN_RATE_BUY: MTConGroupSymbol.DEFAULT_VALUE_DOUBLE,
            MTEnMarginRateTypes.MARGIN_RATE_SELL: MTConGroupSymbol.DEFAULT_VALUE_DOUBLE,
            MTEnMarginRateTypes.MARGIN_RATE_BUY_LIMIT: MTConGroupSymbol.DEFAULT_VALUE_DOUBLE,
            MTEnMarginRateTypes.MARGIN_RATE_SELL_LIMIT: MTConGroupSymbol.DEFAULT_VALUE_DOUBLE,
            MTEnMarginRateTypes.MARGIN_RATE_BUY_STOP: MTConGroupSymbol.DEFAULT_VALUE_DOUBLE,
            MTEnMarginRateTypes.MARGIN_RATE_SELL_STOP: MTConGroupSymbol.DEFAULT_VALUE_DOUBLE,
            MTEnMarginRateTypes.MARGIN_RATE_BUY_STOP_LIMIT: MTConGroupSymbol.DEFAULT_VALUE_DOUBLE,
            MTEnMarginRateTypes.MARGIN_RATE_SELL_STOP_LIMIT: MTConGroupSymbol.DEFAULT_VALUE_DOUBLE,
        }
        self.MarginRateMaintenance = {
            MTEnMarginRateTypes.MARGIN_RATE_BUY: MTConGroupSymbol.DEFAULT_VALUE_DOUBLE,
            MTEnMarginRateTypes.MARGIN_RATE_SELL: MTConGroupSymbol.DEFAULT_VALUE_DOUBLE,
            MTEnMarginRateTypes.MARGIN_RATE_BUY_LIMIT: MTConGroupSymbol.DEFAULT_VALUE_DOUBLE,
            MTEnMarginRateTypes.MARGIN_RATE_SELL_LIMIT: MTConGroupSymbol.DEFAULT_VALUE_DOUBLE,
            MTEnMarginRateTypes.MARGIN_RATE_BUY_STOP: MTConGroupSymbol.DEFAULT_VALUE_DOUBLE,
            MTEnMarginRateTypes.MARGIN_RATE_SELL_STOP: MTConGroupSymbol.DEFAULT_VALUE_DOUBLE,
            MTEnMarginRateTypes.MARGIN_RATE_BUY_STOP_LIMIT: MTConGroupSymbol.DEFAULT_VALUE_DOUBLE,
            MTEnMarginRateTypes.MARGIN_RATE_SELL_STOP_LIMIT: MTConGroupSymbol.DEFAULT_VALUE_DOUBLE,
        }
        self.MarginRateLiquidity = MTConGroupSymbol.DEFAULT_VALUE_DOUBLE
        self.MarginHedged = MTConGroupSymbol.DEFAULT_VALUE_DOUBLE
        self.MarginRateCurrency = MTConGroupSymbol.DEFAULT_VALUE_DOUBLE

        # # DEPRECATED
        self.MarginLong = MTConGroupSymbol.DEFAULT_VALUE_DOUBLE
        self.MarginShort = MTConGroupSymbol.DEFAULT_VALUE_DOUBLE
        self.MarginLimit = MTConGroupSymbol.DEFAULT_VALUE_DOUBLE
        self.MarginStop = MTConGroupSymbol.DEFAULT_VALUE_DOUBLE
        self.MarginStopLimit = MTConGroupSymbol.DEFAULT_VALUE_DOUBLE

        self.SwapMode = MTConGroupSymbol.DEFAULT_VALUE_UINT
        self.SwapLong = MTConGroupSymbol.DEFAULT_VALUE_DOUBLE
        self.SwapShort = MTConGroupSymbol.DEFAULT_VALUE_DOUBLE
        self.Swap3Day = MTConGroupSymbol.DEFAULT_VALUE_INT
        self.REFlags = MTConGroupSymbol.DEFAULT_VALUE_UINT
        self.RETimeout = MTConGroupSymbol.DEFAULT_VALUE_UINT
        self.IEFlags = MTConGroupSymbol.DEFAULT_VALUE_UINT
        self.IECheckMode = MTConGroupSymbol.DEFAULT_VALUE_UINT
        self.IETimeout = MTConGroupSymbol.DEFAULT_VALUE_UINT
        self.IESlipProfit = MTConGroupSymbol.DEFAULT_VALUE_UINT
        self.IESlipLosing = MTConGroupSymbol.DEFAULT_VALUE_UINT
        self.IEVolumeMax = MTConGroupSymbol.DEFAULT_VALUE_UINT64
        self.IEVolumeMaxExt = MTConGroupSymbol.DEFAULT_VALUE_UINT64
        self.PermissionsFlags = MTEnGroupSymbolPermissions.PERMISSION_DEFAULT
        self.BookDepthLimit = 0
