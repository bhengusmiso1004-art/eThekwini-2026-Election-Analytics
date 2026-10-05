
import streamlit as st
import pandas as pd
import pickle

st.set_page_config(
    page_title="eThekwini 2026 Election Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("eThekwini 2026 Local Government Election Analytics")
st.write(
    "Machine-learning analysis and projections for "
    "eThekwini Metropolitan Municipality."
)

st.info(
    "2026 values displayed in this dashboard are model-generated "
    "projections, not official election results."
)

# Load saved model information
with open("ethekwini_2026_model_info.pkl", "rb") as file:
    model_info = pickle.load(file)

# Load prediction results
metro_predictions = pd.read_csv(
    "ethekwini_2026_metro_predictions.csv"
)

ward_predictions = pd.read_csv(
    "ethekwini_2026_ward_predictions.csv"
)

ward_leaders = pd.read_csv(
    "ethekwini_2026_ward_leaders.csv"
)

st.success("Prediction data loaded successfully.")

st.divider()

st.header("2026 Metro Party Projection")

st.write(
    "The model estimates the Ward-ballot vote share for four "
    "major parties in eThekwini."
)

# Display projected leading party
leading_party = metro_predictions.iloc[0]

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Projected Leading Party",
        leading_party["PartyName"]
    )

with col2:
    st.metric(
        "Projected Vote Share",
        f'{leading_party["PredictedVoteShare2026"]:.2f}%'
    )

# Display prediction table
display_metro = metro_predictions.copy()

display_metro["PredictedVoteShare2026"] = (
    display_metro["PredictedVoteShare2026"].round(2)
)

display_metro = display_metro.rename(
    columns={
        "PartyName": "Party",
        "PredictedVoteShare2026": "Projected Vote Share (%)"
    }
)

st.subheader("Projected Party Vote Shares")

st.dataframe(
    display_metro,
    use_container_width=True,
    hide_index=True
)

# Bar chart
chart_data = metro_predictions.set_index(
    "PartyName"
)["PredictedVoteShare2026"]

st.bar_chart(chart_data)

st.caption(
    "These are model-generated Ward-ballot projections. "
    "They are not official 2026 election results and the four "
    "party shares are not normalised to 100%."
)

st.divider()

st.header("Selected Ward Predictions")

st.write(
    "Select one of the three competitive wards analysed "
    "in the forecasting model."
)

selected_ward = st.selectbox(
    "Choose a ward:",
    sorted(ward_predictions["Ward"].unique())
)

selected_data = ward_predictions[
    ward_predictions["Ward"] == selected_ward
].sort_values(
    "PredictedVoteShare2026",
    ascending=False
)

leader = selected_data.iloc[0]
runner_up = selected_data.iloc[1]

margin = (
    leader["PredictedVoteShare2026"]
    - runner_up["PredictedVoteShare2026"]
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Projected Leader",
        leader["PartyName"]
    )

with col2:
    st.metric(
        "Projected Share",
        f'{leader["PredictedVoteShare2026"]:.2f}%'
    )

with col3:
    st.metric(
        "Lead Margin",
        f"{margin:.2f} percentage points"
    )

# Ward prediction table
ward_display = selected_data[
    ["PartyName", "PredictedVoteShare2026"]
].copy()

ward_display["PredictedVoteShare2026"] = (
    ward_display["PredictedVoteShare2026"].round(2)
)

ward_display = ward_display.rename(
    columns={
        "PartyName": "Party",
        "PredictedVoteShare2026": "Projected Vote Share (%)"
    }
)

st.dataframe(
    ward_display,
    use_container_width=True,
    hide_index=True
)

# Ward chart
ward_chart = selected_data.set_index(
    "PartyName"
)["PredictedVoteShare2026"]

st.bar_chart(ward_chart)

st.warning(
    "Ward projections should be interpreted with caution. "
    "Small differences between the leading parties are not "
    "evidence of a certain election outcome."
)

st.divider()

st.header("Model Performance")

st.write(
    "Four regression algorithms were evaluated using a "
    "time-based validation approach. The model was trained "
    "on earlier election transitions and evaluated on the "
    "unseen 2021 election."
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "R² Score",
        f'{model_info["Validation_R2"]:.4f}'
    )

with col2:
    st.metric(
        "MAE",
        f'{model_info["Validation_MAE"]:.2f} pp'
    )

with col3:
    st.metric(
        "RMSE",
        f'{model_info["Validation_RMSE"]:.2f} pp'
    )

st.write(
    "**Selected model:** Linear Regression"
)

st.caption(
    "R² measures how much variation in vote share is explained "
    "by the model. MAE and RMSE measure prediction error in "
    "percentage points."
)

st.subheader("2026 Turnout Assessment")

st.write(
    "A separate modelling process was tested for voter turnout. "
    "However, the turnout models did not generalise successfully "
    "to the unseen 2021 election."
)

st.error(
    "No reliable 2026 turnout prediction is reported. "
    "The best tested turnout model had an R² of -2.7630 "
    "and an MAE of approximately 17.4 percentage points."
)

st.write(
    "Because a negative R² indicates performance worse than a "
    "simple mean-based prediction, the available historical "
    "variables were considered insufficient for a defensible "
    "2026 turnout forecast."
)

st.divider()

st.header("Historical Turnout")

turnout_history = pd.DataFrame({
    "Election Year": [2011, 2016, 2021],
    "Estimated Turnout (%)": [59.06, 59.30, 41.36]
})

st.line_chart(
    turnout_history.set_index("Election Year")
)

st.caption(
    "Historical turnout values are derived estimates from "
    "Ward-ballot data and should not be interpreted as official "
    "IEC turnout statistics."
)

st.divider()

st.header("Methodology and Limitations")

st.markdown("""
### Methodology

Historical eThekwini local-government election data from 2011, 2016
and 2021 was used.

The party forecasting model uses previous-election:

- vote share
- party votes
- registered voters

A time-based validation approach was used rather than a random
train-test split. Earlier election transitions were used for training
and the 2021 election was used as unseen test data.

### Important Limitations

The 2026 figures are statistical model projections and are **not
official election results**.

Only four major parties are included in the current forecasting model:
ANC, DA, EFF and IFP. Other parties and independent candidates are
therefore not represented in these projections.

Ward and voting-district geography can change between elections.
Historical comparisons were restricted where possible to geographically
comparable units, but geographic change remains a limitation.

The model predicts Ward-ballot vote share. It does not directly predict
municipal council seats or determine which party or coalition will
govern eThekwini.

A reliable 2026 turnout prediction could not be produced from the
available variables because the tested turnout models failed
time-based validation.
""")

st.divider()

st.caption(
    "eThekwini 2026 Local Government Election Analytics | "
    "Educational forecasting project"
)
