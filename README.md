# Weekly Forecasting Application
This repository contains a complete implementation of a Weekly Forecasting Application. The project is built using FastAPI for the backend and Streamlit for the frontend, designed to predict future weekly values using historical data and a machine learning model.

## Prototyping highlights
- Implemented time series cross-validation and robust feature engineering techniques.
- Assessed stationarity and feature importance for each time series.
- Trained both individual and global models, balancing predictive accuracy and scalability.
### Outputs
- Feature importance metrics for individual time series.
- MAPE scores for individual and global models.
- Visualized decompositions, predictions, and feature trends.

## Deployment features
This application is deployed on Render at: https://m4-weekly-frontend.onrender.com/
- Frontend: Interactive Streamlit application for data input and visualization of predictions.
- Backend: FastAPI server that performs preprocessing and generates predictions using a pre-trained XGBoost model.
- Machine Learning: Uses XGBoost for forecasting and includes preprocessing pipelines for feature engineering.
- Deployment: Fully containerized using Docker and deployed on Render.

## How to Run Locally
1. Clone the Repository
```
git clone https://github.com/s-siddhant/timeseries-forecasting-m4-weekly.git
cd weekly-forecasting-app
```
2. Backend Setup
```
cd backend
docker build -t weekly-backend .
docker run -d -p 8000:8000 weekly-backend
```
  The FastAPI backend will be available at http://localhost:8000.
  
3. Frontend Setup
```
cd ../frontend
docker build -t weekly-frontend .
docker run -d -p 8501:8501 weekly-frontend
```

## API Documentation
1. Helthcheck:
   - URL: /healthcheck
   - Method: GET
   - Response: { "status": "API is up and running" }
2. Predictions:
   - URL: /predict
   - Method: POST
   - Request Body
     ```
     {
     "start_date": "YYYY-MM-DD",
     "target_values": [10.0, 15.0, 20.0]
     }
     ```
   - Response
     ```
     {
       "predictions": [
       { "date": "YYYY-MM-DD", "prediction": 25.0 },
       ...
       ]
     }
     ```

## Example Usage
1. Navigate to the frontend URL.
2. Input a start date and a list of historical target values.
3. Click "Get Predictions" to view the forecast for the next 5 weeks.
4. Visualize predictions in the displayed chart.

## Technologies Used
- Frontend: Streamlit
- Backend: FastAPI
- Machine Learning: XGBoost
- Feature Engineering: Lagged and rolling features, temporal features
- Deployment: Docker, Render

## License
This project is licensed under the MIT License.
Feel free to contribute by submitting issues or pull requests. 😊
