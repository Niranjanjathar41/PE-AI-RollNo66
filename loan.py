import streamlit as st
import math

st.set_page_config(page_title="Loan Expert System", page_icon="💰", layout="wide")

st.markdown("""<style>
.main-header {font-size: 2.5rem; color: #4F46E5; font-weight: bold;}
.success-box {background: #ECFDF5; padding: 1.5rem; border-radius: 0.5rem; border-left: 4px solid #10B981;}
.error-box {background: #FEF2F2; padding: 1.5rem; border-radius: 0.5rem; border-left: 4px solid #EF4444;}
</style>""", unsafe_allow_html=True)

st.markdown('<p class="main-header">💰 Loan Recommendation Expert System</p>', unsafe_allow_html=True)

if 'rec' not in st.session_state:
    st.session_state.rec = None

with st.sidebar:
    st.header("📋 Application Details")
    age = st.slider("Age", 18, 70, 25)
    dependents = st.slider("Dependents", 0, 8, 1)
    income = st.slider("Monthly Income (₹)", 10000, 500000, 50000, 5000)
    expenses = st.slider("Monthly Expenses (₹)", 5000, 200000, 15000, 1000)
    loans = st.slider("Existing Loan Payments (₹)", 0, 100000, 5000, 1000)
    emp_type = st.selectbox("Employment", ["Salaried", "Self Employed", "Business Owner"])
    emp_years = st.slider("Employment Years", 0.0, 30.0, 2.0, 0.5)
    credit = st.slider("Credit Score", 300, 850, 700, 10)
    purpose = st.selectbox("Purpose", ["Personal", "Home Purchase", "Vehicle", "Education", "Business"])
    amount = st.slider("Loan Amount (₹)", 50000, 10000000, 200000, 50000)
    collateral = st.radio("Collateral?", ["No", "Yes"])
    analyze = st.button("🔍 Analyze", use_container_width=True)

def calc_emi(p, r, t):
    mr = r / 1200
    return round(p * mr * (1 + mr)**t / ((1 + mr)**t - 1), 2)

def recommend(age, inc, cr, ey, amt, et, col, purp, lns, exp, dep):
    dti = ((lns + exp) / inc) * 100 if inc > 0 else 0
    mult = {750: 5, 700: 4, 650: 3.5}.get(next((k for k in [750, 700, 650] if cr >= k), 600), 3)
    mult *= 0.5 if dti > 50 else 0.7 if dti > 40 else 0.85 if dti > 30 else 1
    max_loan = inc * 12 * mult
    
    rate = {750: 7.5, 700: 9, 650: 10.5, 600: 12}.get(next((k for k in [750, 700, 650, 600] if cr >= k), 300), 15)
    rate -= 0.5 if et == "Salaried" else 0
    rate -= 1 if col == "Yes" else 0
    
    cw = {750: "Excellent", 700: "Good", 650: "Fair", 600: "Poor"}.get(next((k for k in [750, 700, 650, 600] if cr >= k), 300), "Very Poor")
    lt, ten = {"Personal": ("Personal Loan", 36), "Home Purchase": ("Home Loan", 240), "Vehicle": ("Vehicle Loan", 60), 
               "Education": ("Education Loan", 84), "Business": ("Business Loan", 60)}.get(purp, ("Personal Loan", 36))
    
    appr, rsns, wrns = True, [], []
    
    if not 21 <= age <= 65: appr, rsns = False, rsns + ["❌ Age must be 21-65"]
    if inc < 20000: appr, rsns = False, rsns + ["❌ Income < ₹20,000"]
    if cr < 600: appr, rsns = False, rsns + ["❌ Credit score < 600"]
    if ey < 0.5: appr, rsns = False, rsns + ["❌ Need 6+ months employment"]
    elif ey < 1: wrns.append("⚠️ Low employment duration")
    if dti > 50: appr, rsns = False, rsns + ["❌ DTI > 50%"]
    elif dti > 40: wrns.append("⚠️ High DTI")
    if amt > max_loan * 1.5: appr, rsns = False, rsns + ["❌ Amount too high"]
    elif amt > max_loan: wrns.append(f"⚠️ Exceeds limit of ₹{max_loan:,.0f}")
    
    app_amt = min(amt, max_loan)
    emi = calc_emi(app_amt, rate, ten)
    
    return {'approved': appr, 'reasons': rsns, 'warnings': wrns, 'loan_type': lt, 'approved_amount': app_amt,
            'max_loan': max_loan, 'interest_rate': round(rate, 2), 'tenure': ten, 'emi': emi, 
            'creditworthiness': cw, 'dti': dti, 'total_payable': emi * ten}

if analyze:
    with st.spinner('🔄 Analyzing...'):
        st.session_state.rec = recommend(age, income, credit, emp_years, amount, emp_type, collateral, purpose, loans, expenses, dependents)

if st.session_state.rec:
    r = st.session_state.rec
    
    if r['approved']:
        st.markdown(f'<div class="success-box"><h2>✅ Loan Approved!</h2></div>', unsafe_allow_html=True)
        st.markdown("### 📊 Loan Details")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("🏦 Type", r['loan_type'])
        c1.metric("💰 Amount", f"₹{r['approved_amount']:,.0f}")
        c2.metric("📈 Rate", f"{r['interest_rate']}% p.a.")
        c2.metric("📅 Tenure", f"{r['tenure']} months")
        c3.metric("💳 EMI", f"₹{r['emi']:,.2f}")
        c3.metric("💵 Total", f"₹{r['total_payable']:,.2f}")
        
        st.markdown("---")
        c4, c5 = st.columns(2)
        c4.metric("Credit", r['creditworthiness'])
        c5.metric("DTI", f"{r['dti']:.2f}%")
        
        if r['warnings']:
            st.markdown("### ⚠️ Warnings")
            for w in r['warnings']: st.warning(w)
        
        st.markdown("### 📉 Breakdown")
        interest = r['total_payable'] - r['approved_amount']
        c6, c7 = st.columns(2)
        c6.metric("Principal", f"₹{r['approved_amount']:,.0f}")
        c7.metric("Interest", f"₹{interest:,.2f}")
        st.progress(interest / r['total_payable'])
        
    else:
        st.markdown('<div class="error-box"><h2>❌ Not Approved</h2></div>', unsafe_allow_html=True)
        st.markdown("### 🚫 Reasons")
        for rsn in r['reasons']: st.error(rsn)
        st.info("💡 Improve the highlighted areas and reapply.")
else:
    st.info("👈 Fill details in sidebar and click Analyze")
    st.markdown("### 🎯 How It Works")
    c1, c2, c3 = st.columns(3)
    c1.markdown("#### 📝 Input\n- Personal info\n- Financials\n- Credit score")
    c2.markdown("#### 🤖 Analysis\n- Rule-based\n- Risk check\n- Eligibility")
    c3.markdown("#### ✅ Results\n- Decision\n- Terms\n- EMI")

st.markdown("---")
st.markdown("<div style='text-align: center; color: #6B7280;'><p>💡 Automated expert system. Final approval may require verification.</p></div>", unsafe_allow_html=True)