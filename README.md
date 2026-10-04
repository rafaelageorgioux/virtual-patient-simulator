# 🩺 Virtual Patient Simulator

An interactive clinical-reasoning simulator for medical students, built in **Python** with **Streamlit**.

The app contains **32 synthetic patient cases** and **34 synthetic clinical visuals**. Students work through a consultation from history taking to management and receive structured feedback at the end.

> **Educational use only.** This project is designed for study and supervised clinical-skills practice. It is not a substitute for clinical guidelines, medical supervision, or real patient care.

---

## ✨ Features

- 32 synthetic clinical cases
- Realistic patient personalities and varied responses
- History taking with natural-language question matching
- Patient trust/emotion changes based on communication style
- Focused physical examination by body system
- Selective investigations
- Clinical visuals including imaging, ECGs, endoscopy, histology and microscopy
- Differential diagnosis stage
- Final diagnosis submission
- Management/treatment planning
- Scoring and structured feedback
- Red-flag / safety learning points
- Automatically generated clinical clerking note
- Easy, OSCE and Hard modes
- Polished lilac/blue medical UI

---

## 🧠 Clinical workflow

1. **History**
2. **Physical examination**
3. **Investigations**
4. **Differential diagnoses**
5. **Final diagnosis**
6. **Management**
7. **End-of-case feedback**

---

## 🚀 Run locally

### 1. Install Python

Make sure Python 3 is installed.

### 2. Clone or download this repository

```bash
git clone <YOUR-REPOSITORY-URL>
cd virtual-patient-simulator
```

Or download the ZIP and open the folder in Terminal.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the app

```bash
streamlit run 32cases.py
```

Streamlit will open the simulator in your browser.

---

## ☁️ Deploy with Streamlit Community Cloud

1. Upload this project to a GitHub repository.
2. Go to Streamlit Community Cloud.
3. Connect your GitHub account.
4. Choose the repository.
5. Set the main file path to:

```text
32cases.py
```

6. Deploy.

No API key is required for the current version.

---

## 📁 Project structure

```text
virtual-patient-simulator/
├── 32cases.py
├── images/
│   └── ... clinical visual assets ...
├── .streamlit/
│   └── config.toml
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🛠️ Built with

- Python
- Streamlit
- Pillow

---

## 🎓 Why I built this

This project was designed as a medical-student learning tool to practise the full clinical-reasoning process in an interactive format rather than studying isolated facts.

The aim is to make revision more active by requiring the learner to decide what to ask, what to examine, which investigations to order, what diagnoses to consider and how to manage the patient.

---

## 🧪 Case content

Cases span multiple areas of undergraduate medicine, including:

- Cardiology
- Respiratory medicine
- Gastroenterology
- Neurology
- Endocrinology
- Infectious disease
- Haematology
- Urology
- Gynaecology
- Emergency medicine
- Rheumatology
- Vascular medicine

All cases are synthetic.

---

## ⚠️ Medical disclaimer

The simulator simplifies clinical reasoning for educational purposes.

Management pathways may differ between countries, hospitals and guideline bodies. Always use current local guidance and supervised clinical teaching for real-world decision-making.

---

## 🖼️ Visual assets

All visuals included in this project are synthetic educational images created for the simulator.

They are not real patient records and should not be used for diagnosis or clinical decision-making.

---

## 💼 CV / portfolio description

**Short version**

> Developed an interactive virtual-patient simulator in Python and Streamlit featuring 32 clinical cases, clinical visuals, history taking, focused examination, investigations, differential diagnosis, management planning and structured feedback.

**Longer version**

> Designed and developed a Python/Streamlit virtual-patient simulator for medical education, featuring 32 synthetic clinical cases and multimodal clinical visuals. Implemented interactive history taking, patient-behaviour logic, focused examination, selective investigations, differential diagnosis, management scoring and end-of-case feedback to support active clinical-reasoning practice.

---

## 🔮 Possible future improvements

- More cases
- More advanced natural-language processing
- User accounts and saved progress
- Faculty-created custom cases
- Structured OSCE marking schemes
- Analytics for teaching cohorts
- Multiplayer or tutor mode

---

## 📜 License

MIT License.
