from decimal import Decimal
from money import PAISA, ROUNDING


class FlatFestivalDiscount:
    def __init__(self, config):
        self.config = config

    def apply(self, base):
        return min(self.config.flat_amount, base)


class PercentMemberDiscount:
    def __init__(self, config):
        self.config = config

    def apply(self, base):
        raw = base * self.config.percent / Decimal("100")
        capped = min(raw, self.config.cap)
        return capped.quantize(PAISA, rounding=ROUNDING)