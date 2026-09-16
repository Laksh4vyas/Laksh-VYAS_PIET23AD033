from decimal import Decimal, InvalidOperation
import re
from models import SeatTier

def clean_price_list(raw_entries):
    imported = {}
    deduplicated = []
    rejected = []

    for entry in raw_entries:
        raw_name = entry.get("name")
        raw_price = entry.get("price")
        raw_seats = entry.get("seats_left", 0)

        # 1. Check for blank or missing values
        if raw_name is None or str(raw_name).strip() == "" or raw_price is None or str(raw_price).strip() == "":
            rejected.append({
                "entry": entry, 
                "reason": "Rejected: Blank or missing name or price value."
            })
            continue

        canonical_name = str(raw_name).strip().title()

        # 2. Clean price format safely
        price_str = str(raw_price).strip()
        is_negative = '-' in price_str

        # Remove everything except numbers and dots
        cleaned_price_str = re.sub(r'[^0-9.]', '', price_str)

        if not cleaned_price_str:
            rejected.append({
                "entry": entry, 
                "reason": f"Rejected: Unparseable price format '{raw_price}'."
            })
            continue

        try:
            price_val = Decimal(cleaned_price_str)
            if is_negative:
                price_val = -price_val
        except (InvalidOperation, ValueError):
            rejected.append({
                "entry": entry, 
                "reason": f"Rejected: Unparseable price format '{raw_price}'."
            })
            continue

        # 3. Check for negative prices
        if price_val < 0:
            rejected.append({
                "entry": entry, 
                "reason": f"Rejected: Negative price not allowed ({price_val} for {canonical_name})."
            })
            continue

        # Parse seats safely
        try:
            seats_val = int(raw_seats)
            if seats_val < 0:
                seats_val = 0
        except (ValueError, TypeError):
            seats_val = 0

        # 4. Handle Case-Insensitive Duplicate Names
        if canonical_name in imported:
            deduplicated.append({
                "duplicate_entry": entry,
                "canonical_name": canonical_name,
                "action": "De-duplicated: Ignored subsequent duplicate variant."
            })
            continue

        imported[canonical_name] = SeatTier(
            name=canonical_name,
            price_per_seat=price_val.quantize(Decimal("0.01")),
            seats_left=seats_val
        )

    report = {
        "total_processed": len(raw_entries),
        "imported_count": len(imported),
        "imported_tiers": list(imported.keys()),
        "deduplicated_count": len(deduplicated),
        "deduplicated_details": deduplicated,
        "rejected_count": len(rejected),
        "rejected_details": rejected
    }

    return imported, report