import streamlit as st
import pandas as pd
import pickle

# =====================================================
# PAGE CONFIGURATION
# =====================================================
st.set_page_config(
    page_title="eThekwini 2026 Election Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# LOAD PROJECT DATA
# =====================================================
@st.cache_data
def load_csv(filename):
    return pd.read_csv(filename)


@st.cache_resource
def load_pickle(filename):
    with open(filename, "rb") as file:
        return pickle.load(file)


try:
    metro_predictions = load_csv(
        "ethekwini_2026_metro_predictions.csv"
    )

    ward_predictions = load_csv(
        "ethekwini_2026_ward_predictions.csv"
    )

    ward_leaders = load_csv(
        "ethekwini_2026_ward_leaders.csv"
    )

    model_info = load_pickle(
        "ethekwini_2026_model_info.pkl"
    )

except Exception as error:
    st.error(f"Unable to load project data: {error}")
    st.stop()


# =====================================================
# SIDEBAR NAVIGATION
# =====================================================
st.sidebar.title("📊 Election Analytics")

st.sidebar.write(
    "eThekwini Metropolitan Municipality"
)

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "🗳️ Metro Prediction",
        "📍 Ward Predictions",
        "📈 Historical Analysis",
        "🤖 Model Performance",
        "📚 Methodology"
    ]
)

st.sidebar.divider()

st.sidebar.info(
    "2026 values are machine-learning projections "
    "and are not official election results."
)


# =====================================================
# MAIN HEADER
# =====================================================
st.title("eThekwini 2026 Election Analytics")

st.caption(
    "Machine-Learning Decision Support System | "
    "eThekwini Metropolitan Municipality"
)

st.divider()
# =====================================================
# DASHBOARD PAGE
# =====================================================
if page == "🏠 Dashboard":

    st.header("2026 Election Forecast Dashboard")

    st.write(
        "Overview of the machine-learning projections for "
        "eThekwini Metropolitan Municipality."
    )

    st.warning(
        "These are model-generated projections for the 2026 election. "
        "They are not official IEC election results."
    )

    # Find projected leading metro party
    metro_sorted = metro_predictions.sort_values(
        by="PredictedVoteShare2026",
        ascending=False
    )

    leading_party = metro_sorted.iloc[0]["PartyName"]
    leading_share = metro_sorted.iloc[0]["PredictedVoteShare2026"]

    # Summary cards
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Projected Metro Leader",
            leading_party
        )

    with col2:
        st.metric(
            "Projected Vote Share",
            f"{leading_share:.2f}%"
        )

    with col3:
        st.metric(
            "Selected Wards Analysed",
            ward_leaders["Ward"].nunique()
        )

    st.divider()

    # Metro overview chart
    st.subheader("Metro Party Projection")

    chart_data = metro_sorted.set_index(
        "PartyName"
    )["PredictedVoteShare2026"]

    st.bar_chart(chart_data)

    st.caption(
        "Projected Ward-ballot vote shares for the four "
        "historically modelled parties. Shares are not normalised "
        "to 100% because other parties and independents are not "
        "included in this model."
    )

    st.divider()

    # Selected ward leaders
    st.subheader("Selected Ward Forecasts")

    st.dataframe(
        ward_leaders,
        use_container_width=True,
        hide_index=True
    )

    st.info(
        "Ward leads should be interpreted cautiously. "
        "The model's validation MAE is approximately 7.27 "
        "percentage points, so small projected margins are uncertain."
    )

    # =====================================================
# METRO PREDICTION PAGE
# =====================================================
elif page == "🗳️ Metro Prediction":

    st.header("2026 Metro Party Projection")

    st.write(
        "This section presents the model-generated Ward-ballot "
        "vote-share projections for the four historically modelled "
        "parties in eThekwini."
    )

    metro_sorted = metro_predictions.sort_values(
        by="PredictedVoteShare2026",
        ascending=False
    )

    leading_party = metro_sorted.iloc[0]["PartyName"]
    leading_share = metro_sorted.iloc[0]["PredictedVoteShare2026"]

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Projected Leading Party",
            leading_party
        )

    with col2:
        st.metric(
            "Projected Vote Share",
            f"{leading_share:.2f}%"
        )

    st.subheader("Projected Party Vote Shares")

    st.bar_chart(
        metro_sorted.set_index(
            "PartyName"
        )["PredictedVoteShare2026"]
    )

    st.subheader("Projection Table")

    display_metro = metro_sorted.copy()

    display_metro["PredictedVoteShare2026"] = (
        display_metro["PredictedVoteShare2026"].round(2)
    )

    st.dataframe(
        display_metro,
        use_container_width=True,
        hide_index=True
    )

    st.warning(
        "These percentages are model outputs, not official results. "
        "The four modelled parties are not the complete election field, "
        "so their projected shares are not normalised to total 100%."
    )

    st.info(
        "A projected party share below 50% must not automatically be "
        "interpreted as requiring a governing coalition. Council control "
        "depends on official results, seat allocation and the full "
        "municipal election outcome."
    )

    # =====================================================
