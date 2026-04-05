import streamlit as st
import joblib
import pandas as pd
import numpy as np
import shap
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Heart Risk Predictor",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

custom_css = """
<style>
    .main {
        padding: 0rem 1rem;
    }
    
    .main-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .risk-high {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 15px;
        text-align: center;
        animation: pulse 2s infinite;
    }
    
    .risk-low {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1rem;
        border-radius: 15px;
        text-align: center;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 15px;
        text-align: center;
        backdrop-filter: blur(10px);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: bold;
        border-radius: 50px;
        transition: transform 0.3s;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    
    .info-box {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    .shap-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0 auto;
        max-width: 800px;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

st.markdown("""
<div class="main-title">
    <h1 style="color: white; margin: 0;">Heart Disease Risk Predictor</h1>
    <p style="color: white; margin: 0.5rem 0 0 0;">AI-Powered Cardiovascular Risk Assessment</p>
</div>
""", unsafe_allow_html=True)

with st.container():
    col_info, col_tip = st.columns([2, 1])
    with col_info:
        st.markdown("""
        <div class="info-box">
        <strong>How it works:</strong> Enter your health metrics below and get an instant risk assessment 
        powered by machine learning. The system analyzes 13 clinical features to predict heart disease risk.
        </div>
        """, unsafe_allow_html=True)
    with col_tip:
        st.markdown("""
        <div class="info-box">
        <strong>Pro Tip:</strong> Click "Explain Prediction" to understand which factors influence your risk!
        </div>
        """, unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

sex_map = {"Male": 1, "Female": 0}
chest_pain_map = {
    "Typical Angina": 0,
    "Atypical Angina": 1,
    "Non-anginal Pain": 2,
    "Asymptomatic": 3
}
truth_map = {"False": 0, "True": 1}
restecg_map = {
    "Normal": 0,
    "ST-T wave Abnormality": 1,
    "Left Ventricular Hypertrophy": 2
}
slope_map = {"Upsloping": 0, "Flat": 1, "Downsloping": 2}
thal_map = {
    "Normal": 0,
    "Fixed Defect": 1,
    "Reversible Defect": 2,
    "Not Applicable or Not Determined": 3
}

with col1:
    st.markdown("### Personal Information")
    age = st.number_input("Age (years)", min_value=0, max_value=120, value=50)
    sex_label = st.selectbox("Gender", list(sex_map.keys()))
    sex = sex_map[sex_label]
    cp_label = st.selectbox("Chest Pain Type", list(chest_pain_map.keys()))
    cp = chest_pain_map[cp_label]
    trestbps = st.number_input("Resting Blood Pressure (mm Hg)", min_value=0, max_value=500, value=120)
    chol = st.number_input("Serum Cholesterol (mg/dl)", min_value=0, max_value=1000, value=200)

with col2:
    st.markdown("### Clinical Measurements")
    fbs_label = st.selectbox("Fasting Blood Sugar > 120 mg/dl", list(truth_map.keys()))
    fbs = truth_map[fbs_label]
    restecg_label = st.selectbox("Resting ECG Results", list(restecg_map.keys()))
    restecg = restecg_map[restecg_label]
    thalach = st.number_input("Maximum Heart Rate Achieved", min_value=0, max_value=500, value=150)
    exang_label = st.selectbox("Exercise Induced Angina", list(truth_map.keys()))
    exang = truth_map[exang_label]

with col3:
    st.markdown("### Advanced Metrics")
    oldpeak = st.slider("ST Depression", min_value=0.0, max_value=7.0, value=1.0, step=0.1)
    slope_label = st.selectbox("ST Segment Slope", list(slope_map.keys()))
    slope = slope_map[slope_label]
    ca = st.slider("Number of Major Vessels", min_value=0, max_value=4, value=0)
    thal_label = st.selectbox("Thallium Stress Test Result", list(thal_map.keys()))
    thal = thal_map[thal_label]

model = joblib.load("health_risk_predictor.pkl")
scaler = joblib.load('health_features_scaler.pkl')

predictor = [[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]]
scaled = scaler.transform(predictor)
prediction = model.predict(scaled)[0]
probabilities = model.predict_proba(scaled)[0]

st.markdown("---")

col_result, col_gauge = st.columns([1, 1])

with col_result:
    if prediction == 1:
        st.markdown("""
        <div class="risk-high">
            <h2 style="color: white; margin: 0;">⚠️ HIGH RISK</h2>
            <p style="color: white; margin: 0.5rem 0 0 0;">Please consult a healthcare professional immediately</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="risk-low">
            <h2 style="color: white; margin: 0;">✅ LOW RISK</h2>
            <p style="color: white; margin: 0.5rem 0 0 0;">Maintain a healthy lifestyle</p>
        </div>
        """, unsafe_allow_html=True)

with col_gauge:
    risk_percentage = probabilities[1] * 100
    st.markdown(f"""
    <div class="metric-card">
        <h3 style="margin: 0;">Risk Score</h3>
        <div style="font-size: 3rem; font-weight: bold; margin: 0.5rem 0;">{risk_percentage:.1f}%</div>
        <div style="background: #e0e0e0; border-radius: 10px; height: 10px; overflow: hidden;">
            <div style="background: linear-gradient(90deg, #4facfe, #f093fb); width: {risk_percentage}%; height: 100%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

