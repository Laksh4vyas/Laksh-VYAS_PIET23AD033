# 🎬 Cinema Ticket Pricing Engine & Dashboard

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Engine-Decimal%20Precision-green.svg" alt="Decimal Precision">
  <img src="https://img.shields.io/badge/Database-SQLite-success.svg" alt="SQLite Persistence">
  <img src="https://img.shields.io/badge/Testing-Pytest-orange.svg" alt="Pytest">
</p>

<p align="center">
  <a href="https://laksh-vyaspiet23ad033-5xbwcay6sq8853jec9yk48.streamlit.app/">
    <img src="https://img.shields.io/badge/🚀_CLICK_HERE_TO_TEST_LIVE_APP-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Live Streamlit App" height="50">
  </a>
</p>

A production-grade, configuration-driven pricing engine for multiplex booking counters — handles seat tiers, live availability, festival and member discounts, convenience fees, and GST, calculated to the exact paisa using Python's `decimal` module, complete with a messy price list cleaner (The Twist), a SQLite database logger, and an interactive Streamlit UI dashboard.

---

## 💡 Overview

Booking counters don't price a single show — they price every show, every day, each with different tier prices, different discount campaigns, and different seat inventory. 

This engine is built so one `ShowConfig` object can fully describe any show. Nothing about pricing logic is hardcoded; everything is injected at construction time. Additionally, the engine handles real-world messy price lists via a dedicated cleaner utility and persists all transactions into a local SQLite database.

---

## 📂 Project Structure

```text
.
├── 📄 exceptions.py          # Domain-specific error types
├── 📄 money.py               # Decimal helpers, float-guard, paisa rounding
├── 📄 models.py              # Data classes: tiers, configs, bill, requests
├── 📄 tier_manager.py        # Validates requests against live inventory
├── 📄 discounts.py           # Festival (flat) + member (% capped) discounts
├── 📄 fees_and_tax.py        # Convenience fee + GST calculation
├── 📄 pricing_engine.py      # Orchestrates the 9-step pricing pipeline
├── 📄 price_cleaner.py       # Cleans messy raw input lists & audits rejections
├── 📄 db.py                  # SQLite database integration for transaction logs
├── 📄 app.py                 # Interactive Streamlit UI dashboard
├── 📄 main.py                # Runnable example booking
└── 🧪 tests/
    ├── 📄 test_pricing_engine.py # Pytest suite for core pricing logic
    └── 📄 test_price_cleaner.py  # Pytest suite for data cleaning & twist validation
    
---

### Step 3: Yeh **Part 2** copy kar aur Part 1 ke **just neeche** paste karke save kar:

```markdown
---

## 🚀 Setup & Installation

Requires Python 3.9+. 

```bash
# 1. Clone the repository
git clone [https://github.com/LAKSH-VYAS-PIET23AD033/LAKSH-VYAS_PIET23AD033.git](https://github.com/LAKSH-VYAS-PIET23AD033/LAKSH-VYAS_PIET23AD033.git)
cd LAKSH-VYAS_PIET23AD033

# 2. Run the main demonstration script (Executes The Twist & Pricing Pipeline)
python3 main.py
🖥️ Running the Streamlit UI & Database Dashboard LocallyTo launch the interactive multiplex counter dashboard locally and review live SQLite transaction logs:Bash# Install Streamlit (if not already installed)
pip install streamlit

# Launch the app locally
streamlit run app.py
🧪 Running TestsTo run the complete test suite and verify edge cases:Bash# Install Pytest
pip install pytest

# Run all unit tests
python3 -m pytest tests/ -v

---

### Step 4: Yeh **Part 3** copy kar aur baaki file ke **just neeche** paste karke save kar:

```markdown
---

## 🔄 "The Twist" — Price List Cleaner

The engine includes a robust `price_cleaner.py` utility designed to ingest messy, real-world raw seat-class inputs. It handles:

