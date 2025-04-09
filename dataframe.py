import re
import streamlit as st
import pandas as pd
import datetime as dt

st.markdown("Data Visualization")
st.sidebar.write("Data Visualization")

data_df = pd.read_csv("./data/Chocolate Sales.csv")
st.subheader("Sample data")
st.dataframe(data_df.head())

st.subheader("Data information's")
info_dict = {
    'Column Name': [],
    'Num Rows': [],
    'Non-Null Count': [],
    'Dtype': []
}
for column in data_df.columns:
    info_dict['Column Name'].append(column)
    info_dict['Non-Null Count'].append(data_df[column].notnull().sum())
    info_dict['Dtype'].append(str(data_df[column].dtypes))
    info_dict['Num Rows'].append(data_df[column].__len__())

st.dataframe(pd.DataFrame(info_dict))


def clean_data():
    """
    :return: pd.Dataframe
    """
    clean_df = data_df
    clean_df['Amount'] = pd.to_numeric(data_df['Amount'].apply(lambda x: re.sub(r'\D', '', x)), errors="coerce")
    data_df['Date'] = data_df['Date'].str.strip()
    clean_df['Date'] = pd.to_datetime(data_df['Date'], errors="coerce", format='%d-%b-%y')
    return clean_df


formatted_df = clean_data()
prod_options = formatted_df['Product'].unique()
person_options = formatted_df["Sales Person"].unique()
selected_prod = st.selectbox("Select you product To get country based sales info", options=prod_options)
prod_data = formatted_df[formatted_df['Product'] == selected_prod].groupby("Country")[['Amount', "Boxes Shipped"]].sum(
).reset_index()

prod_data = prod_data.set_index("Country")
st.dataframe(prod_data)
st.subheader("Graphical information")
st.line_chart(data=prod_data)

min_date = formatted_df["Date"].min().date()
max_date = formatted_df["Date"].max().date()

col_1, col_2, col_3 = st.columns(3)
selected_person = col_1.selectbox("Sales Person country based sales info", options=person_options)
start_date = col_2.date_input("Start date", min_value=min_date, max_value=max_date, value=min_date)
end_date = col_3.date_input("End date", min_value=min_date, max_value=max_date, value=max_date)
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)
person_data = formatted_df[(formatted_df['Sales Person'] == selected_person) & (formatted_df['Date'] >= start_date)
                           & (formatted_df['Date'] <= end_date)].groupby("Country")[['Amount', "Boxes Shipped"]].sum(
).reset_index()

person_data = person_data.set_index("Country")
st.dataframe(person_data)
st.subheader("Graphical information")
st.bar_chart(person_data, stack=False)

box_data = formatted_df[['Date', 'Product', 'Boxes Shipped']]
box_data['Month'] = box_data['Date'].apply(lambda x: x.month)
box_data = box_data.groupby(['Month', 'Product'])['Boxes Shipped'].sum(
).reset_index()

box_data = box_data.pivot(index='Month', columns='Product', values='Boxes Shipped')
st.subheader("Month and product moment")
st.scatter_chart(box_data, )

low_box_shipment = formatted_df.groupby(['Product', 'Country'])[
    ['Boxes Shipped', "Amount"]].sum().reset_index().sort_values(['Boxes Shipped', 'Amount'], ascending=False)
print("*" * 30)
print(formatted_df)
print(low_box_shipment)
print(low_box_shipment[low_box_shipment['Boxes Shipped'] <600])
print(low_box_shipment[low_box_shipment['Product'] == "Baker's Choco Chips"])
