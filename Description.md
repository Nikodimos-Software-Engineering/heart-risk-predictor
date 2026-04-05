## **Feature Descriptions and Value Meanings**

### **1. age** (int64)
- **Description**: Age of the patient in years
- **Range**: 29 - 77 years
- **Mean**: ~54 years
- **Interpretation**: Direct age value

### **2. sex** (int64)
- **Description**: Gender of the patient
- **Values**:
  - `0` = Female
  - `1` = Male
- **Distribution**: ~70% male, ~30% female

### **3. cp - Chest Pain Type** (int64)
- **Description**: Type of chest pain experienced
- **Values**:
  - `0` = Typical angina (classic chest pain related to heart disease)
  - `1` = Atypical angina (chest pain not typically heart-related)
  - `2` = Non-anginal pain (chest pain not caused by heart issues)
  - `3` = Asymptomatic (no chest pain)
- **Clinical Note**: Typical angina is strongly associated with heart disease

### **4. trestbps - Resting Blood Pressure** (int64)
- **Description**: Resting blood pressure in mm Hg (millimeters of mercury)
- **Range**: 94 - 200 mm Hg
- **Mean**: ~132 mm Hg
- **Interpretation**: 
  - Normal: < 120 mm Hg
  - Elevated: 120-129 mm Hg
  - High: ≥ 130 mm Hg
  - Higher values indicate hypertension risk

### **5. chol - Serum Cholesterol** (int64)
- **Description**: Serum cholesterol in mg/dl (milligrams per deciliter)
- **Range**: 126 - 564 mg/dl
- **Mean**: ~246 mg/dl
- **Interpretation**:
  - Desirable: < 200 mg/dl
  - Borderline high: 200-239 mg/dl
  - High: ≥ 240 mg/dl

### **6. fbs - Fasting Blood Sugar** (int64)
- **Description**: Fasting blood sugar > 120 mg/dl
- **Values**:
  - `0` = False (blood sugar ≤ 120 mg/dl)
  - `1` = True (blood sugar > 120 mg/dl)
- **Clinical Note**: Indicates diabetes risk
- **Distribution**: Only ~15% have elevated fasting blood sugar

### **7. restecg - Resting Electrocardiographic Results** (int64)
- **Description**: Resting ECG (EKG) results
- **Values**:
  - `0` = Normal
  - `1` = ST-T wave abnormality (indicates potential heart issues)
  - `2` = Left ventricular hypertrophy (enlarged heart)
- **Interpretation**: Higher values indicate more concerning ECG findings

### **8. thalach - Maximum Heart Rate Achieved** (int64)
- **Description**: Maximum heart rate achieved during exercise test
- **Range**: 71 - 202 bpm (beats per minute)
- **Mean**: ~149 bpm
- **Interpretation**: 
  - Lower than expected for age may indicate heart problems
  - Normal formula: 220 - age (rough estimate)
  - Higher values generally indicate better cardiovascular fitness

### **9. exang - Exercise Induced Angina** (int64)
- **Description**: Chest pain during exercise
- **Values**:
  - `0` = No exercise-induced angina
  - `1` = Yes, exercise-induced angina
- **Clinical Note**: Strong indicator of heart disease (~34% of patients experience this)

### **10. oldpeak - ST Depression** (float64)
- **Description**: ST depression induced by exercise relative to rest
- **Range**: 0.0 - 6.2
- **Mean**: ~1.07
- **Interpretation**:
  - Measures how much the ST segment of ECG drops during exercise
  - Higher values indicate more severe myocardial ischemia (reduced blood flow to heart)
  - Values > 1.0 are concerning

### **11. slope - Slope of ST Segment** (int64)
- **Description**: Slope of the peak exercise ST segment
- **Values**:
  - `0` = Upsloping (less concerning, often normal)
  - `1` = Flat (intermediate risk)
  - `2` = Downsloping (most concerning, strongly indicates heart disease)
- **Clinical Note**: Downsloping is a strong predictor of heart disease

### **12. ca - Number of Major Vessels** (int64)
- **Description**: Number of major blood vessels (0-4) colored by fluoroscopy
- **Range**: 0 - 4
- **Mean**: ~0.75
- **Interpretation**:
  - Counts how many of the main coronary arteries show blockage
  - 0 = No visible blockages
  - 1-4 = Number of blocked vessels
  - Higher numbers indicate more severe coronary artery disease

### **13. thal - Thallium Stress Test Result** (int64)
- **Description**: Results of thallium stress test (nuclear imaging)
- **Values**:
  - `0` = Normal (no perfusion defects)
  - `1` = Fixed defect (likely old heart attack/scar tissue)
  - `2` = Reversible defect (indicates ischemia/blockage)
  - `3` = Not applicable or not determined
- **Interpretation**:
  - Fixed defect: Previous heart damage
  - Reversible defect: Areas that don't get enough blood during stress but improve at rest (indicates blockages)

### **14. target - Heart Disease Diagnosis** (int64)
- **Description**: Presence of heart disease (target variable)
- **Values**:
  - `0` = No heart disease
  - `1` = Heart disease present
- **Distribution**: ~51% have heart disease, ~49% don't (well-balanced dataset)

## **Key Clinical Insights**

### **Strongest Risk Factors** (typically high correlation with target):
1. **cp (chest pain type)** - especially typical angina (value 0)
2. **thalach (max heart rate)** - lower values indicate higher risk
3. **ca (number of vessels)** - more blockages = higher risk
4. **oldpeak (ST depression)** - higher values indicate higher risk
5. **exang (exercise angina)** - presence indicates higher risk
6. **slope** - downsloping (value 2) indicates higher risk

### **Typical Values for High-Risk Patients**:
- Older age (>60)
- Male (sex=1)
- Chest pain (cp=0 or 1)
- High blood pressure (>140 mm Hg)
- High cholesterol (>240 mg/dl)
- Low max heart rate (<130 bpm)
- Exercise-induced angina (exang=1)
- High ST depression (>2.0)
- Multiple blocked vessels (ca≥2)
- Thallium defects (thal=1 or 2)

### **Typical Values for Low-Risk Patients**:
- Younger age (<50)
- Female (sex=0)
- No chest pain (cp=2 or 3)
- Normal blood pressure (<120 mm Hg)
- Normal cholesterol (<200 mg/dl)
- High max heart rate (>160 bpm)
- No exercise angina (exang=0)
- Low ST depression (<0.5)
- No blocked vessels (ca=0)
- Normal thallium scan (thal=0)

This dataset comes from the Cleveland Heart Disease database, which is widely used for cardiovascular disease prediction research. The target variable indicates whether the patient has a heart condition (presence of coronary artery disease > 50% diameter narrowing in at least one major vessel).