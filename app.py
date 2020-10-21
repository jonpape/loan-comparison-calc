import streamlit as st
import numpy_financial as npf
import pandas as pd


def loan_payments(list_name, loan_length, mth_payment):
    """ Function gets the principal, loan_term, and interest rate and
    returns a list with total paid and a list with interest paid."""

    total_interest = 0

    # variable calculations for the length of the loan
    for i in range(loan_length):

        # get principal for last end date
        principal = list_name[i]

        # calc monthly interest payment
        monthly_interest_payment = monthly_interest * principal

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
            monthly_interest_payment = monthly_interest * ending_balance
            # calc interest paid
            total_interest += monthly_interest_payment
            # returns total paid and total interest paid
            return total_interest


title_html = "<h1>Compare loan cost, interest & duration by making extra payments each month</h1>"
st.markdown(title_html, unsafe_allow_html=True)

page_text = "<p>It has always amazed me how paying a little more each month " +\
            "can have a significant impact in the length of your loan.<p>" +\
            "<p>This calculator was created to show how, if you pay a little" +\
            " extra each month, you can significantly lower your total " +\
            "loan terms by a lot.</p>"
st.markdown(page_text, unsafe_allow_html=True)

st.sidebar.markdown("Enter your loan information then test different incremental payments.")
# get inputs
loan_amount = st.sidebar.text_input("Enter the total amount of your loan: ", 40000)
loan_term = st.sidebar.text_input("Enter the length of your loan in months: ", 84)
loan_rate = st.sidebar.text_input("Enter the interest rate of your loan (example: 3.75): ", 3.75)
option1_payment = st.sidebar.text_input("Option 1: Pay an extra x amount per month: ", 50)
option2_payment = st.sidebar.text_input("Option 2: Pay an extra x amount per month: ", 100)
option3_payment = st.sidebar.text_input("Option 3: Pay an extra x amount per month: ", 200)

try:
    loan_amount = int(loan_amount)
    loan_term = int(loan_term)
    loan_rate = float(loan_rate)
    option1_payment = int(option1_payment)
    option2_payment = int(option2_payment)
    option3_payment = int(option3_payment)
except TypeError:
    print('There is an error with the inputs in the sidebar. Please reenter your numbers.')


# fixed calculations for the length of loan
monthly_interest = (loan_rate / 12) / 100
monthly_payment = npf.pmt(monthly_interest, loan_term, loan_amount) * -1

original = [loan_amount]
option_1 = [loan_amount]  # pay $50 more
option_2 = [loan_amount]  # pay $100 more
option_3 = [loan_amount]  # pay $200 more

# list for total interest payments
total_interest_payments = []

total_interest = loan_payments(original, loan_term, monthly_payment)
total_interest_payments.append(total_interest)

total_interest = loan_payments(option_1, loan_term, monthly_payment + option1_payment)
total_interest_payments.append(total_interest)

total_interest = loan_payments(option_2, loan_term, monthly_payment + option2_payment)
total_interest_payments.append(total_interest)

total_interest = loan_payments(option_3, loan_term, monthly_payment + option3_payment)
total_interest_payments.append(total_interest)


Chart_title = '<div style="text-align: center"><h2>Amount of principal ' \
              'by loan term (months).</h2></div'
st.markdown(Chart_title, unsafe_allow_html=True)

header = ['original', 'option 1', 'option 2', 'option 3']

df_options = pd.DataFrame([original, option_1, option_2, option_3])
df_transposed = df_options.transpose()
df_transposed.columns = header
chart_data = df_transposed

st.area_chart(chart_data)

under_chart_html = '<p>Original loan term is ' + str(loan_term) + ' months.</p><block><ul>' + \
                   '<li>Total cost: $' + str(int(loan_amount + total_interest_payments[0])) + \
                   '</li><li>Total interest: $' + str(int(total_interest_payments[0])) + '</li>' + \
                   '<li>Monthly payment: $' + str(int(monthly_payment)) + '</li></ul></block>'

under_chart_html = under_chart_html + '<p>Option 1 loan term is ' + str(len(option_1)) + \
                   ' months.</p><block><ul>' + \
                   '<li>Total cost: $' + str(int(loan_amount + total_interest_payments[1])) + \
                   '</li><li>Total interest: $' + str(int(total_interest_payments[1])) + \
                   '</li><li>Monthly payment: $' + str(int(monthly_payment + option1_payment)) + \
                   '</li></ul></block>'

under_chart_html = under_chart_html + '<p>Option 2 loan term is ' + str(len(option_2)) + \
                   ' months.</p><block><ul>' + \
                   '<li>Total cost: $' + str(int(loan_amount + total_interest_payments[2])) + \
                   '</li><li>Total interest: $' + str(int(total_interest_payments[2])) + \
                   '</li><li>Monthly payment: $' + str(int(monthly_payment + option2_payment)) + \
                   '</li></ul></block>'

under_chart_html = under_chart_html + '<p>Option 3 loan term is ' + str(len(option_3)) + \
                   ' months.</p><block><ul>' + \
                   '<li>Total cost: $' + str(int(loan_amount + total_interest_payments[3])) + \
                   '</li><li>Total interest: $' + str(int(total_interest_payments[3])) + \
                   '</li><li>Monthly payment: $' + str(int(monthly_payment + option3_payment)) + \
                   '</li></ul></block>'

under_chart_html = under_chart_html + '<br><br><br><p>Website is for entertainment purposes only. ' + \
                   'Created by <a href="http://jonpape.com">Jon Pape</a>.</p></block>'

st.markdown(under_chart_html, unsafe_allow_html=True)
