import streamlit as st
import pandas as pd
import joblib
import os
import json

st.title("Prediksi MDT PM16")

# Select Grade
grade = st.selectbox(
    "Pilih Grade Tissue",
    ["Facial", "Towel", "Toilet"]
)

# Base Directory
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# State File
state_dir = os.path.join(BASE_DIR, "state")
os.makedirs(state_dir, exist_ok=True)
state_file = os.path.join(
    state_dir,
    f"PM16_{grade}_input_state.json"
)

# Load Save Input State
saved_state = {}
if os.path.exists(state_file):
    with open(state_file, "r") as f:
        saved_state = json.load(f)

# Load Model & Features
model_path = os.path.join(BASE_DIR,"models","PM16",grade,"model.pkl")
features_path = os.path.join(BASE_DIR,"models","PM16",grade,"features.pkl")
model = joblib.load(model_path)
features = joblib.load(features_path)

# Import Dataframe
data_dir = os.path.join(BASE_DIR, "..", "Data Final")
pm16_toilet = pd.read_excel(os.path.join(data_dir, "Final_PM16-Toilet.xlsx"))
pm16_towel = pd.read_excel(os.path.join(data_dir, "Final_PM16-Towel.xlsx"))
pm16_facial = pd.read_excel(os.path.join(data_dir, "Final_PM16-Facial.xlsx"))

# Feature Configuration
feature_config_toilet = {
    '% NBKP': {
        'min': float(pm16_toilet['% NBKP'].min()),
        'max': float(pm16_toilet['% NBKP'].max()),
        'default': 0,
        'step': 1.0,
        'format': "%.2f"
    },
    'Mean_Load KWH Tickling Refiner': {
        'min': float(pm16_toilet['Mean_Load KWH Tickling Refiner'].min()),
        'max': float(pm16_toilet['Mean_Load KWH Tickling Refiner'].max()),
        'default': 0,
        'step': 1,
        'format': "%.2f"},
    'Mean_Creping': {
        'min': float(pm16_toilet['Mean_Creping'].min()),
        'max': float(pm16_toilet['Mean_Creping'].max()),
        'default': 0,
        'step': 0.1,
        'format': "%.2f"
    },
    'Mean_Jet Wire Ratio': {
        'min': float(pm16_toilet['Mean_Jet Wire Ratio'].min()),
        'max': float(pm16_toilet['Mean_Jet Wire Ratio'].max()),
        'default': 0,
        'step': 0.01,
        'format': "%.2f"
    },
    'GSM': {
        'min': float(pm16_toilet['GSM'].min()),
        'max': float(pm16_toilet['GSM'].max()),
        'default': 0,
        'step': 0.1,
        'format': "%.2f"
    },
    'Mean_Flow Coating': {
        'min': float(pm16_toilet['Mean_Flow Coating'].min()),
        'max': float(pm16_toilet['Mean_Flow Coating'].max()),
        'default': 0,
        'step': 0.1,
        'format': "%.2f"
    },
    'Mean_Flow Release': {
        'min': float(pm16_toilet['Mean_Flow Release'].min()),
        'max': float(pm16_toilet['Mean_Flow Release'].max()),
        'default': 0,
        'step': 0.1,
        'format': "%.2f"
    },
    'coating_release_ratio': {'min': 0.0,'max': 1.0}
}
feature_config_towel = {
    '% NBKP': {
        'min': float(pm16_towel['% NBKP'].min()),
        'max': float(pm16_towel['% NBKP'].max()),
        'default': 0,
        'step': 1.0,
        'format': "%.2f"
    },
    'Mean_Load KWH Tickling Refiner': {
        'min': float(pm16_towel['Mean_Load KWH Tickling Refiner'].min()),
        'max': float(pm16_towel['Mean_Load KWH Tickling Refiner'].max()),
        'default': 0,
        'step': 1,
        'format': "%.2f"},
    'Mean_Creping': {
        'min': float(pm16_towel['Mean_Creping'].min()),
        'max': float(pm16_towel['Mean_Creping'].max()),
        'default': 0,
        'step': 0.1,
        'format': "%.2f"
    },
    'Mean_Jet Wire Ratio': {
        'min': float(pm16_towel['Mean_Jet Wire Ratio'].min()),
        'max': float(pm16_towel['Mean_Jet Wire Ratio'].max()),
        'default': 0,
        'step': 0.01,
        'format': "%.2f"
    },
    'GSM': {
        'min': float(pm16_towel['GSM'].min()),
        'max': float(pm16_towel['GSM'].max()),
        'default': 0,
        'step': 0.1,
        'format': "%.2f"
    },
    'Mean_Flow Coating': {
        'min': float(pm16_towel['Mean_Flow Coating'].min()),
        'max': float(pm16_towel['Mean_Flow Coating'].max()),
        'default': 0,
        'step': 0.1,
        'format': "%.2f"
    },
    'Mean_Flow Release': {
        'min': float(pm16_towel['Mean_Flow Release'].min()),
        'max': float(pm16_towel['Mean_Flow Release'].max()),
        'default': 0,
        'step': 0.1,
        'format': "%.2f"
    },
    'coating_release_ratio': {'min': 0.0,'max': 1.0}
}
feature_config_facial = {
    '% NBKP': {
        'min': float(pm16_facial['% NBKP'].min()),
        'max': float(pm16_facial['% NBKP'].max()),
        'default': 0,
        'step': 1.0,
        'format': "%.2f"
    },
    'Mean_Load KWH Tickling Refiner': {
        'min': float(pm16_facial['Mean_Load KWH Tickling Refiner'].min()),
        'max': float(pm16_facial['Mean_Load KWH Tickling Refiner'].max()),
        'default': 0,
        'step': 1,
        'format': "%.2f"},
    'Mean_Creping': {
        'min': float(pm16_facial['Mean_Creping'].min()),
        'max': float(pm16_facial['Mean_Creping'].max()),
        'default': 0,
        'step': 0.1,
        'format': "%.2f"
    },
    'Mean_Jet Wire Ratio': {
        'min': float(pm16_facial['Mean_Jet Wire Ratio'].min()),
        'max': float(pm16_facial['Mean_Jet Wire Ratio'].max()),
        'default': 0,
        'step': 0.01,
        'format': "%.2f"
    },
    'GSM': {
        'min': float(pm16_facial['GSM'].min()),
        'max': float(pm16_facial['GSM'].max()),
        'default': 0,
        'step': 0.1,
        'format': "%.2f"
    },
    'Mean_Flow Coating': {
        'min': float(pm16_facial['Mean_Flow Coating'].min()),
        'max': float(pm16_facial['Mean_Flow Coating'].max()),
        'default': 0,
        'step': 0.1,
        'format': "%.2f"
    },
    'Mean_Flow Release': {
        'min': float(pm16_facial['Mean_Flow Release'].min()),
        'max': float(pm16_facial['Mean_Flow Release'].max()),
        'default': 0,
        'step': 0.1,
        'format': "%.2f"
    },
    'coating_release_ratio': {'min': 0.0,'max': 1.0}
}

