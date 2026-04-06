"""
Senior Shield Mode - Elderly Banking Protection System
Three-layer security mechanism for senior citizens
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import random
import time
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Senior Shield Mode - Elderly Protection",
    page_icon="🛡️",
    layout="wide"
)

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'transaction_pending' not in st.session_state:
    st.session_state.transaction_pending = False
if 'pending_time' not in st.session_state:
    st.session_state.pending_time = None
if 'carecircle_alert_sent' not in st.session_state:
    st.session_state.carecircle_alert_sent = False
if 'knowledge_check_passed' not in st.session_state:
    st.session_state.knowledge_check_passed = False
if 'transaction_amount' not in st.session_state:
    st.session_state.transaction_amount = 0
if 'recipient' not in st.session_state:
    st.session_state.recipient = ""
if 'cooling_period_started' not in st.session_state:
    st.session_state.cooling_period_started = False

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .step-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 5px solid #3B82F6;
    }
    
    .step-active {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        border-left: 5px solid #1E3A8A;
    }
    
    .alert-card {
        background: #FEF2F2;
        border-left: 5px solid #EF4444;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .success-card {
        background: #F0FDF4;
        border-left: 5px solid #10B981;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .warning-card {
        background: #FFFBEB;
        border-left: 5px solid #F59E0B;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .timer {
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
        color: #EF4444;
        margin: 1rem 0;
    }
    
    .family-badge {
        background: #E0E7FF;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        margin: 0.25rem;
    }
    
    .feature-box {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# ==================== Helper Functions ====================

def generate_knowledge_check():
    """Generate personalized security questions"""
    questions = [
        {
            "question": "What is your wedding anniversary date?",
            "options": ["January 15", "March 20", "May 10", "August 8", "October 1", "December 25"],
            "correct": "May 10"
        },
        {
            "question": "What month is your eldest child's birthday?",
            "options": ["January", "March", "May", "July", "September", "November"],
            "correct": "May"
        },
        {
            "question": "In which year did you open your first bank account?",
            "options": ["1985", "1990", "1995", "2000", "2005", "2010"],
            "correct": "1995"
        },
        {
            "question": "What is your favorite pet's name?",
            "options": ["Lucky", "Mimi", "White", "Black", "Bean", "Flower"],
            "correct": "Lucky"
        },
        {
            "question": "What is the name of your elementary school?",
            "options": ["Central Elementary", "Northside School", "Southside Academy", "Eastside Primary", "Westside School", "St. Mary's School"],
            "correct": "Central Elementary"
        },
        {
            "question": "What is your mother's maiden name?",
            "options": ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia"],
            "correct": "Smith"
        },
        {
            "question": "What was the model of your first car?",
            "options": ["Toyota", "Honda", "Ford", "Chevrolet", "Nissan", "BMW"],
            "correct": "Toyota"
        }
    ]
    return random.choice(questions)

def send_carecircle_alert(amount, recipient, family_members):
    """Send CareCircle alerts to family members"""
    alerts = []
    for member in family_members:
        alert = {
            "recipient": member['name'],
            "phone": member['phone'],
            "message": f"[CareCircle Alert] Your family member is transferring HKD {amount:,} to {recipient}. Please confirm if this is authorized. Reply YES to approve, NO to reject.",
            "status": "Sent Successfully"
        }
        alerts.append(alert)
    return alerts

def start_cooling_period():
    """Start the 2-hour cooling period"""
    return datetime.now() + timedelta(hours=2)

def get_remaining_time():
    """Get remaining cooling period time"""
    if st.session_state.pending_time:
        remaining = st.session_state.pending_time - datetime.now()
        if remaining.total_seconds() > 0:
            hours = int(remaining.total_seconds() // 3600)
            minutes = int((remaining.total_seconds() % 3600) // 60)
            return f"{hours}h {minutes}m"
    return "0h 0m"

def create_security_status_chart():
    """Create security status visualization"""
    steps_completed = 0
    if st.session_state.knowledge_check_passed:
        steps_completed += 1
    if st.session_state.carecircle_alert_sent:
        steps_completed += 1
    if st.session_state.transaction_pending:
        steps_completed += 1
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=steps_completed * 33.33,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Security Status", 'font': {'size': 20}},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#1E3A8A"},
            'steps': [
                {'range': [0, 33], 'color': "#FEE2E2"},
                {'range': [33, 66], 'color': "#FEF3C7"},
                {'range': [66, 100], 'color': "#D1FAE5"}
            ]
        }
    ))
    fig.update_layout(height=250, margin=dict(t=50, b=20, l=20, r=20))
    return fig

# ==================== Sidebar ====================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/elderly.png", width=80)
    st.title("🛡️ Senior Shield")
    st.caption("Elderly Banking Protection v1.0")
    
    st.markdown("---")
    
    # Protection Status
    st.markdown("### 🛡️ Protection Status")
    
    status_col1, status_col2 = st.columns(2)
    with status_col1:
        if st.session_state.knowledge_check_passed:
            st.success("✅ Step 1")
        else:
            st.warning("⏳ Step 1")
    with status_col2:
        if st.session_state.carecircle_alert_sent:
            st.success("✅ Step 2")
        else:
            st.warning("⏳ Step 2")
    
    if st.session_state.transaction_pending:
        st.info(f"⏰ Step 3: {get_remaining_time()}")
    else:
        st.info("✅ Step 3: Ready")
    
    st.markdown("---")
    
    # Security Status Gauge
    st.markdown("### 📊 Security Score")
    security_fig = create_security_status_chart()
    st.plotly_chart(security_fig, use_container_width=True)
    
    st.markdown("---")
    
    # CareCircle Members
    st.markdown("### 👨‍👩‍👧‍👦 CareCircle Members")
    st.markdown("""
    <span class="family-badge">👨 David Chen (Son)</span><br>
    <span class="family-badge">👩 Lisa Chen (Daughter)</span><br>
    <span class="family-badge">👵 Mary Chen (Spouse)</span>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Emergency Contacts
    st.markdown("### 🚨 Emergency")
    st.info("**ADCC Hotline:** 18222\n**Bank Support:** 2233 3000")
    
    st.markdown("---")
    st.caption("© 2024 Senior Shield | All Rights Reserved")

