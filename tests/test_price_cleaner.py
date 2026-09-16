from decimal import Decimal
from price_cleaner import clean_price_list

def test_price_list_cleaner_handles_messy_data():
    messy_data = [
        {"name": "silver", "price": "₹180.00", "seats_left": 50},
        {"name": "SILVER", "price": "190.00", "seats_left": 10},  # Duplicate case
        {"name": "Gold", "price": "invalid_price", "seats_left": 5}, # Bad format -> Reject
        {"name": "VIP", "price": "-50.00", "seats_left": 5},      # Negative -> Reject
        {"name": "", "price": "300.00", "seats_left": 5},         # Blank name -> Reject
        {"name": "Recliner", "price": "  550 ", "seats_left": 2}
    ]

    tiers, report = clean_price_list(messy_data)

    assert report["imported_count"] == 2  # Silver and Recliner
    assert "Silver" in tiers
    assert "Recliner" in tiers
    assert tiers["Silver"].price_per_seat == Decimal("180.00")
    assert report["deduplicated_count"] == 1
    assert report["rejected_count"] == 3