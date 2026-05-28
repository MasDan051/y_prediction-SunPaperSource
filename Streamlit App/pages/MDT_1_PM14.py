import streamlit as st
import pandas as pd
import joblib
import os
import json

st.title("Prediksi MDT PM14")

grade = st.selectbox(
    "Pilih Grade Tissue",
    ["Facial", "Toilet"]
)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
state_dir = os.path.join(BASE_DIR, "state")
os.makedirs(state_dir, exist_ok=True)
state_file = os.path.join(
    state_dir,
    f"PM14_{grade}_input_state.json"
)

saved_state = {}
if os.path.exists(state_file):
    with open(state_file, "r") as f:
        saved_state = json.load(f)

model_path = os.path.join(BASE_DIR,"models","PM14",grade,"model.pkl")
features_path = os.path.join(BASE_DIR,"models","PM14",grade,"features.pkl")
model = joblib.load(model_path)
features = joblib.load(features_path)

data_dir = os.path.join(BASE_DIR, "..", "Data Final")

if grade == "Toilet":
    pm14_toilet = pd.read_excel(
        os.path.join(data_dir, "Final_PM14-Toilet.xlsx")
    )
    feature_config_toilet = {
        'Mean_Yankee Pressure': {
            'min': float(pm14_toilet['Mean_Yankee Pressure'].min()),
            'max': float(pm14_toilet['Mean_Yankee Pressure'].max()),
            'default': 0,
            'step': 1.0,
            'format': "%.2f"
        },
        '% NBKP': {
            'min': float(pm14_toilet['% NBKP'].min()),
            'max': float(pm14_toilet['% NBKP'].max()),
            'default': 0,
            'step': 1.0,
            'format': "%.3f"
        },
        'Mean_Load KWH Refiner': {
            'min': float(pm14_toilet['Mean_Load KWH Refiner'].min()),
            'max': float(pm14_toilet['Mean_Load KWH Refiner'].max()),
            'default': 0,
            'step': 1,
            'format': "%.3f"
        },
        'Mean_Creping': {
            'min': float(pm14_toilet['Mean_Creping'].min()),
            'max': float(pm14_toilet['Mean_Creping'].max()),
            'default': 0,
            'step': 0.1,
            'format': "%.2f"
        },
        'Mean_Jet Wire Ratio': {
            'min': float(pm14_toilet['Mean_Jet Wire Ratio'].min()),
            'max': float(pm14_toilet['Mean_Jet Wire Ratio'].max()),
            'default': 0,
            'step': 0.01,
            'format': "%.3f"
        },
        'GSM': {
            'min': float(pm14_toilet['GSM'].min()),
            'max': float(pm14_toilet['GSM'].max()),
            'default': 0,
            'step': 0.1,
            'format': "%.1f"
        },
        'Mean_Flow Coating': {
            'min': float(pm14_toilet['Mean_Flow Coating'].min()),
            'max': float(pm14_toilet['Mean_Flow Coating'].max()),
            'default': 0,
            'step': 0.1,
            'format': "%.2f"
        },
        'Mean_Flow Release': {
            'min': float(pm14_toilet['Mean_Flow Release'].min()),
            'max': float(pm14_toilet['Mean_Flow Release'].max()),
            'default': 0,
            'step': 0.1,
            'format': "%.2f"
        },
        'coating_release_ratio': {'min': 0.0, 'max': 1.0},
        'pseudo_mass': {'min': 2.73, 'max': 3.67}
    }
    feature_config = feature_config_toilet

