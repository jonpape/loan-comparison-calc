import streamlit as st
import numpy_financial as npf
import pandas as pd


def loan_payments(list_name, amount, term, rate, mth_interest, mth_payment):
    """ Function gets the list, principal, loan_term, and interest rate and
    returns a list with total paid and a list with interest paid."""

    total_interest = 0

    # variable calculations for the length of the loan
    for i in range(term):

        # get principal for last end date
        principal = list_name[i]

        # calc monthly interest payment
        monthly_interest_payment = mth_interest * principal

        # calc interest paid
        total_interest += monthly_interest_payment

        # calc monthly principal payment
        monthly_principal_paid = mth_payment - monthly_interest_payment

        # calc ending balance
        ending_balance = int(principal - monthly_principal_paid)

        # update the principal balance
        list_name.append(ending_balance)

        # if ending balance - monthly payment is less than 0
        if ending_balance - (mth_payment - monthly_interest_payment) <= 0:
            # calc monthly interest payment
            monthly_interest_payment = mth_interest * ending_balance
            # calc interest paid
            total_interest += monthly_interest_payment
            # returns total paid and total interest paid
            return total_interest


def monthly_payment_calc(loan_amount, loan_term, loan_rate):
    """Calculates the monthly payment of a loan"""
    # fixed calculations for the length of loan

    # calculates the monthly interest
    monthly_interest = (loan_rate / 12) / 100
    # calculates the monthly payment
    monthly_payment = npf.pmt(monthly_interest, loan_term, loan_amount) * -1
    # returns the monthly payment
    return monthly_interest, monthly_payment


title_html = "<h1>Compare loan cost, interest & duration by making extra payments each month</h1>"
st.markdown(title_html, unsafe_allow_html=True)

page_text = "<p>It has always amazed me how paying a little more each month " + \
            "can have a significant impact in the length of your loan.<p>" + \
            "<p>This calculator was created to show how, if you pay a little" + \
            " extra each month, you can significantly lower your total " + \
            "loan terms by a lot.</p>"
st.markdown(page_text, unsafe_allow_html=True)

st.markdown("Enter the loan information you would like to compare.")

col1, col2, col3, col4 = st.beta_columns(4)

loan_information = {}

# get inputs
loan_amount1 = col1.text_input("Enter the total amount of your loan: ", 40000)
loan_term1 = col1.text_input("Enter the length of your loan in months: ", 84)
loan_rate1 = col1.text_input("Enter the interest rate of your loan: ", 4.80)

loan_data = {"loan1": {"amount": int(loan_amount1),
                       "term": int(loan_term1),
                       "rate": float(loan_rate1),
                       "total_interest": 0,
                       "mth_interest": 0.0,
                       "payment": 0.0}}

loan_amount2 = col2.text_input("Enter the total amount of your loan: ", 40000)
loan_term2 = col2.text_input("Enter the length of your loan in months: ", 72)
loan_rate2 = col2.text_input("Enter the interest rate of your loan: ", 4.50)

loan_data = {"loan2": {"amount": int(loan_amount2),
                       "term": int(loan_term2),
                       "rate": float(loan_rate2),
                       "total_interest": 0,
                       "mth_interest": 0.0,
                       "payment": 0.0}}

loan_amount3 = col3.text_input("Enter the total amount of your loan: ", 40000)
loan_term3 = col3.text_input("Enter the length of your loan in months: ", 60)
loan_rate3 = col3.text_input("Enter the interest rate of your loan: ", 4.10)

loan_data = {"loan3": {"amount": int(loan_amount3),
                       "term": int(loan_term3),
                       "rate": float(loan_rate3),
                       "total_interest": 0,
                       "mth_interest": 0.0,
                       "payment": 0.0}}

loan_amount4 = col4.text_input("Enter the total amount of your loan: ", 40000)
loan_term4 = col4.text_input("Enter the length of your loan in months: ", 36)
loan_rate4 = col4.text_input("Enter the interest rate of your loan: ", 3.50)

loan_data = {"loan4": {"amount": int(loan_amount4),
                       "term": int(loan_term4),
                       "rate": float(loan_rate4),
                       "total_interest": 0,
                       "mth_interest": 0.0,
                       "payment": 0.0}}

# calculate monthly payment
loan_data["loan1"]["payment"], loan_data["loan1"]["mth_interest"] = monthly_payment_calc(loan_data["loan1"]["amount"],
                                                                                          loan_data["loan1"]["term"],
                                                                                          loan_data["loan1"]["rate"], )
loan_data["loan2"]["payment"], loan_data["loan2"]["mth_interest"] = monthly_payment_calc(loan_data["loan2"]["amount"],
                                                                                         loan_data["loan2"]["term"],
                                                                                         loan_data["loan2"]["rate"], )