# Pilih Config Berdasarkan Grade
if grade == "Toilet":
    feature_config = feature_config_toilet
elif grade == "Towel":
    feature_config = feature_config_towel
elif grade == "Facial":
    feature_config = feature_config_facial

# Feature labels
feature_labels = {
    '% NBKP': 'NBKP (%)',
    'Mean_Load KWH Tickling Refiner':'Load KWH Tickling Refiner',
    'Mean_Creping': 'Creping',
    'Mean_Jet Wire Ratio':'Jet Wire Ratio',
    'Mean_Flow Coating':'Flow Coating',
    'Mean_Flow Release':'Flow Release'
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
    if feature == "coating_release_ratio":
        continue
    if feature in ["Mean_Flow Coating","Mean_Flow Release"]:
        continue
    
    config = feature_config.get(feature)

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

# Save Input State
with open(state_file, "w") as f:
    json.dump({**input_data,
               "Mean_Flow Coating": coating_value,
               "Mean_Flow Release": release_value},
               f)

# Button Section
col1, col2 = st.columns(2)
with col1:
    predict_button = st.button("Predict",key="predict_button_pm16")
with col2:
    reset_button = st.button("Hapus Semua",key="reset_button_pm16")
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
    df['coating_release_ratio'] = (coating_release_ratio)
    prediction_ratio = model.predict(df)[0]
    #gsm = df['GSM'].values[0]
    #prediction_mdt = prediction_ratio * gsm
    st.success(f"Hasil Prediksi MDT PM16 "f"({grade}): "f"{prediction_ratio:.2f}")