import streamlit as st
import pandas as pd
import joblib
import os
import json

st.title("Prediksi MDT PM14")

# Select Grade
grade = st.selectbox(
    "Pilih Grade Tissue",
    ["Facial", "Toilet"]
)

# Base Directory
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# State File
state_dir = os.path.join(BASE_DIR, "state")
os.makedirs(state_dir, exist_ok=True)
state_file = os.path.join(
    state_dir,
    f"PM14_{grade}_input_state.json"
)

# Load Save Input State
saved_state = {}
if os.path.exists(state_file):
    with open(state_file, "r") as f:
        saved_state = json.load(f)

# Load Model & Features
model_path = os.path.join(BASE_DIR,"models","PM14",grade,"model.pkl")
features_path = os.path.join(BASE_DIR,"models","PM14",grade,"features.pkl")
model = joblib.load(model_path)
features = joblib.load(features_path)
#st.write("Features Path:", features_path)
#st.write("Loaded Features:", features)

# Feature Configuration
feature_config = {    
    'Mean_Yankee Pressure': {'min': 162.0,'max': 257.0, 'hard_max': 300, 'default': 0.0,'step': 1,'format': "%.2f"},
    'Mean_Load KWH Refiner': {'min': 5.5,'max': 7.4, 'hard_max': 10, 'default': 0.0,'step': 0.1,'format': "%.2f"},
    '% NBKP': {'min': 0.0,'max': 100.0, 'hard_max': 100, 'default': 0.0,'step': 1,'format': "%.2f"},
    'Mean_Load KWH Tickling Refiner': {'min': 0.0,'max': 400.0,'default': 0.0,'step': 1,'format': "%.2f"},
    'Mean_Creping': {'min': 0.0,'max': 40.0, 'hard_max': 100,'default': 0.0,'step': 1,'format': "%.2f"},
    'Mean_Jet Wire Ratio': {'min': 0.0,'max': 1.0,'default': 0.0,'step': 0.01,'format': "%.2f"},
    'GSM': {'min': 0.0,'max': 40.0,'default': 0.0,'step': 0.1,'format': "%.1f"},
    'Mean_Flow Coating': {'default': 0.0,'step': 1,'format': "%.2f"},
    'Mean_Flow Release': {'default': 1.0,'step': 1,'format': "%.2f"},
    'coating_release_ratio': {'min': 0.0,'max': 1.0},
    'pseudo_mass': {'min': 2.7,'max': 3.7, 'hard_max': 5, 'default': 0.0,'step': 0.1,'format': "%.2f"}
}

# Feature labels
feature_labels = {
    '% NBKP': 'NBKP (%)',
    'Mean_Load KWH Refiner':'Load KWH Refiner',
    'Mean_Creping': 'Creping',
    'Mean_Jet Wire Ratio':'Jet Wire Ratio',
    'Mean_Flow Coating':'Flow Coating',
    'Mean_Flow Release':'Flow Release',
    'Mean_Yankee Pressure': 'Yankee Pressure',
    'Mean_Stock Flow': 'Stock Flow',
    'Mean_Stock Consistency': 'Stock Consistency',
    'Mean_Yankee Speed': 'Yankee Speed',
}

# Feature default
for feature in feature_config:
    if feature not in st.session_state:
        st.session_state[feature] = saved_state.get(
            feature,
            feature_config[feature]['default']
            if 'default' in feature_config[feature]
            else 0.0
        )

# INPUT DATA
st.subheader("Masukkan Nilai Parameter")
input_data = {}

for feature in features:
    if feature in [
        "coating_release_ratio",
        "pseudo_mass",
        "Mean_Flow Coating",
        "Mean_Flow Release",
        "Mean_Stock Flow",
        "Mean_Stock Consistency",
        "Mean_Yankee Speed"
    ]:
        continue
    
    config = feature_config.get(feature)
    if config is None:
        st.error(f"Feature '{feature}' belum memiliki konfigurasi di feature_config")
        st.stop()

    input_data[feature] = st.number_input(
        label=feature_labels.get(feature,feature),
    
        min_value=0.0,
        
        max_value=(float(config['hard_max'])
        if 'hard_max' in config
        else None),
        
        step=float(config['step']),
        
        value=min(
        float(st.session_state.get(feature,config['default'])),
        float(config['hard_max'])
        if 'hard_max' in config
        else float(st.session_state.get(feature,config['default']))       
        ),
        
        format=config['format'],
        
        help=(
            f"Data histori training: "
            f"{config['min']} - {config['max']}"
            if 'min' in config
            else None),

        key=feature
    )

    if 'min' in config:
        if (
            input_data[feature] < config['min']
            or
            input_data[feature] > config['max']
        ):
            st.warning(
                f"⚠️ Nilai untuk "
                f"'{feature_labels.get(feature, feature)}' "
                f"berada di luar data histori "
                f"pelatihan model "
                f"({config['min']} - {config['max']}). "
                f"Hal ini dapat menurunkan "
                f"akurasi prediksi."
            )

