# air-quality-monitoring

Project Board:https://trello.com/b/n0v5yY6J/air-quality-analysis

Commit 1 : Data-preprocessinng part 
1. Checked missing values in both files
2. Dropped unwanted columns.
3. Found and visualized outliers.
4. Filled missing values based on outliers in both files.
5. Concatenated both files into one dataframe.

Commit 2: EDA_featureEngineering
1. Performed EDA and visualization to check co-relation, distibution, trends
2. feature Engineering: Added columns - AQI, AQI_Category, AQI_Numerical


Commit 3 : #ARIMA MODEL
1. I have started from building ARIMA model from an already done EDA part 
2. After Building it i have forcasted the results for the next 60 days
3. Repeated these steps for all the pollutants
4. calculated the metrics
5. Optimized the model for better results
6. Obtained optimized metric results
7. Compared original values and optimized values using bar chart
8. Visualised the forecasted data.
9. Interpretation from the obtained metrics

Commit 4: XGBoost
1.I have made the XGboost model and started after the EDA process done in the Arima model
2.Defining the features and targets.
3.Training and evaluating an XGBoost regression model for each target variable.
4.Storing and printing evaluation metrics.
5.Plotting the actual vs. predicted values for visual comparison


Commit 5: LSTM model
1. I have started building LSTM model after the ARIMA model
2. The dataset was preprocessed by handling missing values with linear interpolation and normalizing the features using MinMaxScaler.
3. Sequences of length 30 were created for time series modeling, and the data was split into training and test sets with an 80-20 ratio.
4. An initial LSTM model with 50 units and dropout layers was built and trained for 20 epochs, yielding moderate prediction accuracy.
5. To improve performance, a Bidirectional LSTM model with 64 units and early stopping was implemented and trained for 30 epochs.
6. The model's performance was evaluated using RMSE, MAE, and R² scores, and results were plotted to visualize training progress and prediction accuracy.
7. The tuned model showed improved performance, particularly for O3 and PM10, and all code, results, and visualizations are documented for further development and analysis.

Commit 6: Data_preprocessing_EDA_FE_V2
1. pre-processed the data by filling missing values by taking mean of upper 3 and lower 3 values.
2. Performed EDA and visualization to check co-relation, distibution, trends
3. feature Engineering: Added columns - AQI, AQI_Category, AQI_Numerical
