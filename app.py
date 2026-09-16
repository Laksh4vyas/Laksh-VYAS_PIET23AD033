from decimal import Decimal
import streamlit as st

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
from exceptions import PricingEngineError
from db import save_booking, fetch_bookings

st.set_page_config(
    page_title="CinePulse | Multiplex Booking Engine",
    page_icon="🎟️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #e50914 0%, #b20710 100%);
        color: white; font-weight: bold; border-radius: 8px; padding: 0.6rem; border: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🎬 CinePulse Booking Engine + Database")
st.markdown("*Production-grade pricing engine with SQLite persistent transaction logging.*")
st.divider()

# Navigation Tabs for UI & Database view
tab1, tab2 = st.tabs(["🎟️ Live Counter & Billing", "🗄️ Database Booking Logs"])

with tab1:
    st.sidebar.header("⚙️ Show Configuration")
    show_id = st.sidebar.text_input("Screen / Show ID", value="PVR-Screen4-Avengers-7PM")

    st.sidebar.subheader("Seat Tiers & Pricing (₹)")
    silver_price = st.sidebar.number_input("Silver Price", value=180.00, step=10.00)
    silver_stock = st.sidebar.number_input("Silver Inventory", value=50, step=1)
    gold_price = st.sidebar.number_input("Gold Price", value=300.00, step=10.00)
    gold_stock = st.sidebar.number_input("Gold Inventory", value=10, step=1)
    recliner_price = st.sidebar.number_input("Recliner Price", value=550.00, step=10.00)
    recliner_stock = st.sidebar.number_input("Recliner Inventory", value=5, step=1)

    st.sidebar.subheader("Offers & Fees")
    festival_flat = st.sidebar.number_input("Festival Flat Discount (₹)", value=100.00, step=10.00)
    member_pct = st.sidebar.number_input("Member Discount (%)", value=10.0, step=1.0)
    member_cap = st.sidebar.number_input("Member Discount Cap (₹)", value=150.00, step=10.00)
    per_ticket_fee = st.sidebar.number_input("Convenience Fee per Ticket (₹)", value=30.00, step=5.00)
    gst_pct = st.sidebar.number_input("GST Rate (%)", value=18.0, step=1.0)

    config = ShowConfig(
        show_id=show_id,
        tiers={
            "Silver": SeatTier("Silver", Decimal(str(silver_price)), seats_left=int(silver_stock)),
            "Gold": SeatTier("Gold", Decimal(str(gold_price)), seats_left=int(gold_stock)),
            "Recliner": SeatTier("Recliner", Decimal(str(recliner_price)), seats_left=int(recliner_stock)),
        },
        festival_discount=FestivalDiscountConfig(flat_amount=Decimal(str(festival_flat))),
        member_discount=MemberDiscountConfig(percent=Decimal(str(member_pct)), cap=Decimal(str(member_cap))),
        fee=FeeConfig(per_ticket_fee=Decimal(str(per_ticket_fee))),
        tax=TaxConfig(gst_percent=Decimal(str(gst_pct))),
    )

    engine = PricingEngine(config)

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.subheader("🎟️ Select Your Seats")
        inv_cols = st.columns(3)
        inv_cols[0].metric("Silver Available", config.tiers["Silver"].seats_left)
        inv_cols[1].metric("Gold Available", config.tiers["Gold"].seats_left)
        inv_cols[2].metric("Recliner Available", config.tiers["Recliner"].seats_left)
        
        st.markdown("###")
        silver_qty = st.number_input("Silver Seats Quantity", min_value=0, max_value=100, value=0, step=1)
        gold_qty = st.number_input("Gold Seats Quantity", min_value=0, max_value=100, value=2, step=1)
        recliner_qty = st.number_input("Recliner Seats Quantity", min_value=0, max_value=100, value=1, step=1)
        
        st.markdown("###")
        calculate_btn = st.button("Calculate & Save to Database")

    with col2:
        st.subheader("🧾 Itemized Bill Breakdown")
        if calculate_btn:
            requests = []
            if silver_qty > 0: requests.append(SeatRequest("Silver", int(silver_qty)))
            if gold_qty > 0: requests.append(SeatRequest("Gold", int(gold_qty)))
            if recliner_qty > 0: requests.append(SeatRequest("Recliner", int(recliner_qty)))
                
            try:
                bill = engine.generate_bill(requests)
                
                # Save transaction into SQLite database
                save_booking(bill.show_id, str(bill.grand_total))
                
                for line in bill.lines:
                    l_col1, l_col2 = st.columns([2, 1])
                    l_col1.write(line.description if hasattr(line, 'description') else line.label)
                    prefix = "-₹" if line.amount < 0 else "₹"
                    l_col2.markdown(f"<div style='text-align: right;'>{prefix}{abs(line.amount):,.2f}</div>", unsafe_allow_html=True)
                
                st.markdown("---")
                t_col1, t_col2 = st.columns([2, 1])
                t_col1.markdown("### GRAND TOTAL")
                t_col2.markdown(f"### <span style='color: #4ade80;'>₹{bill.grand_total:,.2f}</span>", unsafe_allow_html=True)
                
                st.success("✅ Bill calculated successfully and recorded in SQLite database!")
            except PricingEngineError as e:
                st.error(f"❌ **Booking Failed:** {e}")
        else:
            st.info("👈 Choose seats and click to compute and log to database.")

with tab2:
    st.subheader("🗄️ SQLite Database Transaction Logs")
    st.markdown("All generated multiplex bookings are permanently stored below.")
    
    records = fetch_bookings()
    if records:
        st.table([{"ID": r[0], "Show ID": r[1], "Grand Total (₹)": r[2], "Timestamp": r[3]} for r in records])
    else:
        st.info("No bookings recorded in the database yet.")