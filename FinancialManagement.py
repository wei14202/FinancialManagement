
from unittest import case

import streamlit as st
import pandas as pd

def cpf_percentage(age):
    match age:
        case age if age <= 35:
            return 0.6217, 0.1891, 0.2162
        case age if age <= 45:
            return 0.5677, 0.1891, 0.2432
        case age if age <= 50:
            return 0.5136, 0.2162, 0.2702
        case age if age <= 55:
            return 0.4055, 0.3108, 0.2837
        case _:
            return 0.0, 0.0, 0.0

citizen = ["Malaysian", "Singaporean", "Others"]

st.title("Financial Management")
st.header("Information")

c1, c2, c3, c4 = st.columns(4)
with c1:
    gross = st.number_input("Total Wage:",0)
with c2:
    extra = st.number_input("Extra Income:",0)
with c3:
    age =st.number_input("Age(maximum of 55):",0,55)
with c4:
    duration = st.number_input("Year:",0,99)
OA = SA = MSA = 0
citizenship = st.selectbox("Citizenship:", citizen)
st.text("This program will considered you are working in the country of your citizenship, and the wage is in the currency of your citizenship, if you are foreign worker with no cpf/epf, please select others.")
match citizenship:
    case "Singaporean":
        currency = "S$"
    case "Malaysian":
        currency = "RM"
    case "Others":
        currency = "$"
        
if citizenship == "Singaporean":
    cpf = gross * 0.37
    income = gross * 0.8 + extra
    st.subheader("Initial Value in your CPF account")
    st.text("You may check your account value in CPF Mobile app")
    co1, co2, co3 = st.columns(3)
    with co1:
        OA = st.number_input("OA account value")
    with co2:
        SA = st.number_input("SA account value")
    with co3:
        MSA = st.number_input("MSA account value")
    for i in range(duration):
        oa, sa, msa = cpf_percentage(age + i)
        if gross * 13 < 96000: 
            NewOA = (OA + (cpf * oa * 13))
            OA = NewOA + ((OA + NewOA)/2)* 0.025
            NewSA = (SA + (cpf * sa * 13))
            SA = NewSA + ((SA + NewSA)/2) * 0.04
            NewMSA = (MSA + (cpf * msa * 13))
            MSA = NewMSA + ((MSA + NewMSA)/2) * 0.04
        else:
            cpf = 96000 * 0.37
            NewOA = (OA + (cpf * oa * 13))
            OA = NewOA + ((OA + NewOA)/2)* 0.025
            NewSA = (SA + (cpf * sa * 13))
            SA = NewSA + ((SA + NewSA)/2) * 0.04
            NewMSA = (MSA + (cpf * msa * 13))
            MSA = NewMSA + ((MSA + NewMSA)/2) * 0.04
    total_cpf = OA + SA + MSA
    cpf_data = {
         "OA Account": [OA],
         "SA Account": [SA],
         "MSA Account": [MSA],
         "Total": [total_cpf]
    }
    cpf_df = pd.DataFrame(cpf_data)
    st.dataframe(cpf_df.T.style.format(f"{currency}{{:.2f}}"))
    st.text("these value might be lesser than actual due to the 1% of additional interest")
elif citizenship == "Malaysian":
    if gross < 5000:
         epf = gross * 0.24
         income = gross * 0.87
    else:
        epf = gross * 0.23
        income = gross * 0.88 + extra
    st.subheader("Initial Value in your KWSP account")
    st.text("You may check your account value in KWSP Mobile app")
    co1, co2, co3 = st.columns(3)
    with co1:
        ACC1 = st.number_input("Account 1 account value")
    with co2:
        ACC2 = st.number_input("Account 2 account value")
    with co3:
        ACC3 = st.number_input("Account 3 account value")
    for i in range(duration):
            NewACC1 = (ACC1 + (epf * 0.75 * 13))
            ACC1 = NewACC1 + ((ACC1 + NewACC1)/2)* 0.025
            NewACC2 = (ACC2 + (epf * 0.15 * 13))
            ACC2 = NewACC2 + ((ACC2 + NewACC2)/2) * 0.025
            NewACC3 = (ACC3 + (epf * 0.05 * 13))
            ACC3 = NewACC3 + ((ACC3 + NewACC3)/2) * 0.025
    total_epf = ACC1 + ACC2 + ACC3
    epf_data = {
         "Account 1": [ACC1],
         "Account 2": [ACC2],
         "Account 3": [ACC3],
         "Total": [total_epf]
    }
    epf_df = pd.DataFrame(epf_data)
    st.dataframe(epf_df.T.style.format(f"{currency}{{:.2f}}"))
    st.text("these value might be lesser than actual because the interest is calculated based on 2.5% of the total EPF value (minimum guaranteed rate)")
else:
    income = gross + extra

st.header("Expenditure")
st.subheader("Neccesary")
if citizenship:
    st.text(f"50% of income(after CPF deduction): {currency} {income * 0.5} is recommended.")
else:
    st.text(f"50% of income: {currency} {income * 0.5} is recommended.")
c1, c2, c3, c4 = st.columns(4)
with c1:
    rent = st.number_input("Mortgage/Rent:")
with c2:
    food = st.number_input("Food:")
with c3:
    allowance = st.number_input("Allowance for Family:")
with c4:
    transport = st.number_input("Transport")
n_total = rent+food+allowance+transport
st.text(f"Total Neccesary Expenditure: {n_total}")
balance1 = income - n_total
st.text(f"balance: {balance1}")

st.subheader("Saving & Investment")
c1, c2 = st.columns(2)
with c1:
    down_saving = st.number_input("Saving for your desired or down payment:")
with c2:
    invest_saving = st.number_input("General Saving & Investment:")
balance2 = balance1 - down_saving - invest_saving
st.subheader(f"Dispensable Balance: {balance2}")

down_saving = down_saving * duration * 13
invest_saving = invest_saving * duration * 13
if citizenship == "Singaporean":
    saving = {
    "Wage": gross,
    "Saving(Down Payment)": [down_saving],
    "OA account + Saving(Down Payment)": [OA + down_saving],
    "Saving & Investment": [invest_saving]
    }
elif citizenship == "Malaysian":
    saving = {
    "Wage": gross,
    "Saving(Down Payment)": [down_saving],
    "Account 2 + Saving(Down Payment)": [ACC2 + down_saving],
    "Saving & Investment": [invest_saving]
    }
else:
    saving = {
    "Wage": gross,
    "Saving(Down Payment)": [down_saving],
    "Saving & Investment": [invest_saving]
    }
df_saving = pd.DataFrame(saving)
st.header("Overview of Saving")
st.dataframe(df_saving.T.style.format(f"{currency}{{:.2f}}"))
