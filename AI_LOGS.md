# 🤖 AI Conversation Log

<p align="center">
  <img src="https://img.shields.io/badge/AI%20Collaborator-Claude%20(Anthropic)-blue.svg" alt="AI Tool">
  <img src="https://img.shields.io/badge/Transparency-100%25%20Authentic-success.svg" alt="Transparent Logs">
</p>

**Tool used:** Claude (Anthropic)  
**Status:** Pasted as-is, unmodified, in accordance with assessment submission guidelines.

---

## 📋 Chronological Session Breakdown

### **Turn 1 — Architecture Request**
* **Request:** Asked for a modular architecture for a cinema pricing engine: seat tiers, availability, festival + member discounts, convenience fee, GST, exact paisa precision, and itemized bill. Requested step-by-step collaboration rather than a single code dump.
* **Assistant Response:** Proposed a modular module split (`models.py`, `tier_manager.py`, `discounts.py`, `fees_and_tax.py`, `pricing_engine.py`, `exceptions.py`), defined core dataclasses, and laid out the 9-step calculation pipeline with explicit rounding rules (`Decimal` only, `ROUND_HALF_UP`, quantize only at derived-value checkpoints). Asked clarifying questions regarding GST base and discount cap semantics.

### **Turn 2 — Full Implementation Request**
* **Request:** Asked for a complete, production-ready single file with custom exceptions (`TierSoldOutError`, `InvalidTierError`, `InvalidQuantityError`, `InvalidConfigurationError`), configuration-driven design, strict Decimal rounding, type hints, and docstrings.
* **Assistant Response:** Delivered a single implementation file implementing all criteria, ran sandbox tests to verify output against hand-calculated math, and verified custom exception triggers.

### **Turn 3 — Code Style Refinement & Structuring**
* **Request:** Asked to split the single file into separate single-responsibility files, remove redundant comments, and use clean, professional variable names.
* **Assistant Response:** Split the logic across modular standalone files (`exceptions.py`, `money.py`, `models.py`, `tier_manager.py`, `discounts.py`, `fees_and_tax.py`, `pricing_engine.py`, `main.py`), streamlined variable conventions, and verified identical numerical output.

### **Turn 4 — Initial Documentation & Submission Files**
* **Request:** Requested initial content for `README.md`, `REASONING.md`, and `AI_LOGS.md` adhering to submission guidelines.
* **Assistant Response:** Provided full markdown documentation detailing project structure, setup guides, pipeline logic, and conversation records.

### **Turn 5 — Codebase Regeneration & Test Suite Integration**
* **Request:** Requested complete source code files across the modular directory layout alongside a robust `pytest` test suite.
* **Assistant Response:** Regenerated all modules and added `tests/test_pricing_engine.py` featuring parametrized edge cases and exact decimal assertions.

### **Turn 6 — Factual Summary & Log Consolidation**
* **Request:** Finalized the conversation logs format to ensure total compliance with submission constraints.
* **Assistant Response:** Compiled the factual summary log detailing the evolution of the project architecture and development steps.

---

### **Turn 7 — "The Twist" (Messy Price List Cleaner)**
* **Request:** Handled the assessment twist requirement: importing a messy real-world seat-class price list containing case-insensitive duplicates, inconsistent string formats (currency symbols, spaces), blank values, and negative prices, while producing an auditable cleaning report.
* **Assistant Response:** Created `price_cleaner.py` featuring robust regex normalization, strict negative-price rejections, and case-insensitive de-duplication tracking, paired with a dedicated unit test suite.

### **Turn 8 — Database Persistence & Streamlit UI Integration**
* **Request:** Requested the integration of a SQLite database persistence layer (`db.py`) to log all completed booking transactions and a modern, dark-themed Streamlit UI dashboard (`app.py`) for interactive multiplex counter simulation.
* **Assistant Response:** Implemented SQLite table initialization and transaction insertion utilities in `db.py` and built an interactive, multi-tab Streamlit dashboard allowing operators to configure shows, calculate exact-paisa bills, and review persistent database audit logs.