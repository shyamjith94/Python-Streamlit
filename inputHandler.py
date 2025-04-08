import streamlit as st
import pandas as pd
from sampleData import address_table

st.sidebar.write("input handler")
st.subheader("Handling Different Type Input", divider="violet")

csv_data = ""


def table_data():
    """
    :return: st.table
    """
    df_data = pd.DataFrame(address_table)
    df_data.index.name = "Sl no"
    csv_data = df_data.to_csv(index=False)
    return st.table(df_data)


# column with input
col_one, col_two, col_three, col_four = st.columns([3, 1, 1, 3])
col_one.text("To show sample data click")

if col_two.button("Yes"):
    table_data()

if col_three.button("Hide"):
    st.text("")

if col_four.download_button(label="Download", data=csv_data, file_name="data.csv", mime="text/csv"):
    st.toast("file downloaded.")

st.subheader("Taking input from dialogue box", divider="green")


@st.dialog("Please provide more details")
def voting_popup(like):
    """
    :param like: st.session_state
    """
    if like:
        st.write("thank for liking")
    else:
        st.write("please put your comments")
    feedback = st.text_area("comments")

    if st.button("Save"):
        st.session_state.vote = {"like": like, "feedback": feedback}
        st.rerun()


if "vote" not in st.session_state:
    st.write("Do you like streamlit app")
    if st.button("simple structure essay to work"):
        voting_popup(True)
    if st.button("I dont like its very difficult"):
        voting_popup(False)
else:
    if not st.session_state.vote["like"]:
        st.write(f"sorry for the in inconvenience we will improve based this comment")
        st.write(st.session_state.vote["feedback"])
    else:
        st.write("Thank your support")
    if st.button("Try Again"):
        st.session_state.pop("vote")
        st.rerun()

st.subheader("Taking input from multi selection", divider="blue")


def selection_alert():
    """
    none
    """
    selection_items = st.session_state.selected_items
    st.toast(f"total selection {len(selection_items)}")


options = ["india", "pakistan", "england", "new york" "america"]
selection = st.multiselect("Select your future country", options=options, )

selection_pill = st.pills("Select your future country", options=options,
                          on_change=selection_alert, key="selected_items", selection_mode="multi")
# print(selection_pill)
# st.markdown(f"selected items {selection_pill}")

st.subheader("Taking input from radio button", divider="orange")
genre = st.radio(
    "What's your favorite movie genre",
    ["Comedy", "Drama", "Documentary"],
    captions=[
        "Laugh out loud.",
        "Get the popcorn with emotional.",
        "Never stop learning like some reality.",
    ],
    index=1

)

st.write(f"Nice choice {genre}")

st.subheader("Dataframe editing")
names = ['Alice', 'Bob', 'Charlie', 'David']
cities = ['New York', 'Los Angeles', 'Chicago', 'Houston']
data = {
    'Name': names,
    'Age': [25, 30, 35, 40],
    'City': cities
}
data_df = pd.DataFrame(data)

column_config = {
    "Age": st.column_config.NumberColumn("Age", help="Enter the age"),
    "City": st.column_config.SelectboxColumn("City", options=cities, help="Select city", default=cities[1])
}
edited_df = st.data_editor(data_df, hide_index=True, )