elif grade == "Facial":
    pm14_facial = pd.read_excel(
        os.path.join(data_dir, "Final_PM14-Facial.xlsx")
    )
    feature_config_facial = {
        'Mean_Yankee Pressure': {
            'min': float(pm14_facial['Mean_Yankee Pressure'].min()),
            'max': float(pm14_facial['Mean_Yankee Pressure'].max()),
            'default': 0,
            'step': 1.0,
            'format': "%.2f"
        },
        '% NBKP': {
            'min': float(pm14_facial['% NBKP'].min()),
            'max': float(pm14_facial['% NBKP'].max()),
            'default': 0,
            'step': 1.0,
            'format': "%.3f"
        },
        'Mean_Load KWH Refiner': {
            'min': float(pm14_facial['Mean_Load KWH Refiner'].min()),
            'max': float(pm14_facial['Mean_Load KWH Refiner'].max()),
            'default': 0,
            'step': 1,
            'format': "%.3f"
        },
        'Mean_Creping': {
            'min': float(pm14_facial['Mean_Creping'].min()),
            'max': float(pm14_facial['Mean_Creping'].max()),
            'default': 0,
            'step': 0.1,
            'format': "%.2f"
        },
        'Mean_Jet Wire Ratio': {
            'min': float(pm14_facial['Mean_Jet Wire Ratio'].min()),
            'max': float(pm14_facial['Mean_Jet Wire Ratio'].max()),
            'default': 0,
            'step': 0.01,
            'format': "%.3f"
        },
        'GSM': {
            'min': float(pm14_facial['GSM'].min()),
            'max': float(pm14_facial['GSM'].max()),
            'default': 0,
            'step': 0.1,
            'format': "%.1f"
        },
        'Mean_Flow Coating': {
            'min': float(pm14_facial['Mean_Flow Coating'].min()),
            'max': float(pm14_facial['Mean_Flow Coating'].max()),
            'default': 0,
            'step': 0.1,
            'format': "%.2f"
        },
        'Mean_Flow Release': {
            'min': float(pm14_facial['Mean_Flow Release'].min()),
            'max': float(pm14_facial['Mean_Flow Release'].max()),
            'default': 0,
            'step': 0.1,
            'format': "%.2f"
        },
        'coating_release_ratio': {'min': 0.0, 'max': 1.0},
        'pseudo_mass': {'min': 2.86, 'max': 3.67}
    }
    feature_config = feature_config_facial

elif grade == "Towel":
    pm14_towel = pd.read_excel(
        os.path.join(data_dir, "Final_PM14-Towel.xlsx")
    )
    feature_config_towel = {
        'Mean_Yankee Pressure': {
            'min': float(pm14_towel['Mean_Yankee Pressure'].min()),
            'max': float(pm14_towel['Mean_Yankee Pressure'].max()),
            'default': 0,
            'step': 1.0,
            'format': "%.2f"
        },
        '% NBKP': {
            'min': float(pm14_towel['% NBKP'].min()),
            'max': float(pm14_towel['% NBKP'].max()),
            'default': 0,
            'step': 1.0,
            'format': "%.3f"
        },
        'Mean_Load KWH Refiner': {
            'min': float(pm14_towel['Mean_Load KWH Refiner'].min()),
            'max': float(pm14_towel['Mean_Load KWH Refiner'].max()),
            'default': 0,
            'step': 1,
            'format': "%.3f"
        },
        'Mean_Creping': {
            'min': float(pm14_towel['Mean_Creping'].min()),
            'max': float(pm14_towel['Mean_Creping'].max()),
            'default': 0,
            'step': 0.1,
            'format': "%.2f"
        },
        'Mean_Jet Wire Ratio': {
            'min': float(pm14_towel['Mean_Jet Wire Ratio'].min()),
            'max': float(pm14_towel['Mean_Jet Wire Ratio'].max()),
            'default': 0,
            'step': 0.01,
            'format': "%.3f"
        },
        'GSM': {
            'min': float(pm14_towel['GSM'].min()),
            'max': float(pm14_towel['GSM'].max()),
            'default': 0,
            'step': 0.1,
            'format': "%.1f"
        },
        'Mean_Flow Coating': {
            'min': float(pm14_towel['Mean_Flow Coating'].min()),
            'max': float(pm14_towel['Mean_Flow Coating'].max()),
            'default': 0,
            'step': 0.1,
            'format': "%.2f"
        },
        'Mean_Flow Release': {
            'min': float(pm14_towel['Mean_Flow Release'].min()),
            'max': float(pm14_towel['Mean_Flow Release'].max()),
            'default': 0,
            'step': 0.1,
            'format': "%.2f"
        },
        'coating_release_ratio': {'min': 0.0, 'max': 1.0},
        'pseudo_mass': {'min': 2, 'max': 4}
    }
    feature_config = feature_config_towel

feature_labels = {
    '% NBKP': 'NBKP (%)',
    'Mean_Load KWH Refiner': 'Load KWH Refiner',
    'Mean_Creping': 'Creping',
    'Mean_Jet Wire Ratio': 'Jet Wire Ratio',
    'Mean_Flow Coating': 'Flow Coating',
    'Mean_Flow Release': 'Flow Release',
    'Mean_Yankee Pressure': 'Yankee Pressure',
    'Mean_Stock Flow': 'Stock Flow',
    'Mean_Stock Consistency': 'Stock Consistency',
    'Mean_Yankee Speed': 'Yankee Speed',
}