st.markdown("### Flow Parameters")

coating_value = st.number_input(
    feature_labels['Mean_Flow Coating'],
    min_value=0.0,
    step=1.0,
    value=float(
        st.session_state.get(
            "Mean_Flow Coating",
            0.0
        )
    ),
    format="%.2f",
    key="Mean_Flow Coating"
)

release_value = st.number_input(
    feature_labels['Mean_Flow Release'],
    min_value=0.1,
    step=1.0,
    value=float(
        st.session_state.get(
            "Mean_Flow Release",
            1.0
        )
    ),
    format="%.2f",
    key="Mean_Flow Release"
)

coating_release_ratio = (coating_value / release_value)

st.info(
    f"Coating Release Ratio: "
    f"{coating_release_ratio:.3f}"
)

ratio_config = feature_config[
    'coating_release_ratio'
]

if (
    coating_release_ratio < ratio_config['min']
    or
    coating_release_ratio > ratio_config['max']
):

    st.warning(
        f"⚠️ Hasil pembagian "
        f"'Flow Coating' / "
        f"'Flow Release' berada di luar "
        f"data histori pelatihan model "
        f"({ratio_config['min']} - {ratio_config['max']}). "
        f"Hal ini dapat menurunkan "
        f"akurasi prediksi."
    )

st.markdown("### Stock Parameters")

stock_flow_value = st.number_input(
    feature_labels['Mean_Stock Flow'],
    min_value=0.0,
    step=1.0,
    value=float(st.session_state.get("Mean_Stock Flow", 0.0)),
    format="%.2f",
    key="Mean_Stock Flow"
)

stock_consistency_value = st.number_input(
    feature_labels['Mean_Stock Consistency'],
    min_value=0.0,
    step=0.01,
    value=float(st.session_state.get("Mean_Stock Consistency", 0.0)),
    format="%.2f",
    key="Mean_Stock Consistency"
)

yankee_speed_value = st.number_input(
    feature_labels['Mean_Yankee Speed'],
    min_value=0.1,
    step=1.0,
    value=float(st.session_state.get("Mean_Yankee Speed", 1.0)),
    format="%.2f",
    key="Mean_Yankee Speed"
)

pseudo_mass = (
    stock_flow_value *
    stock_consistency_value
) / yankee_speed_value

st.info(f"Pseudo Mass: {pseudo_mass:.3f}")

pseudo_mass_config = feature_config['pseudo_mass']

if (
    pseudo_mass < pseudo_mass_config['min']
    or
    pseudo_mass > pseudo_mass_config['max']
):
    st.warning(
        f"⚠️ Hasil perhitungan "
        f"'Stock Flow × Stock Consistency / Yankee Speed' "
        f"berada di luar data histori pelatihan model "
        f"({pseudo_mass_config['min']} - {pseudo_mass_config['max']}). "
        f"Hal ini dapat menurunkan akurasi prediksi."
    )

# Save Input State
with open(state_file, "w") as f:
    json.dump({**input_data,
               "Mean_Flow Coating": coating_value,
               "Mean_Flow Release": release_value},
               f)

# Button Section
col1, col2 = st.columns(2)
with col1:
    predict_button = st.button("Predict",key="predict_button_pm14")
with col2:
    reset_button = st.button("Hapus Semua",key="reset_button_pm14")
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
    df['coating_release_ratio'] = coating_release_ratio
    df['pseudo_mass'] = pseudo_mass
    prediction_ratio = model.predict(df)[0]
    #gsm = df['GSM'].values[0]
    #prediction_mdt = prediction_ratio * gsm
    st.success(f"Hasil Prediksi MDT PM14 "f"({grade}): "f"{prediction_ratio:.2f}")