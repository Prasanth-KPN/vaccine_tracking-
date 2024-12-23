#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import streamlit as st

# Initialize the DataFrame
columns = ["Patient Name", "Age", "Vaccine Name", "Dose Number", "Date Administered", "Location"]
if "vaccination_data" not in st.session_state:
    st.session_state.vaccination_data = pd.DataFrame(columns=columns)

# Title
st.title("Vaccination Tracking System")

# Sidebar menu
menu = st.sidebar.radio("Menu", ["Add Record", "View Records", "Update Record", "Delete Record"])

if menu == "Add Record":
    st.header("Add a New Patient Vaccination Record")
    with st.form("add_form"):
        patient_name = st.text_input("Patient Name")
        age = st.number_input("Age", min_value=0, step=1)
        vaccine_name = st.text_input("Vaccine Name")
        dose_number = st.number_input("Dose Number", min_value=1, step=1)
        date_administered = st.date_input("Date Administered")
        location = st.text_input("Location")
        submit = st.form_submit_button("Add Record")
    
    if submit:
        new_record = {
            "Patient Name": patient_name,
            "Age": age,
            "Vaccine Name": vaccine_name,
            "Dose Number": dose_number,
            "Date Administered": date_administered.strftime("%Y-%m-%d"),
            "Location": location,
        }
        st.session_state.vaccination_data = pd.concat(
            [st.session_state.vaccination_data, pd.DataFrame([new_record])], ignore_index=True
        )
        st.success("Record added successfully!")

elif menu == "View Records":
    st.header("View Vaccination Records")
    if st.session_state.vaccination_data.empty:
        st.warning("No records found.")
    else:
        st.dataframe(st.session_state.vaccination_data)

elif menu == "Update Record":
    st.header("Update a Current Record")
    patient_name = st.text_input("Enter Patient Name to update record")
    record = st.session_state.vaccination_data[
        st.session_state.vaccination_data["Patient Name"] == patient_name
    ]

    if not record.empty:
        st.write("Current Record:")
        st.dataframe(record)

        column_to_update = st.selectbox("Select column to update", st.session_state.vaccination_data.columns)
        new_value = st.text_input(f"Enter new value for {column_to_update}")
        if st.button("Update Record"):
            st.session_state.vaccination_data.loc[
                st.session_state.vaccination_data["Patient Name"] == patient_name, column_to_update
            ] = new_value
            st.success("Record updated successfully!")
    else:
        st.warning("Record not found.")

elif menu == "Delete Record":
    st.header("Delete a Existing Record")
    patient_name = st.text_input("Enter Patient Name to delete record")
    if st.button("Delete Record"):
        if patient_name in st.session_state.vaccination_data["Patient Name"].values:
            st.session_state.vaccination_data = st.session_state.vaccination_data[
                st.session_state.vaccination_data["Patient Name"] != patient_name
            ]
            st.success("Record deleted successfully!")
        else:
            st.warning("Record not found.")

