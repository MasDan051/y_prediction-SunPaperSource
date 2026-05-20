import streamlit as st
import pandas as pd
import joblib
import os
import json

st.title("Prediksi MDS PM15")

# Base Directory
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# State File
state_dir = os.path.join(BASE_DIR, "state")
os.makedirs(state_dir, exist_ok=True)

state_file = os.path.join(
    state_dir,
    "PM15_MDS_input_state.json"
)

# Load Save Input State
saved_state = {}

if os.path.exists(state_file):
    with open(state_file, "r") as f:
        saved_state = json.load(f)

# Load Model & Features
model_path = os.path.join(
    BASE_DIR,
    "models",
    "PM15",
    "MDS",
    "model.pkl"
)

features_path = os.path.join(
    BASE_DIR,
    "models",
    "PM15",
    "MDS",
    "features.pkl"
)

model = joblib.load(model_path)
features = joblib.load(features_path)

# Feature Configuration
feature_config = {
    'Mean_Creping': {
        'min': 0.0,
        'max': 40.0,
        'default': 0.0,
        'step': 0.1,
        'format': "%.2f"
    }
}

# Feature Labels
feature_labels = {
    'Mean_Creping': 'Creping'
}

# Default Session State
for feature in feature_config:

    if feature not in st.session_state:

        st.session_state[feature] = saved_state.get(
            feature,
            feature_config[feature]['default']
        )

# INPUT SECTION
st.subheader("Masukkan Nilai Parameter")

input_data = {}

for feature in features:

    config = feature_config[feature]

    input_data[feature] = st.number_input(
        label=feature_labels.get(feature, feature),

        min_value=0.0,

        step=float(config['step']),

        value=float(
            st.session_state.get(
                feature,
                config['default']
            )
        ),

        format=config['format'],

        help=(
            f"Data histori training: "
            f"{config['min']} - {config['max']}"
        ),

        key=feature
    )

    # Warning outlier
    if (
        input_data[feature] < config['min']
        or
        input_data[feature] > config['max']
    ):

        st.warning(
            f"⚠️ Nilai '{feature_labels.get(feature, feature)}' "
            f"berada di luar data histori pelatihan model "
            f"({config['min']} - {config['max']}). "
            f"Hal ini dapat menurunkan akurasi prediksi."
        )

# Save Input State
with open(state_file, "w") as f:
    json.dump(input_data, f)

# BUTTON SECTION
col1, col2 = st.columns(2)

with col1:
    predict_button = st.button(
        "Predict",
        key="predict_button_pm15_mds"
    )

with col2:
    reset_button = st.button(
        "Hapus Semua",
        key="reset_button_pm15_mds"
    )

# Reset Button
if reset_button:

    for feature in feature_config:

        if feature in st.session_state:
            del st.session_state[feature]

    if os.path.exists(state_file):
        os.remove(state_file)

    st.rerun()

# Prediction
if predict_button:

    df = pd.DataFrame([input_data])

    prediction = model.predict(df)[0]

    st.success(
        f"Hasil Prediksi MDS PM15: {prediction:.2f}"
    )