loan_data["loan3"]["payment"], loan_data["loan3"]["mth_interest"] = monthly_payment_calc(loan_data["loan3"]["amount"],
                                                                                         loan_data["loan3"]["term"],
                                                                                         loan_data["loan3"]["rate"], )
loan_data["loan4"]["payment"], loan_data["loan4"]["mth_interest"] = monthly_payment_calc(loan_data["loan4"]["amount"],
                                                                                         loan_data["loan4"]["term"],
                                                                                         loan_data["loan4"]["rate"], )



# list of lists for all loans of all payments
loan1_payments = []
loan2_payments = []
loan3_payments = []
loan4_payments = []

#function loan payments creates the list for the payments and returns the total interest paid
loan_data["loan1"]["total_interest"] = loan_payments(loan1_payments,
                                                     loan_data["loan1"]["amount"],
                                                     loan_data["loan1"]["term"],
                                                     loan_data["loan1"]["rate"],
                                                     loan_data["loan1"]["mth_interest"],
                                                     loan_data["loan1"]["payment"])
loan_data["loan2"]["total_interest"] = loan_payments(loan2_payments,
                                                     loan_data["loan2"]["amount"],
                                                     loan_data["loan2"]["term"],
                                                     loan_data["loan2"]["rate"],
                                                     loan_data["loan2"]["mth_interest"],
                                                     loan_data["loan2"]["payment"])
loan_data["loan3"]["total_interest"] = loan_payments(loan3_payments,
                                                     loan_data["loan3"]["amount"],
                                                     loan_data["loan3"]["term"],
                                                     loan_data["loan3"]["rate"],
                                                     loan_data["loan3"]["mth_interest"],
                                                     loan_data["loan3"]["payment"])
loan_data["loan4"]["total_interest"] = loan_payments(loan4_payments,
                                                     loan_data["loan4"]["amount"],
                                                     loan_data["loan4"]["term"],
                                                     loan_data["loan4"]["rate"],
                                                     loan_data["loan4"]["mth_interest"],
                                                     loan_data["loan4"]["payment"])


Chart_title = '<div style="text-align: center"><h2>Amount of principal ' \
              'by loan term (months).</h2></div'
st.markdown(Chart_title, unsafe_allow_html=True)

header = ['loan 1', 'loan 2', 'loan 3', 'loan 4']

df_options = pd.DataFrame([loan1_payments, loan2_payments, loan3_payments, loan4_payments])
df_transposed = df_options.transpose()
df_transposed.columns = header
chart_data = df_transposed

st.area_chart(chart_data)

under_chart_html = '<p>Loan 1 term is ' + str(loan_data["loan1"]["term"]) + ' months.</p><block><ul>' + \
                   '<li>Total cost: $' + str(int(loan_data["loan1"]["amount"] + loan_data["loan1"]["total_interest"])) + \
                   '</li><li>Total interest: $' + str(int(loan_data["loan1"]["total_interest"])) + '</li>' + \
                   '<li>Monthly payment: $' + str(int(loan_data["loan1"]["payment"])) + '</li></ul></block>'

under_chart_html = under_chart_html + '<p>Loan 2 term is ' + str(loan_data["loan2"]["term"]) + ' months.</p><block><ul>' + \
                   '<li>Total cost: $' + str(int(loan_data["loan2"]["amount"] + loan_data["loan2"]["total_interest"])) + \
                   '</li><li>Total interest: $' + str(int(loan_data["loan2"]["total_interest"])) + '</li>' + \
                   '<li>Monthly payment: $' + str(int(loan_data["loan2"]["payment"])) + '</li></ul></block>'

under_chart_html = under_chart_html + '<p>Loan 3 term is ' + str(loan_data["loan3"]["term"]) + ' months.</p><block><ul>' + \
                   '<li>Total cost: $' + str(int(loan_data["loan3"]["amount"] + loan_data["loan3"]["total_interest"])) + \
                   '</li><li>Total interest: $' + str(int(loan_data["loan3"]["total_interest"])) + '</li>' + \
                   '<li>Monthly payment: $' + str(int(loan_data["loan3"]["payment"])) + '</li></ul></block>'

under_chart_html = under_chart_html + '<p>Loan 4 term is ' + str(loan_data["loan4"]["term"]) + ' months.</p><block><ul>' + \
                   '<li>Total cost: $' + str(int(loan_data["loan4"]["amount"] + loan_data["loan4"]["total_interest"])) + \
                   '</li><li>Total interest: $' + str(int(loan_data["loan4"]["total_interest"])) + '</li>' + \
                   '<li>Monthly payment: $' + str(int(loan_data["loan4"]["payment"])) + '</li></ul></block>'

under_chart_html = under_chart_html + '<br><br><br><p>Website is for entertainment purposes only. ' + \
                   'Created by <a href="http://jonpape.com">Jon Pape</a>.</p></block>'

st.markdown(under_chart_html, unsafe_allow_html=True)
