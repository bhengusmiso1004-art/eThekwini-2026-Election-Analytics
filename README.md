# eThekwini 2026 Election Analytics

Machine-learning election analytics project for the eThekwini Metropolitan Municipality using historical South African Local Government Election data.

## Live Streamlit Application

https://ethekwini-2026-election-analytics-sbonelos.streamlit.app/

## Data Sources

Historical election data was obtained from the Electoral Commission of South Africa (IEC).

IEC Downloadable Municipal Election Results:
https://results.elections.org.za/home/Downloads/ME-Results

Historical election years used:
- 2011 Local Government Elections
- 2016 Local Government Elections
- 2021 Local Government Elections

Municipality:
- eThekwini Metropolitan Municipality, KwaZulu-Natal

The analysis primarily uses historical Ward-ballot election results downloaded from the official IEC results portal.

## Model

Four machine-learning algorithms were evaluated:
- Linear Regression
- Decision Tree
- Random Forest
- Gradient Boosting

Linear Regression was selected based on time-based validation.

Final validation performance:
- R²: 0.8162
- MAE: 7.3056 percentage points
- RMSE: 11.0389 percentage points

## Important Note

The 2026 values shown by this project are machine-learning projections and are not official IEC election results. Historical observations, derived estimates, and model predictions should not be interpreted as the same type of information.
