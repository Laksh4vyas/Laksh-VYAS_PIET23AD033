from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, List
from exceptions import InvalidConfigurationError


@dataclass(frozen=True)
class SeatTier:
    name: str
    price_per_seat: Decimal
    seats_left: int

    def __post_init__(self):
        if self.price_per_seat <= 0:
            raise InvalidConfigurationError(
                f"{self.name} tier price must be positive, got {self.price_per_seat}"
            )
        if self.seats_left < 0:
            raise InvalidConfigurationError(
                f"{self.name} tier can't have negative seats_left"
            )


@dataclass(frozen=True)
class FestivalDiscountConfig:
    flat_amount: Decimal = field(default_factory=lambda: Decimal("0.00"))

    def __post_init__(self):
        if self.flat_amount < 0:
            raise InvalidConfigurationError("festival flat_amount can't be negative")


@dataclass(frozen=True)
class MemberDiscountConfig:
    percent: Decimal = field(default_factory=lambda: Decimal("0"))
    cap: Decimal = field(default_factory=lambda: Decimal("0.00"))

    def __post_init__(self):
        if not (Decimal("0") <= self.percent <= Decimal("100")):
            raise InvalidConfigurationError("member percent must be between 0 and 100")
        if self.cap < 0:
            raise InvalidConfigurationError("member cap can't be negative")


@dataclass(frozen=True)
class FeeConfig:
    per_ticket_fee: Decimal = field(default_factory=lambda: Decimal("0.00"))

    def __post_init__(self):
        if self.per_ticket_fee < 0:
            raise InvalidConfigurationError("per_ticket_fee can't be negative")


@dataclass(frozen=True)
class TaxConfig:
    gst_percent: Decimal = field(default_factory=lambda: Decimal("0"))

    def __post_init__(self):
        if self.gst_percent < 0:
            raise InvalidConfigurationError("gst_percent can't be negative")


@dataclass(frozen=True)
class ShowConfig:
    show_id: str
    tiers: Dict[str, SeatTier]
    festival_discount: FestivalDiscountConfig = field(default_factory=FestivalDiscountConfig)
    member_discount: MemberDiscountConfig = field(default_factory=MemberDiscountConfig)
    fee: FeeConfig = field(default_factory=FeeConfig)
    tax: TaxConfig = field(default_factory=TaxConfig)

    def __post_init__(self):
        if not self.tiers:
            raise InvalidConfigurationError(f"show {self.show_id} needs at least one tier")


@dataclass(frozen=True)
class SeatRequest:
    tier_name: str
    quantity: int


@dataclass(frozen=True)
class BillLine:
    label: str
    amount: Decimal


@dataclass
class Bill:
    show_id: str
    lines: List[BillLine]
    gross_subtotal: Decimal
    festival_discount: Decimal
    member_discount: Decimal
    net_ticket_amount: Decimal
    convenience_fee: Decimal
    taxable_amount: Decimal
    gst_amount: Decimal
    grand_total: Decimal

    def render(self):
        rows = [f"Show: {self.show_id}", "-" * 46]
        for line in self.lines:
            sign = "-" if line.amount < 0 else ""
            rows.append(f"{line.label:<32}{sign}Rs. {abs(line.amount):>8}")
        rows.append("-" * 46)
        rows.append(f"{'GRAND TOTAL':<32}Rs. {self.grand_total:>8}")
        return "\n".join(rows)