col_metric1, col_metric2, col_metric3 = st.columns(3)
with col_metric1:
    st.metric("Disease Probability", f"{probabilities[1]*100:.1f}%")
with col_metric2:
    st.metric("No Disease Probability", f"{probabilities[0]*100:.1f}%")
with col_metric3:
    confidence = max(probabilities) * 100
    st.metric("Model Confidence", f"{confidence:.1f}%")

with st.expander("Detailed Probabilities", expanded=False):
    col_bar1, col_bar2 = st.columns(2)
    with col_bar1:
        st.markdown(f"**No Disease:** {probabilities[0]*100:.1f}%")
        st.progress(probabilities[0])
    with col_bar2:
        st.markdown(f"**Disease:** {probabilities[1]*100:.1f}%")
        st.progress(probabilities[1])

@st.cache_resource
def load_shap_explainer():
    try:
        X_train = pd.read_csv("heart.csv").drop('target', axis=1)
        background_data = shap.sample(X_train, 50)
        explainer = shap.KernelExplainer(model.predict_proba, background_data)
        return explainer
    except Exception as e:
        st.error(f"Failed to load SHAP explainer: {e}")
        return None

explainer = load_shap_explainer()

def create_shap_plot(input_values, feature_names):
    input_scaled = scaler.transform([input_values])
    shap_values = explainer.shap_values(input_scaled)
    
    if len(shap_values.shape) == 3:
        shap_values_class1 = shap_values[0, :, 1]
        base_value = explainer.expected_value[1]
    elif len(shap_values.shape) == 2:
        shap_values_class1 = shap_values[:, 1]
        base_value = explainer.expected_value[1]
    else:
        shap_values_class1 = shap_values[1] if isinstance(shap_values, list) else shap_values
        base_value = explainer.expected_value[1] if isinstance(explainer.expected_value, list) else explainer.expected_value
    
    if isinstance(base_value, np.ndarray):
        base_value = base_value[1]
    
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(8, 5), facecolor='white')
    shap.waterfall_plot(
        shap.Explanation(
            values=shap_values_class1,
            base_values=base_value,
            data=np.array(input_values),
            feature_names=feature_names
        ),
        show=False,
        max_display=8
    )
    plt.tight_layout()
    return fig

if st.button("Explain This Prediction with AI", use_container_width=True):
    if explainer is not None:
        with st.spinner("Analyzing your health data with SHAP..."):
            feature_names = ['Age', 'Sex', 'Chest Pain', 'Blood Pressure', 'Cholesterol', 'Fasting Blood Sugar', 
                           'ECG Results', 'Max Heart Rate', 'Exercise Angina', 'ST Depression', 
                           'ST Slope', 'Major Vessels', 'Thallium Test']
            current_input = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
            
            try:
                fig = create_shap_plot(current_input, feature_names)
                
                col_center1, col_graph, col_center2 = st.columns([1, 2, 1])
                with col_graph:
                    st.pyplot(fig, use_container_width=True)
                
                with st.expander("Understanding Your Results", expanded=True):
                    col_exp1, col_exp2, col_exp3 = st.columns(3)
                    with col_exp1:
                        st.markdown("""
                        **🔴 Red Bars**
                        Features that increase your risk
                        """)
                    with col_exp2:
                        st.markdown("""
                        **🔵 Blue Bars**
                        Features that decrease your risk
                        """)
                    with col_exp3:
                        st.markdown("""
                        **📏 Bar Length**
                        Strength of influence
                        """)
                    
                    st.info("**Remember:** Focus on improving red factors (cholesterol, blood pressure, exercise) and maintaining blue factors. Always consult healthcare professionals for medical advice.")
                    
            except Exception as e:
                st.error(f"Error creating visualization: {e}")
                st.info("Try: `pip install --upgrade shap matplotlib`")
    else:
        st.error("SHAP explainer not loaded. Please check your setup.")

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <small>⚠️ Disclaimer: This tool is for educational purposes only. Not a substitute for professional medical advice.</small>
</div>
""", unsafe_allow_html=True)