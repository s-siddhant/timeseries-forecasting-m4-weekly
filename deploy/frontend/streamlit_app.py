import streamlit as st
import requests
import pandas as pd

# Define the FastAPI endpoint
#API_URL = "http://127.0.0.1:8000"
#API_URL = "http://fastapi-backend:8000"

API_URL = "https://m4-weekly-backend.onrender.com" # Use your actual backend URL from Render

# Page title
st.title("Weekly Forecasting Application")

# Input fields
st.header("Input Data")
start_date = st.date_input("Start Date")
target_values = st.text_area(
    "Enter target values (comma-separated)",
    placeholder="e.g., 10, 15, 20, 25, 30",
)

# Submit button
if st.button("Get Predictions"):
    # Validate input
    if not start_date or not target_values:
        st.error("Please provide both start date and target values.")
    else:
        try:
            # Convert target values to a list of floats
            target_values_list = [float(x.strip()) for x in target_values.split(",")]

            # Prepare the payload
            payload = {
                "start_date": start_date.strftime("%Y-%m-%d"),
                "target_values": target_values_list,
            }

            # Send a POST request to the API
            response = requests.post(f"{API_URL}/predict", json=payload)

            # Check the response status
            if response.status_code == 200:
                # Display predictions
                predictions = response.json()["predictions"]
                st.success("Predictions for the next 5 weeks:")
                predictions_df = pd.DataFrame(predictions)
                st.dataframe(predictions_df)

                # Visualize predictions
                st.line_chart(
                    predictions_df.set_index("date")["prediction"]
                )
            else:
                st.error(
                    f"Error: {response.status_code} - {response.json().get('error', 'Unknown error')}"
                )
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
