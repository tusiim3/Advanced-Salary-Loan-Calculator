import streamlit as st
import pandas as pd
import requests
import os
import json

# Page configuration
st.set_page_config(page_title="Advanced Salary & Loan Calculator", layout="centered")

# API URL - use environment variable or default to backend service
API_URL = os.getenv("API_URL", "http://backend:8000")

def main():
    st.title("💰 Advanced Salary Loan Calculator")
    st.markdown("---")

    # Main layout 
    col1, col2, col3, col4 = st.columns([2, 1.5, 0.5, 1.5])

    with col1:
        gross_salary = st.number_input("Gross Salary:", placeholder = "e.g. 750000")
        if gross_salary:
            st.session_state.gross_salary = gross_salary
    
    with col2:
        currency = st.selectbox("Currency:", ["UGX", "RWF", "KES", "TZS", "USD", "GBP", "EUR"], key="currency")
    
    with col3:
        st.markdown("<br><b>per</b>", unsafe_allow_html = True)
            
    with col4:
        pay_frequency = st.selectbox("", ["Week", "2 Weeks", "Month"], index=2)

    st.markdown("---")

    # Loan Type Selection
    st.subheader("Choose Loan Type")
    loan_type = st.radio("", ["Advance", "Loan", "Both"], horizontal = True)

    if loan_type in ["Advance", "Both"]:
        st.markdown("### 💸 Salary Advance")
        advance_amount = st.number_input("Requested Advance Amount:", placeholder = "e.g. 150000")

        if advance_amount and gross_salary:
            try:
                payload = {
                    "gross_salary": gross_salary,
                    "advance_amount": advance_amount,
                    "currency": currency,
                    "pay_frequency": pay_frequency
                }

                response = requests.post(f"{API_URL}/calculate_advance", json=payload)
                if response.status_code == 200:
                    """data = response.json()
                    st.success(f"Eligible Advance Amount: {data['eligible_advance']}")
                    st.info(f"Processing Fee: {data['processing_fee']}")
                    st.info(f"Total Repayment: {data['total_repayment']}")
                else:
                   st.error("Error calculating advance. Please try again.")
"""
                    data = response.json()

                    st.markdown(f"**Maximum Eligible Adavance:** {data['max_advance']:,.0f} {currency}")

                    if data["eligible"]:
                        st.success("✅ Eligible")
                        st.write(f"**Fee Rate ({data[ 'fee_rate']*100:.0f}%):** {data['fee']:,.0f} {currency}")
                        st.write(f"**Total Repayable on Next Salary:** {data['total_repayable']:,.0f} {currency}")
                    else:
                        st.error("❌ You are not eligible for this amount.")
                else:
                    st.error("Error contacting advance calculation API.")
            except:
                st.error("Please enter a valid number for advance amount.")
        
        st.markdown("---")

    if loan_type in ["Loan", "Both"]:
        st.markdown("### 🏦 Salary Loan")

        loan_amount = st.number_input("Requested Loan Amount:", placeholder = "e.g. 500000")
        loan_term = st.selectbox("Loan Term (months)", [3, 6, 12, 18, 24])
        interest_rate = st.slider("Annual Interest Rate (%)", 1, 30, 15)

        if loan_amount:
            try:
                payload = {
                    "loan_amount": loan_amount,
                    "loan_term": loan_term,
                    "interest_rate": interest_rate,
                    "currency": currency
                }

                response = requests.post(f"{API_URL}/calculate_loan", json=payload)

                if response.status_code == 200:
                    data = response.json()
                    st.success("Loan Calculation Successful ✅")

                    st.write(f"**Monthly EMI:** {data['emi']:,.0f} {currency}")
                    st.write(f"**Total Repayable:** {data['total_repayable']:,.0f} {currency}")

                else:
                    st.error("Error contacting loan calculation API.")

            except:
                st.error("Please enter valid number for loan amount.")

    st.markdown("---")

                    





# Run the main function
if __name__ == "__main__":
    main()
    
                                


                






