import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Description'])

def add_expense(date, category, amount, description):
    new_expense = pd.DataFrame([[date, category, amount, description]], columns=st.session_state.expenses.columns)
    st.session_state.expenses = pd.concat([st.session_state.expenses, new_expense], ignore_index=True)

def load_expenses():
    uploaded_file = st.file_uploader("Choose a file", type=['csv'])
    if uploaded_file is not None:
        st.session_state.expenses = pd.read_csv(uploaded_file)

def save_expenses():
    st.session_state.expenses.to_csv('expenses.csv', index=False)
    st.success("Expenses saved successfully")

def visualize_expenses():
    if not st.session_state.expenses.empty:
        fig, ax = plt.subplots()
        sns.barplot(data=st.session_state.expenses, x='Category', y="Amount", ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.warning("No Expenses to Visualize!")

st.title("Daily Expense Tracker")

with st.sidebar:
    st.header('Add Expense')
    date = st.date_input("Date")
    category = st.selectbox('Category', ['Food', 'Transport', 'Entertainment', 'Utilities', 'Other'])
    amount = st.number_input('Amount', min_value=0.0, format="%.2f")
    description = st.text_input('Description')
    if st.button('Add'):
        add_expense(date, category, amount, description)
        st.success("Expense Added!")
        
    st.header('File Operations')
    if st.button('Save Expenses'):
        save_expenses()
    if st.button('Load Expenses'):
        load_expenses()

st.header('Expenses')
st.write(st.session_state.expenses)

st.header('Visualization')
if st.button('Visualize Expenses'):
    visualize_expenses()

def edit_expense(index, date, category, amount, description):
    st.session_state.expenses.loc[index, 'Date'] = date
    st.session_state.expenses.loc[index, 'Category'] = category
    st.session_state.expenses.loc[index, 'Amount'] = amount
    st.session_state.expenses.loc[index, 'Description'] = description

st.header('Select Expenses To Edit')

if not st.session_state.expenses.empty:
    selected_index = st.selectbox("Select an expense to edit", st.session_state.expenses.index)
    selected_expense = st.session_state.expenses.loc[selected_index]

    st.write("### Edit Selected Expense")
    edit_date = st.date_input("Date", value=pd.to_datetime(selected_expense['Date']))
    edit_category = st.selectbox('Category', ['Food', 'Transport', 'Entertainment', 'Utilities', 'Other'], index=['Food', 'Transport', 'Entertainment', 'Utilities', 'Other'].index(selected_expense['Category']))
    edit_amount = st.number_input('Amount', min_value=0.0, format="%.2f", value=selected_expense['Amount'])
    edit_description = st.text_input('Description', value=selected_expense['Description'])

    if st.button('Update Expense'):
        edit_expense(selected_index, edit_date, edit_category, edit_amount, edit_description)
        st.success("Expense Updated!")
else:
    st.write("No expenses to edit.")

st.write(st.session_state.expenses)

