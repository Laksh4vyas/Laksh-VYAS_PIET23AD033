# 🧠 Reasoning & Architectural Design Decisions

<p align="center">
  <img src="https://img.shields.io/badge/Architecture-Modular%20&%20Clean-blue.svg" alt="Modular Architecture">
  <img src="https://img.shields.io/badge/Precision-Exact%20Paisa-green.svg" alt="Exact Paisa Precision">
  <img src="https://img.shields.io/badge/Exceptions-Domain%20Specific-orange.svg" alt="Custom Exceptions">
</p>

---

## 1. 🧮 Why `Decimal` exclusively, never `float`

Binary floating point cannot exactly represent most base-10 fractions — `0.1 + 0.2 != 0.3` in float arithmetic. That's a rounding error hidden inside what looks like correct code, and at booking-counter scale it compounds into real, auditable discrepancies on customer receipts. 

* **The Rule:** Every monetary value in this engine is constructed from a `Decimal` or a `str`, never a `float`. 
* **Enforcement:** `money.py` enforces this at the boundary: passing a float into `to_money()` raises `InvalidConfigurationError` immediately rather than silently accepting imprecise input.

---

## 2. 📋 Why the order of operations is a strict business rule

Whether a percentage discount is computed before or after a flat discount changes the final total — this isn't a stylistic choice, it's a pricing policy decision. 

* This engine applies the **flat festival discount first** (a promotional cut off the sticker price), then computes the **percentage member discount** on the already-discounted amount (loyalty rewards apply to what the customer is actually paying, not the list price). 
* The 9-step pipeline in `pricing_engine.py` encodes this order explicitly and documents it in the README so it's never ambiguous or accidentally reordered during a refactor.

---

## 3. 🎯 Controlled rounding strategy

Rounding at every arithmetic step compounds small errors across a multi-stage pipeline; rounding only at the very end hides intermediate values that a printed bill needs to show exactly (e.g., *"Member Discount: Rs. 105.00"* has to match what's actually subtracted). 

* **The Resolution:** `ROUND_HALF_UP` quantization to `0.01` happens at **exactly two points** — the percentage-based member discount and the GST calculation — because those are the only two steps where a genuinely new value is derived via multiplication or division. 
* Every other figure in the pipeline is an exact sum or difference of already paisa-exact numbers and therefore needs no rounding at all. This guarantees the final total is correct to the paisa with zero compounding drift.

---

## 4. 🧩 Why the codebase is split into single-responsibility files

The project is heavily modularized to respect separation of concerns:
* `tier_manager.py` only validates a seat request against availability — it has no concept of discounts or tax. 
* `discounts.py` only computes a discount given a base amount — it doesn't know where that base came from. 
* `fees_and_tax.py` only computes fee and GST math. 
* `pricing_engine.py` is the only file that knows the *order* these steps happen in. 

* **Benefit:** Each unit can be tested in complete isolation. A test for `PercentMemberDiscount` never needs to touch seat availability logic, and a test for `TierManager` never needs to care what GST rate is configured. The result is a test suite that pinpoints exactly what broke, rather than one large integration test.

---

## 5. ⚙️ Why configuration-driven, not hardcoded

The brief is explicit: this engine has to serve any cinema counter, not one show. Hardcoding tier names, prices, or a fixed GST rate would make it correct for exactly one showtime and wrong for every other one. 

* Instead, `ShowConfig` — covering tiers, discount rules, fee, and tax — is injected into `PricingEngine` at construction time. 
* Adding a new show, adjusting a promotional discount, or changing GST for a new financial year never requires touching engine code, only the config passed in.

---

## 6. 🛡️ Why domain-specific exceptions over generic errors

A bare `ValueError("bad tier")` forces the calling layer to parse error strings to determine what went wrong. 

* `InvalidTierError`, `TierSoldOutError`, `InvalidQuantityError`, and `InvalidConfigurationError` are each independently catchable. 
* This allows a booking API or counter UI to respond correctly to each specific failure — e.g., *"this tier is sold out"* vs. *"please enter a valid seat count"* — without any messy string matching.

---

## 🔮 What I'd improve with more time

* **Tier-Specific Eligibility:** Per-tier discount eligibility (e.g., member discount valid on Silver/Gold only, not Recliner).
* **Composable Pipelines:** A configurable discount pipeline (list of discount rules applied in a configured order) instead of two discount types hardcoded into the orchestrator.
* **Concurrency Controls:** Atomic seat-locking for concurrent booking requests — availability is currently a static count per request, not safe under concurrent access.