from decimal import Decimal
from exceptions import InvalidConfigurationError
from models import BillLine, Bill
from tier_manager import TierManager
from discounts import FlatFestivalDiscount, PercentMemberDiscount
from fees_and_tax import FeeTaxCalculator


class PricingEngine:
    def __init__(self, config):
        self.config = config
        self.tier_manager = TierManager(config.tiers)
        self.festival_discount = FlatFestivalDiscount(config.festival_discount)
        self.member_discount = PercentMemberDiscount(config.member_discount)
        self.fee_tax = FeeTaxCalculator(config.fee, config.tax)

    def generate_bill(self, requests):
        if not requests:
            raise InvalidConfigurationError("need at least one seat request to bill")

        lines = []
        gross_subtotal = Decimal("0.00")
        ticket_count = 0

        for req in requests:
            tier = self.tier_manager.resolve(req)
            line_total = tier.price_per_seat * req.quantity
            gross_subtotal += line_total
            ticket_count += req.quantity
            lines.append(
                BillLine(f"{tier.name} x {req.quantity} @ Rs. {tier.price_per_seat}", line_total)
            )

        festival_cut = self.festival_discount.apply(gross_subtotal)
        if festival_cut > 0:
            lines.append(BillLine("Festival Discount", -festival_cut))
        after_festival = gross_subtotal - festival_cut

        member_cut = self.member_discount.apply(after_festival)
        if member_cut > 0:
            lines.append(BillLine("Member Discount", -member_cut))
        net_ticket_amount = after_festival - member_cut

        fee = self.fee_tax.convenience_fee(ticket_count)
        if fee > 0:
            lines.append(BillLine(f"Convenience Fee ({ticket_count} ticket(s))", fee))

        taxable_amount = net_ticket_amount + fee
        gst_amount = self.fee_tax.gst(taxable_amount)
        if gst_amount > 0:
            lines.append(BillLine(f"GST @ {self.config.tax.gst_percent}%", gst_amount))

        grand_total = taxable_amount + gst_amount

        return Bill(
            show_id=self.config.show_id,
            lines=lines,
            gross_subtotal=gross_subtotal,
            festival_discount=festival_cut,
            member_discount=member_cut,
            net_ticket_amount=net_ticket_amount,
            convenience_fee=fee,
            taxable_amount=taxable_amount,
            gst_amount=gst_amount,
            grand_total=grand_total,
        )