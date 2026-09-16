from decimal import Decimal
from dataclasses import replace
import pytest

from exceptions import (
    TierSoldOutError,
    InvalidTierError,
    InvalidQuantityError,
)
from models import (
    ShowConfig,
    SeatTier,
    FestivalDiscountConfig,
    MemberDiscountConfig,
    FeeConfig,
    TaxConfig,
    SeatRequest,
)
from pricing_engine import PricingEngine


@pytest.fixture
def sample_show_config():
    return ShowConfig(
        show_id="TEST-SHOW-01",
        tiers={
            "Silver": SeatTier("Silver", Decimal("180.00"), seats_left=50),
            "Gold": SeatTier("Gold", Decimal("300.00"), seats_left=5),
            "Recliner": SeatTier("Recliner", Decimal("550.00"), seats_left=2),
        },
        festival_discount=FestivalDiscountConfig(flat_amount=Decimal("100.00")),
        member_discount=MemberDiscountConfig(percent=Decimal("10"), cap=Decimal("150.00")),
        fee=FeeConfig(per_ticket_fee=Decimal("30.00")),
        tax=TaxConfig(gst_percent=Decimal("18")),
    )


def test_successful_booking_breakdown(sample_show_config):
    engine = PricingEngine(sample_show_config)
    requests = [SeatRequest("Gold", 2), SeatRequest("Recliner", 1)]
    bill = engine.generate_bill(requests)

    assert bill.gross_subtotal == Decimal("1150.00")
    assert bill.festival_discount == Decimal("100.00")
    assert bill.member_discount == Decimal("105.00")
    assert bill.net_ticket_amount == Decimal("945.00")
    assert bill.convenience_fee == Decimal("90.00")
    assert bill.taxable_amount == Decimal("1035.00")
    assert bill.gst_amount == Decimal("186.30")
    assert bill.grand_total == Decimal("1221.30")


def test_sold_out_tier_raises_error(sample_show_config):
    gold_tier = replace(sample_show_config.tiers["Gold"], seats_left=0)
    new_tiers = {**sample_show_config.tiers, "Gold": gold_tier}
    sold_out_config = replace(sample_show_config, tiers=new_tiers)
    
    engine = PricingEngine(sold_out_config)
    with pytest.raises(TierSoldOutError):
        engine.generate_bill([SeatRequest("Gold", 1)])


def test_invalid_tier_raises_error(sample_show_config):
    engine = PricingEngine(sample_show_config)
    with pytest.raises(InvalidTierError):
        engine.generate_bill([SeatRequest("Platinum", 1)])


@pytest.mark.parametrize("invalid_qty", [0, -2])
def test_invalid_quantity_raises_error(sample_show_config, invalid_qty):
    engine = PricingEngine(sample_show_config)
    with pytest.raises(InvalidQuantityError):
        engine.generate_bill([SeatRequest("Silver", invalid_qty)])


def test_member_discount_hits_cap(sample_show_config):
    new_member_discount = MemberDiscountConfig(
        percent=Decimal("50"), cap=Decimal("20.00")
    )
    capped_config = replace(sample_show_config, member_discount=new_member_discount)
    engine = PricingEngine(capped_config)
    
    bill = engine.generate_bill([SeatRequest("Silver", 1)])
    assert bill.member_discount == Decimal("20.00")