# WARD PREDICTIONS PAGE
# =====================================================
elif page == "📍 Ward Predictions":

    st.header("2026 Selected Ward Predictions")

    st.write(
        "Explore the model-generated party vote-share projections "
        "for the three selected eThekwini wards."
    )

    # Select a ward
    selected_ward = st.selectbox(
        "Select a Ward",
        sorted(ward_predictions["Ward"].unique())
    )

    # Filter prediction data
    selected_data = ward_predictions[
        ward_predictions["Ward"] == selected_ward
    ].copy()

    selected_data = selected_data.sort_values(
        by="PredictedVoteShare2026",
        ascending=False
    )

    # Get leader and runner-up
    leader = selected_data.iloc[0]
    runner_up = selected_data.iloc[1]

    margin = (
        leader["PredictedVoteShare2026"]
        - runner_up["PredictedVoteShare2026"]
    )

    # Summary cards
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
            f"{margin:.2f} pp"
        )

    st.divider()

    # Ward chart
    st.subheader(f"Party Projection — Ward {selected_ward}")

    st.bar_chart(
        selected_data.set_index(
            "PartyName"
        )["PredictedVoteShare2026"]
    )

    # Projection table
    st.subheader("Ward Projection Table")

    display_ward = selected_data.copy()

    display_ward["PredictedVoteShare2026"] = (
        display_ward["PredictedVoteShare2026"].round(2)
    )

    st.dataframe(
        display_ward,
        use_container_width=True,
        hide_index=True
    )

    # Uncertainty warning
    if margin < 7.27:
        st.warning(
            "This projected lead is smaller than the model's "
            "validation MAE of approximately 7.27 percentage points. "
            "The projected ordering should therefore be treated as uncertain."
        )
    else:
        st.info(
            "The projected margin is larger than the model's validation "
            "MAE, but the result remains a model-generated forecast "
            "rather than an official election outcome."
        )

    st.caption(
        "The selected wards were chosen to represent competitive "
        "electoral contests with different patterns of party competition."
    )

    # =====================================================
# HISTORICAL ANALYSIS PAGE
# =====================================================
elif page == "📈 Historical Analysis":

    st.header("Historical Election Analysis")

    st.write(
        "Historical Ward-ballot trends provide context for the "
        "2026 machine-learning projections."
    )

    st.subheader("Historical Estimated Turnout")

    turnout_history = pd.DataFrame({
        "Election Year": [2011, 2016, 2021],
        "Estimated Turnout (%)": [59.06, 59.30, 41.36]
    })

    st.line_chart(
        turnout_history.set_index("Election Year")
    )

    st.dataframe(
        turnout_history,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "These turnout values were derived from the historical "
        "common-geography Ward-ballot dataset using registered voters "
        "and estimated ballots cast."
    )

    st.divider()

    st.subheader("Historical Major-Party Vote Share")

    historical_share = pd.DataFrame({
        "Election Year": [
            2011, 2011, 2011,
            2016, 2016, 2016, 2016,
            2021, 2021, 2021, 2021
        ],
        "Party": [
            "ANC", "DA", "IFP",
            "ANC", "DA", "EFF", "IFP",
            "ANC", "DA", "EFF", "IFP"
        ],
        "Vote Share (%)": [
            60.11, 20.21, 4.30,
            52.30, 27.08, 3.22, 4.05,
            41.24, 26.26, 10.15, 6.65
        ]
    })

    historical_pivot = historical_share.pivot(
        index="Election Year",
        columns="Party",
        values="Vote Share (%)"
    )

    st.line_chart(historical_pivot)

    st.caption(
        "Historical shares shown here use the 103 wards whose ward "
        "identifiers were common across the 2011, 2016 and 2021 datasets. "
        "EFF is absent from 2011 because it did not contest that election."
    )

    st.warning(
        "Matching ward identifiers across election years does not prove "
        "that ward geography remained identical. Boundary and voting-"
        "district changes are therefore an important limitation."
    )

    # =====================================================
