from decimal import Decimal
from money import PAISA, ROUNDING


class FeeTaxCalculator:
    def __init__(self, fee_config, tax_config):
        self.fee_config = fee_config
        self.tax_config = tax_config

    def convenience_fee(self, ticket_count):
        return self.fee_config.per_ticket_fee * ticket_count

    def gst(self, taxable_amount):
        raw = taxable_amount * self.tax_config.gst_percent / Decimal("100")
        return raw.quantize(PAISA, rounding=ROUNDING)