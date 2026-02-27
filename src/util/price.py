from decimal import Decimal


class PriceUtil:
    @staticmethod
    def getActualQuantity(storedQuantity: int) -> Decimal:
        return Decimal(storedQuantity) / Decimal(1_0000)

    @staticmethod
    def getActualCostBasis(storedCostBasis: int) -> Decimal:
        return Decimal(storedCostBasis) / Decimal(1_0000_0000)

    @staticmethod
    def getActualSecurityValue(storedQuantity: int, storedAvgCostBasis: int) -> Decimal:
        return PriceUtil.getActualQuantity(
            storedQuantity
        ) * PriceUtil.getActualCostBasis(storedAvgCostBasis)
