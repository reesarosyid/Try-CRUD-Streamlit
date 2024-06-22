import streamlit as st
import pandas as pd
import os

# Path absolut ke file data.xlsx
file_path = os.path.join(os.path.dirname(__file__), 'data.xlsx')

# Load data from excel file
def load_data(file_path):
    try:
        df = pd.read_excel(file_path)
        st.write("Data loaded successfully")
        st.write("Columns:", ", ".join(df.columns.tolist()))
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# Save data to excel file
def save_data(df, file_path):
    try:
        df.to_excel(file_path, index=False)
        st.write("Data saved successfully")
    except Exception as e:
        st.error(f"Error saving data: {e}")

# Function to add a new record with automatic ID
def add_record(df, record):
    if df.empty:
        new_id = 1
    else:
        new_id = df['id'].max() + 1
    record['id'] = new_id
    return pd.concat([df, pd.DataFrame([record])], ignore_index=True)

# Function to update a record
def update_record(df, record, record_id):
    index = df[df['id'] == record_id].index
    if not index.empty:
        df.loc[index, :] = pd.DataFrame([record])
    return df

# Function to delete a record
def delete_record(df, record_id):
    return df[df['id'] != record_id]

# Main function
def main():
    st.title("CRUD Application with Streamlit and Pandas")

    # Load data
    df = load_data(file_path)
    
    
    # Sidebar for CRUD operations
    option = st.sidebar.selectbox("Operation", ["Create", "Read", "Update", "Delete"])
    
    if option == "Create":
        st.subheader("Add New Record")
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1)
        city = st.text_input("City")
        if st.button("Add"):
            new_record = {'name': name, 'age': age, 'city': city}
            df = add_record(df, new_record)
            save_data(df, file_path)
            st.success("Record added successfully")
    
    elif option == "Read":
        st.subheader("View Records")
        st.dataframe(df)
    
    elif option == "Update":
        st.subheader("Update Record")
        record_id = st.number_input("Enter ID of the record to update", min_value=1)
        if record_id in df['id'].values:
            name = st.text_input("Name", value=df.loc[df['id'] == record_id, 'name'].values[0])
            age = st.number_input("Age", min_value=1, value=int(df.loc[df['id'] == record_id, 'age'].values[0]))
            city = st.text_input("City", value=df.loc[df['id'] == record_id, 'city'].values[0])
            if st.button("Update"):
                updated_record = {'id': record_id, 'name': name, 'age': age, 'city': city}
                df = update_record(df, updated_record, record_id)
                save_data(df, file_path)
                st.success("Record updated successfully")
        else:
            st.error("Record not found")
    
    elif option == "Delete":
        st.subheader("Delete Record")
        record_id = st.number_input("Enter ID of the record to delete", min_value=1)
        if record_id in df['id'].values:
            if st.button("Delete"):
                df = delete_record(df, record_id)
                save_data(df, file_path)
                st.success("Record deleted successfully")
        else:
            st.error("Record not found")

if __name__ == "__main__":
    main()