# ==================== Main Content ====================
st.markdown("""
<div class="main-header">
    <h1>🛡️ Senior Shield Mode</h1>
    <p>Three-Layer Security Protection for Elderly Banking</p>
</div>
""", unsafe_allow_html=True)

# Feature Overview
st.markdown("## 🎯 Three-Layer Protection System")

feature_col1, feature_col2, feature_col3 = st.columns(3)

with feature_col1:
    st.markdown("""
    <div class="feature-box">
        <h2>🔐 Layer 1</h2>
        <h3>Knowledge Check</h3>
        <p>Personalized security questions only the user would know</p>
        <code>Step 1: Security Challenge</code>
    </div>
    """, unsafe_allow_html=True)

with feature_col2:
    st.markdown("""
    <div class="feature-box">
        <h2>👨‍👩‍👧‍👦 Layer 2</h2>
        <h3>CareCircle Alert</h3>
        <p>Automatic SMS alerts to pre-registered family members</p>
        <code>Step 2: Social Verification</code>
    </div>
    """, unsafe_allow_html=True)

with feature_col3:
    st.markdown("""
    <div class="feature-box">
        <h2>⏰ Layer 3</h2>
        <h3>Cooling Off Period</h3>
        <p>2-hour pending period for new payee transfers</p>
        <code>Step 3: Cooling Period</code>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Progress Steps
st.markdown("## 📋 Transaction Security Flow")

col1, col2, col3 = st.columns(3)

with col1:
    if st.session_state.step >= 1:
        st.markdown("""
        <div class="step-card step-active">
            <h2>🔐 Step 1</h2>
            <h3>Knowledge Check</h3>
            <p>Personalized Security Question</p>
            <span style="color: #10B981;">✅ Completed</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="step-card">
            <h2>🔐 Step 1</h2>
            <h3>Knowledge Check</h3>
            <p>Personalized Security Question</p>
            <span style="color: #6B7280;">⏳ Pending</span>
        </div>
        """, unsafe_allow_html=True)

with col2:
    if st.session_state.step >= 2:
        st.markdown("""
        <div class="step-card step-active">
            <h2>👨‍👩‍👧‍👦 Step 2</h2>
            <h3>CareCircle Alert</h3>
            <p>Family Verification</p>
            <span style="color: #10B981;">✅ Completed</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="step-card">
            <h2>👨‍👩‍👧‍👦 Step 2</h2>
            <h3>CareCircle Alert</h3>
            <p>Family Verification</p>
            <span style="color: #6B7280;">⏳ Pending</span>
        </div>
        """, unsafe_allow_html=True)

with col3:
    if st.session_state.step >= 3:
        st.markdown("""
        <div class="step-card step-active">
            <h2>⏰ Step 3</h2>
            <h3>Cooling Period</h3>
            <p>2-Hour Waiting Period</p>
            <span style="color: #10B981;">✅ Active</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="step-card">
            <h2>⏰ Step 3</h2>
            <h3>Cooling Period</h3>
            <p>2-Hour Waiting Period</p>
            <span style="color: #6B7280;">⏳ Pending</span>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ==================== Transaction Form ====================
st.markdown("## 💰 New Transaction")

with st.form("transaction_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        recipient_name = st.text_input("Recipient Name", placeholder="Enter recipient's full name")
        recipient_account = st.text_input("Account Number", placeholder="Enter bank account number")
        amount = st.number_input("Transfer Amount (HKD)", min_value=100, max_value=1000000, value=10000, step=1000)
    
    with col2:
        transfer_reason = st.selectbox(
            "Transfer Reason",
            ["Goods Purchase", "Service Payment", "Family Transfer", "Investment", "Charity Donation", "Other"]
        )
        is_new_payee = st.radio("Is this a new payee?", ["Yes", "No"], horizontal=True)
    
    submitted = st.form_submit_button("🚀 Initiate Transfer", type="primary", use_container_width=True)

# ==================== Step 1: Knowledge Check ====================
if submitted and not st.session_state.knowledge_check_passed:
    st.markdown("---")
    st.markdown("## 🔐 Step 1: Security Verification")
    
    # Generate security question
    if 'current_question' not in st.session_state:
        st.session_state.current_question = generate_knowledge_check()
    
    question = st.session_state.current_question
    
    st.markdown(f"""
    <div class="step-card">
        <h3>📋 Personalized Security Verification</h3>
        <p>To protect your account, please answer the following question:</p>
        <p><strong>❓ {question['question']}</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    answer = st.radio("Select your answer:", question['options'], index=None)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Verify Identity", type="primary"):
            if answer == question['correct']:
                st.session_state.knowledge_check_passed = True
                st.session_state.step = 2
                st.session_state.transaction_amount = amount
                st.session_state.recipient = recipient_name
                
                st.markdown("""
                <div class="success-card">
                    <h3>✅ Verification Passed!</h3>
                    <p>Identity confirmed. Proceeding to next security layer.</p>
                </div>
                """, unsafe_allow_html=True)
                time.sleep(1)
                st.rerun()
            else:
                st.markdown("""
                <div class="alert-card">
                    <h3>❌ Verification Failed</h3>
                    <p>Incorrect answer. Please try again or contact your bank.</p>
                    <p>⚠️ Your account has been temporarily protected. Please contact your family.</p>
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        if st.button("❌ Cancel Transaction"):
            st.markdown("""
            <div class="warning-card">
                <h3>⏸️ Transaction Cancelled</h3>
                <p>Your transaction has been cancelled for security reasons.</p>
            </div>
            """, unsafe_allow_html=True)
            st.session_state.knowledge_check_passed = False

# ==================== Step 2: CareCircle Alert ====================
elif st.session_state.knowledge_check_passed and not st.session_state.carecircle_alert_sent:
    st.markdown("---")
    st.markdown("## 👨‍👩‍👧‍👦 Step 2: CareCircle Alert")
    
    # Check if amount exceeds limit
    if st.session_state.transaction_amount > 10000:
        st.markdown(f"""
        <div class="warning-card">
            <h3>⚠️ Large Transfer Detected</h3>
            <p>Transfer amount <strong>HKD {st.session_state.transaction_amount:,}</strong> exceeds preset limit (HKD 10,000)</p>
            <p>System has automatically triggered CareCircle protection mechanism</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Family members list
        family_members = [
            {"name": "David Chen (Son)", "phone": "+852 9123 4567"},
            {"name": "Lisa Chen (Daughter)", "phone": "+852 9234 5678"},
            {"name": "Mary Chen (Spouse)", "phone": "+852 9345 6789"}
        ]
        
        # Send alerts
        alerts = send_carecircle_alert(st.session_state.transaction_amount, st.session_state.recipient, family_members)
        
        st.markdown("### 📱 Alert Notifications Sent")
        
        for alert in alerts:
            st.markdown(f"""
            <div class="step-card">
                <p><strong>📲 Sent to:</strong> {alert['recipient']} ({alert['phone']})</p>
                <p><strong>💬 Message:</strong> {alert['message']}</p>
                <p><strong>Status:</strong> ✅ {alert['status']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Family confirmation simulation
        st.markdown("### 👪 Family Confirmation")
        
        st.info("💡 SMS messages have been sent to all CareCircle members. The transaction will proceed only after family confirmation.")
        
        family_approval = st.radio(
            "Has the family confirmed this transfer?",
            ["Awaiting confirmation...", "✅ Approved", "❌ Rejected"],
            index=0
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Confirm Approval", type="primary"):
                if family_approval == "✅ Approved":
                    st.session_state.carecircle_alert_sent = True
                    st.session_state.step = 3
                    st.markdown("""
                    <div class="success-card">
                        <h3>✅ Family Confirmed</h3>
                        <p>Family has approved this transfer. Proceeding to cooling period.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    time.sleep(1)
                    st.rerun()
                else:
                    st.warning("Please confirm that family has approved the transfer.")
        
        with col2:
            if st.button("❌ Reject Transfer"):
                st.markdown("""
                <div class="alert-card">
                    <h3>🚫 Transaction Rejected</h3>
                    <p>The transfer has been rejected by family verification.</p>
                </div>
                """, unsafe_allow_html=True)
                st.session_state.knowledge_check_passed = False
                st.session_state.carecircle_alert_sent = False
    else:
        # Amount below limit, skip CareCircle
        st.markdown(f"""
        <div class="success-card">
            <h3>✅ Amount Below Limit</h3>
            <p>Transfer amount HKD {st.session_state.transaction_amount:,} is below the HKD 10,000 limit.</p>
            <p>CareCircle alert not required for this transaction.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Continue to Cooling Period"):
            st.session_state.carecircle_alert_sent = True
            st.session_state.step = 3
            st.rerun()

# ==================== Step 3: Cooling Off Period ====================
elif st.session_state.carecircle_alert_sent and not st.session_state.transaction_pending:
    st.markdown("---")
    st.markdown("## ⏰ Step 3: Cooling Off Period")
    
    st.markdown("""
    <div class="warning-card">
        <h3>⏰ 2-Hour Cooling Period Active</h3>
        <p>All transfers to new payees require a 2-hour waiting period for security.</p>
        <p>This helps prevent fraudulent transactions and gives you time to verify.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Transaction details summary
    st.markdown("### 📋 Transaction Summary")
    
    summary_col1, summary_col2 = st.columns(2)
    with summary_col1:
        st.markdown(f"""
        **Recipient:** {st.session_state.recipient}<br>
        **Amount:** HKD {st.session_state.transaction_amount:,}<br>
        **Status:** Pending Verification
        """, unsafe_allow_html=True)
    
    with summary_col2:
        st.markdown(f"""
        **Initiated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
        **Completion Time:** {(datetime.now() + timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')}<br>
        **Cooling Period:** 2 Hours
        """, unsafe_allow_html=True)
    
    # Start cooling period
    if not st.session_state.pending_time:
        st.session_state.pending_time = start_cooling_period()
        st.session_state.transaction_pending = True
    
    # Display timer
    remaining = get_remaining_time()
    
    st.markdown(f"""
    <div style="text-align: center;">
        <div class="timer">⏰ {remaining}</div>
        <p>Remaining Cooling Period</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress bar for cooling period
    if st.session_state.pending_time:
        total_seconds = 2 * 60 * 60  # 2 hours in seconds
        remaining_seconds = max(0, (st.session_state.pending_time - datetime.now()).total_seconds())
        progress_percentage = (total_seconds - remaining_seconds) / total_seconds
        st.progress(min(progress_percentage, 1.0))
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("⏸️ Cancel Transaction", use_container_width=True):
            st.markdown("""
            <div class="alert-card">
                <h3>✅ Transaction Cancelled</h3>
                <p>Your transaction has been successfully cancelled.</p>
            </div>
            """, unsafe_allow_html=True)
            # Reset all states
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()
    
    with col2:
        st.info("💡 You can cancel anytime during cooling period")
    
    with col3:
        st.warning("⚠️ Transaction will auto-complete after 2 hours")

# ==================== Transaction Complete ====================
elif st.session_state.transaction_pending and st.session_state.pending_time:
    if datetime.now() >= st.session_state.pending_time:
        st.markdown("---")
        st.markdown("""
        <div class="success-card">
            <h1>✅ Transaction Completed Successfully!</h1>
            <p>All security checks have been passed. Your transfer has been processed.</p>
            <hr>
            <h3>📊 Transaction Summary</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Recipient", st.session_state.recipient)
            st.metric("Amount", f"HKD {st.session_state.transaction_amount:,}")
        with col2:
            st.metric("Completion Time", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            st.metric("Security Checks", "3/3 Passed")
        
        if st.button("🔄 Start New Transaction", type="primary"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()
    else:
        # Still in cooling period, show timer
        remaining = get_remaining_time()
        st.markdown(f"""
        <div style="text-align: center;">
            <div class="timer">⏰ {remaining}</div>
            <p>Remaining Cooling Period</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.pending_time:
            total_seconds = 2 * 60 * 60
            remaining_seconds = max(0, (st.session_state.pending_time - datetime.now()).total_seconds())
            progress_percentage = (total_seconds - remaining_seconds) / total_seconds
            st.progress(min(progress_percentage, 1.0))

# ==================== Footer ====================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6B7280; padding: 20px;">
    <p><strong>🛡️ Senior Shield Mode | Elderly Banking Protection System</strong></p>
    <p>Three-Layer Security: Knowledge Check + CareCircle Alert + Cooling Off Period</p>
    <p>© 2024 Senior Shield Technologies | All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)
