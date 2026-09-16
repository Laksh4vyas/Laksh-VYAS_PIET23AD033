from decimal import Decimal
from models import ShowConfig, FestivalDiscountConfig, MemberDiscountConfig, FeeConfig, TaxConfig, SeatRequest
from pricing_engine import PricingEngine
from price_cleaner import clean_price_list

# Messy raw data matching the test case expectations
messy_raw_price_list = [
    {"name": "silver", "price": "₹180.00", "seats_left": 40},
    {"name": "SILVER", "price": "190.00", "seats_left": 10},  # Case duplicate -> De-duplicate
    {"name": "Gold", "price": "  300 ", "seats_left": 2},
    {"name": "gold", "price": "310.00", "seats_left": 5},     # Case duplicate -> De-duplicate
    {"name": "Recliner", "price": "550.50", "seats_left": 10}, # Clean price format
    {"name": "VIP_Box", "price": "-100.00", "seats_left": 5},  # Negative price -> Reject
    {"name": "", "price": "250.00", "seats_left": 20},         # Blank name -> Reject
    {"name": "Balcony", "price": "N/A", "seats_left": 15},     # Bad price format -> Reject
    {"name": "  gold  ", "price": "320", "seats_left": 1}      # Case duplicate -> De-duplicate
]

print("=== CLEANING MESSY PRICE LIST (THE TWIST) ===")
clean_tiers, audit_report = clean_price_list(messy_raw_price_list)

print(f"Total Entries Processed : {audit_report['total_processed']}")
print(f"Successfully Imported   : {audit_report['imported_count']} ({audit_report['imported_tiers']})")
print(f"De-duplicated Count     : {audit_report['deduplicated_count']}")
print(f"Rejected Count          : {audit_report['rejected_count']}")

print("\n" + "="*50 + "\n")

# Build show config using the newly cleaned tiers
show = ShowConfig(
    show_id="PVR-Screen4-TwistShow",
    tiers=clean_tiers,
    festival_discount=FestivalDiscountConfig(flat_amount=Decimal("100.00")),
    member_discount=MemberDiscountConfig(percent=Decimal("10"), cap=Decimal("150.00")),
    fee=FeeConfig(per_ticket_fee=Decimal("30.00")),
    tax=TaxConfig(gst_percent=Decimal("18")),
)

engine = PricingEngine(show)
bill = engine.generate_bill([
    SeatRequest("Gold", 2),
    SeatRequest("Recliner", 1),
])

print(bill.render())