# MODEL PERFORMANCE PAGE
# =====================================================
elif page == "🤖 Model Performance":

    st.header("Machine-Learning Model Performance")

    st.write(
        "Multiple regression models were evaluated using a "
        "time-based validation strategy. Earlier election data "
        "was used to predict a later election rather than randomly "
        "splitting observations."
    )

    st.subheader("Selected Model")

    st.success("Linear Regression")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Validation R²", "0.8165")

    with col2:
        st.metric("Validation MAE", "7.27 pp")

    with col3:
        st.metric("Validation RMSE", "10.99 pp")

    st.write(
        "Linear Regression produced the strongest validation "
        "performance among the tested models."
    )

    st.divider()

    st.subheader("Model Comparison")

    model_results = pd.DataFrame({
        "Model": [
            "Linear Regression",
            "Decision Tree",
            "Random Forest",
            "Gradient Boosting"
        ],
        "MAE": [
            7.2654,
            9.6572,
            8.0151,
            7.8652
        ],
        "RMSE": [
            10.9943,
            15.3419,
            12.5402,
            12.1807
        ],
        "R²": [
            0.8165,
            0.6427,
            0.7612,
            0.7747
        ]
    })

    st.dataframe(
        model_results,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("Turnout Model Assessment")

    st.error(
        "No reliable 2026 turnout forecast was produced."
    )

    st.write(
        "The turnout models failed time-based validation. "
        "The best turnout model achieved an R² of approximately "
        "-2.7630 with an MAE of approximately 17.4 percentage points."
    )

    st.info(
        "A negative R² indicates that the tested turnout model "
        "performed worse than a simple mean-based prediction. "
        "For this reason, an unsupported 2026 turnout value was "
        "not reported."
    )

    st.caption(
        "This follows the project's evidence-based approach: "
        "insufficient predictive performance is reported rather "
        "than presenting an unreliable forecast as fact."
    )

    # =====================================================
# METHODOLOGY PAGE
# =====================================================
elif page == "📚 Methodology":

    st.header("Methodology and Project Limitations")

    st.subheader("Project Objective")

    st.write(
        "The purpose of this project is to use historical local-government "
        "election data to develop machine-learning projections for the "
        "2026 Local Government Election in eThekwini Metropolitan Municipality."
    )

    st.subheader("Historical Data")

    st.write(
        "Historical Ward-ballot election data from 2011, 2016 and 2021 "
        "was used. The analysis focused on comparable eThekwini wards "
        "and voting districts across election years."
    )

    st.subheader("Parties Modelled")

    st.write(
        "The forecasting model focuses on ANC, DA, EFF and IFP. "
        "These parties had sufficient historical information for the "
        "modelling approach used. EFF has no 2011 observation because "
        "the party did not contest that election."
    )

    st.subheader("Machine-Learning Approach")

    st.write(
        "The target variable is party vote share. Historical party vote "
        "share, party votes and registered voters from the previous "
        "election were used as predictive variables."
    )

    st.write(
        "Linear Regression, Decision Tree, Random Forest and Gradient "
        "Boosting models were evaluated. Linear Regression was selected "
        "because it achieved the strongest time-based validation performance."
    )

    st.subheader("Validation Strategy")

    st.write(
        "A time-based validation strategy was used instead of a random "
        "train-test split. Historical election transitions were used to "
        "evaluate how well the models could predict a later election."
    )

    st.subheader("Selected Wards")

    st.write(
        "Wards 59500009, 59500026 and 59500099 were selected because "
        "they represented competitive contests and different patterns "
        "of party competition in the 2021 election."
    )

    st.subheader("Important Limitations")

    st.markdown(
        """
        - 2026 values are **model-generated predictions**, not official results.
        - Ward and voting-district boundaries may change between elections.
        - Matching geographic identifiers does not guarantee identical boundaries.
        - The metro forecast shown in this application is based on **Ward-ballot data**.
        - Only four historically modelled parties are included in the main forecast.
        - The four projected party shares are **not normalised to 100%**.
        - A reliable 2026 turnout forecast could not be produced from the available variables.
        - Projected ward leads with small margins should be treated cautiously.
        - Vote-share projections alone cannot determine which party will govern the municipality.
        """
    )

    st.subheader("Interpretation")

    st.info(
        "Historical observations, derived analytical measures and 2026 "
        "predictions should be treated as separate types of information. "
        "The dashboard is an analytical decision-support tool and not an "
        "official election-results system."
    )