import streamlit as st
import random
import time
from datetime import datetime, timedelta

# Page setup
st.set_page_config(page_title="Senior Shield Mode", page_icon="🛡️", layout="wide")

# Session state
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'pending' not in st.session_state:
    st.session_state.pending = False
if 'pending_time' not in st.session_state:
    st.session_state.pending_time = None
if 'family_approved' not in st.session_state:
    st.session_state.family_approved = False
if 'amount' not in st.session_state:
    st.session_state.amount = 0
if 'recipient' not in st.session_state:
    st.session_state.recipient = ""

# Title
st.title("🛡️ Senior Shield Mode")
st.caption("Three-Layer Protection for Elderly Banking")

# Show current step
st.info(f"**Current Status:** Step {st.session_state.step} of 3")

# Step indicators
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**Step 1** 🔐\nKnowledge Check")
with col2:
    st.markdown("**Step 2** 👨‍👩‍👧\nCareCircle Alert")
with col3:
    st.markdown("**Step 3** ⏰\nCooling Period")
st.markdown("---")

# ========== STEP 1: Knowledge Check ==========
if st.session_state.step == 1:
    st.subheader("🔐 Step 1: Security Verification")
    
    # Transaction form
    with st.form("transaction"):
        recipient = st.text_input("Recipient Name")
        amount = st.number_input("Amount (HKD)", min_value=100, max_value=500000, value=10000)
        submitted = st.form_submit_button("Continue", type="primary")
    
    if submitted:
        st.session_state.recipient = recipient
        st.session_state.amount = amount
        
        # Security question
        st.markdown("---")
        st.markdown("### ❓ Security Question")
        
        questions = {
            "What is your wedding anniversary?": "May 10",
            "What is your eldest child's birth month?": "May",
            "What year did you open your first bank account?": "1995"
        }
        
        question = random.choice(list(questions.keys()))
        correct_answer = questions[question]
        
        st.write(f"**{question}**")
        answer = st.text_input("Your answer:")
        
        if st.button("Verify"):
            if answer.lower() == correct_answer.lower():
                st.success("✅ Verified! Moving to Step 2")
                st.session_state.step = 2
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Wrong answer. Transaction cancelled.")
                st.session_state.step = 1

# ========== STEP 2: CareCircle Alert ==========
elif st.session_state.step == 2:
    st.subheader("👨‍👩‍👧 Step 2: CareCircle Alert")
    
    # Check if amount exceeds limit
    if st.session_state.amount > 10000:
        st.warning(f"⚠️ Amount HKD {st.session_state.amount:,} exceeds limit (HKD 10,000)")
        st.info("📱 Sending alerts to family members...")
        
        # Show sent alerts
        st.markdown("**Alerts sent to:**")
        st.success("✅ David Chen (Son) - +852 9123 4567")
        st.success("✅ Lisa Chen (Daughter) - +852 9234 5678")
        st.success("✅ Mary Chen (Spouse) - +852 9345 6789")
        
        st.markdown("---")
        
        # Family approval
        approval = st.radio("Family confirmation:", ["Waiting...", "✅ Approved", "❌ Rejected"])
        
        if approval == "✅ Approved":
            st.success("Family approved! Moving to Step 3")
            st.session_state.step = 3
            time.sleep(1)
            st.rerun()
        elif approval == "❌ Rejected":
            st.error("Transaction rejected by family. Cancelling...")
            st.session_state.step = 1
    else:
        st.success(f"✅ Amount HKD {st.session_state.amount:,} is below limit. No alert needed.")
        if st.button("Continue to Step 3"):
            st.session_state.step = 3
            st.rerun()

# ========== STEP 3: Cooling Period ==========
elif st.session_state.step == 3:
    st.subheader("⏰ Step 3: Cooling Off Period")
    
    if not st.session_state.pending:
        st.warning("⏰ 2-hour cooling period started")
        st.session_state.pending_time = datetime.now() + timedelta(hours=2)
        st.session_state.pending = True
    
    # Show timer
    remaining = st.session_state.pending_time - datetime.now()
    if remaining.total_seconds() > 0:
        hours = int(remaining.total_seconds() // 3600)
        minutes = int((remaining.total_seconds() % 3600) // 60)
        
        st.markdown(f"### ⏰ Time remaining: **{hours}h {minutes}m**")
        
        # Progress bar
        total = 2 * 60 * 60
        elapsed = total - remaining.total_seconds()
        progress = elapsed / total
        st.progress(progress)
        
        # Transaction details
        st.markdown("---")
        st.markdown("**Transaction Summary:**")
        st.write(f"Recipient: {st.session_state.recipient}")
        st.write(f"Amount: HKD {st.session_state.amount:,}")
        st.write(f"Status: Pending until {st.session_state.pending_time.strftime('%H:%M')}")
        
        # Cancel button
        if st.button("❌ Cancel Transaction", type="secondary"):
            st.success("Transaction cancelled successfully!")
            # Reset
            for key in st.session_state.keys():
                del st.session_state[key]
            time.sleep(1)
            st.rerun()
    else:
        st.success("✅ Cooling period complete! Transaction processed successfully.")
        if st.button("New Transaction"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()

# Footer
st.markdown("---")
st.caption("Senior Shield Mode | Emergency: 18222")