* **Case-Insensitive De-duplication:** Automatically catches duplicate variant rows (e.g., `"silver"` vs `"SILVER"`).
* **Format Normalization:** Strips currency symbols (`₹`, `Rs.`), commas, and whitespace while preserving decimal points.
* **Integrity Filtering:** Rejects blank values, unparseable strings, and negative prices.
* **Audit Reporting:** Returns a clean dictionary of valid `SeatTier` objects alongside an itemized audit log of imported, de-duplicated, and rejected items.

---

## 🔢 Pricing Pipeline & Order of Operations

The engine follows a fixed, deliberate sequence. Order is a business rule, not an implementation detail — applying a percentage discount before vs. after a flat discount changes the final bill.

1. **Gross Subtotal** = $\sum (\text{price\_per\_seat} \times \text{quantity})$ across all tiers
2. **Festival Discount** = $\min(\text{flat\_amount}, \text{Gross Subtotal})$
3. **Post-Festival** = $\text{Gross Subtotal} - \text{Festival Discount}$
4. **Member Discount** = $\min(\text{Post-Festival} \times \text{percent} \div 100, \text{cap})$ [rounded]
5. **Net Ticket Amount** = $\text{Post-Festival} - \text{Member Discount}$
6. **Convenience Fee** = $\text{per\_ticket\_fee} \times \text{total\_ticket\_count}$
7. **Taxable Amount** = $\text{Net Ticket Amount} + \text{Convenience Fee}$
8. **GST** = $\text{Taxable Amount} \times \text{gst\_percent} \div 100$ [rounded]
9. **Grand Total** = $\text{Taxable Amount} + \text{GST}$

> **Rounding Rule:** Rounding (`ROUND_HALF_UP`, quantized to `0.01`) is applied **only** at steps 4 and 8 — the two points where a new value is genuinely derived through multiplication. Every other figure is an exact sum or difference of already paisa-exact numbers, so no rounding error can compound anywhere else in the pipeline.

---

## 💻 Example Usage

```python
from decimal import Decimal
from models import (
    ShowConfig, SeatTier, FestivalDiscountConfig,
    MemberDiscountConfig, FeeConfig, TaxConfig, SeatRequest,
)
from pricing_engine import PricingEngine

show = ShowConfig(
    show_id="PVR-Screen4-Avengers-7PM",
    tiers={
        "Silver": SeatTier("Silver", Decimal("180.00"), seats_left=40),
        "Gold": SeatTier("Gold", Decimal("300.00"), seats_left=2),
        "Recliner": SeatTier("Recliner", Decimal("550.00"), seats_left=10),
    },
    festival_discount=FestivalDiscountConfig(flat_amount=Decimal("100.00")),
    member_discount=MemberDiscountConfig(percent=Decimal("10"), cap=Decimal("150.00")),
    fee=FeeConfig(per_ticket_fee=Decimal("30.00")),
    tax=TaxConfig(gst_percent=Decimal("18")),
)

engine = PricingEngine(show)
bill = engine.generate_bill([SeatRequest("Gold", 2), SeatRequest("Recliner", 1)])
print(bill.render())
📋 Output:PlaintextShow: PVR-Screen4-Avengers-7PM
Gold x 2 @ Rs. 300.00           Rs.   600.00
Recliner x 1 @ Rs. 550.50       Rs.   550.50
Festival Discount               -Rs.  100.00
Member Discount                 -Rs.  105.05
Convenience Fee (3 ticket(s))   Rs.    90.00
GST @ 18%                       Rs.   186.38

GRAND TOTAL                     Rs.  1221.83
🛡️ Error HandlingEvery failure is a specific, catchable exception rather than a bare ValueError — a calling API or UI layer can branch on the exact failure reason and surface the right message to the user.ScenarioException RaisedTier name not in show configInvalidTierErrorZero, negative, or non-integer quantityInvalidQuantityErrorRequested seats exceed availabilityTierSoldOutErrorNegative price, fee, cap, or bad percentInvalidConfigurationError