for feature in feature_config:
    if feature not in st.session_state:
        if feature == "Mean_Flow Release":
            st.session_state[feature] = 0.1
        elif feature == "Mean_Yankee Speed":
            st.session_state[feature] = 0.1
        else:
            default_value = feature_config[feature].get('default', 0.0)
            st.session_state[feature] = saved_state.get(feature, default_value)

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
        label=feature_labels.get(feature, feature),
        min_value=0.0,
        max_value=(float(config['hard_max']) if 'hard_max' in config else None),
        step=float(config['step']),
        value=float(st.session_state.get(feature, config['default'])),
        format=config['format'],
        help=(f"Data histori training: {config['min']} - {config['max']}" if 'min' in config else None),
        key=feature
    )

    if 'min' in config:
        if input_data[feature] < config['min'] or input_data[feature] > config['max']:
            st.warning(
                f"⚠️ Nilai untuk '{feature_labels.get(feature, feature)}' "
                f"berada di luar data histori pelatihan model "
                f"({config['min']} - {config['max']}). "
                f"Hal ini dapat menurunkan akurasi prediksi."
            )

st.markdown("### Flow Parameters")

coating_value = st.number_input(
    feature_labels['Mean_Flow Coating'],
    min_value=0.0,
    step=1.0,
    value=float(st.session_state.get("Mean_Flow Coating", 0.0)),
    format="%.2f",
    key="Mean_Flow Coating"
)

release_value = st.number_input(
    feature_labels['Mean_Flow Release'],
    min_value=0.1,
    step=1.0,
    value=float(st.session_state.get("Mean_Flow Release", 0.1)),
    format="%.2f",
    key="Mean_Flow Release"
)

coating_release_ratio = (coating_value / release_value)

st.info(f"Coating Release Ratio: {coating_release_ratio:.3f}")

ratio_config = feature_config['coating_release_ratio']

if coating_release_ratio < ratio_config['min'] or coating_release_ratio > ratio_config['max']:
    st.warning(
        f"⚠️ Hasil pembagian 'Flow Coating' / 'Flow Release' berada di luar "
        f"data histori pelatihan model ({ratio_config['min']} - {ratio_config['max']}). "
        f"Hal ini dapat menurunkan akurasi prediksi."
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
    value=float(st.session_state.get("Mean_Yankee Speed", 0.1)),
    format="%.2f",
    key="Mean_Yankee Speed"
)

pseudo_mass = (stock_flow_value * stock_consistency_value) / yankee_speed_value

st.info(f"Pseudo Mass: {pseudo_mass:.3f}")

pseudo_mass_config = feature_config['pseudo_mass']

if pseudo_mass < pseudo_mass_config['min'] or pseudo_mass > pseudo_mass_config['max']:
    st.warning(
        f"⚠️ Hasil perhitungan 'Stock Flow × Stock Consistency / Yankee Speed' "
        f"berada di luar data histori pelatihan model "
        f"({pseudo_mass_config['min']} - {pseudo_mass_config['max']}). "
        f"Hal ini dapat menurunkan akurasi prediksi."
    )

with open(state_file, "w") as f:
    json.dump({
        **input_data,
        "Mean_Flow Coating": coating_value,
        "Mean_Flow Release": release_value,
        "Mean_Stock Flow": stock_flow_value,
        "Mean_Stock Consistency": stock_consistency_value,
        "Mean_Yankee Speed": yankee_speed_value
    }, f)

col1, col2 = st.columns(2)
with col1:
    predict_button = st.button("Predict", key="predict_button_pm14")
with col2:
    reset_button = st.button("Hapus Semua", key="reset_button_pm14")

if reset_button:
    for feature in feature_config:
        if feature in st.session_state:
            del st.session_state[feature]
    if os.path.exists(state_file):
        os.remove(state_file)
    st.rerun()

if predict_button:
    df = pd.DataFrame([input_data])
    df['coating_release_ratio'] = coating_release_ratio
    df['pseudo_mass'] = pseudo_mass
    prediction_ratio = model.predict(df)[0]
    st.success(f"Hasil Prediksi MDT PM14 ({grade}): {prediction_ratio:.2f}")