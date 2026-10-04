
import streamlit as st
import random
import re
from difflib import SequenceMatcher
from pathlib import Path

# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Virtual Patient Simulator",
    page_icon="🩺",
    layout="centered"
)


# =========================================================
# GLOBAL UI POLISH
# =========================================================
st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at 0% 0%, rgba(231,220,246,.48), transparent 25%),
            radial-gradient(circle at 100% 0%, rgba(218,237,245,.50), transparent 28%),
            linear-gradient(180deg, #FCFBFD 0%, #F8F8FB 100%);
    }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    .block-container { max-width: 1080px; padding-top: 1.5rem; padding-bottom: 4rem; }

    h1,h2,h3 { color:#352C3D; letter-spacing:-0.02em; }
    h1 { font-weight:850 !important; }
    h2,h3 { font-weight:780 !important; }
    p,li,label,.stMarkdown { color:#514859; }

    .vp-card {
        background:rgba(255,255,255,.92);
        border:1px solid rgba(154,133,170,.15);
        border-radius:22px;
        padding:20px 22px;
        box-shadow:0 10px 30px rgba(69,52,82,.05);
        margin:10px 0 16px;
    }
    .vp-card-title { font-weight:800; color:#3F3348; font-size:1.02rem; margin-bottom:5px; }
    .vp-card-copy { color:#746A7A; font-size:.91rem; line-height:1.5; }
    .vp-section-pill {
        display:inline-block;
        padding:6px 11px;
        border-radius:999px;
        background:#EFE8F6;
        color:#725A84;
        font-size:.72rem;
        font-weight:800;
        letter-spacing:.07em;
        text-transform:uppercase;
        margin-bottom:7px;
    }

    [data-testid="stChatMessage"] {
        border-radius:18px;
        padding:.45rem .55rem;
        margin-bottom:.55rem;
    }
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        background:linear-gradient(135deg,#F1EAF8,#F7F2FB);
        border:1px solid #E5D9EF;
    }
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        background:linear-gradient(135deg,#EEF6F9,#F7FBFC);
        border:1px solid #DDECF1;
    }
    [data-testid="stChatInput"] textarea {
        border-radius:16px !important;
        border:1px solid #D9CFDF !important;
        background:rgba(255,255,255,.96) !important;
    }

    div.stButton > button {
        border-radius:14px;
        min-height:2.85rem;
        font-weight:750;
        border:1px solid #DCCFE6;
        background:rgba(255,255,255,.95);
        color:#493B52;
        transition:all .15s ease;
    }
    div.stButton > button:hover {
        border-color:#9D7EB3;
        color:#4A3855;
        transform:translateY(-1px);
        box-shadow:0 7px 18px rgba(84,63,99,.08);
    }
    div.stButton > button[kind="primary"] {
        border:none !important;
        color:white !important;
        background:linear-gradient(135deg,#7E6096 0%,#5E8195 100%) !important;
        box-shadow:0 10px 24px rgba(91,69,110,.16);
    }

    div[data-baseweb="select"] > div,
    input, textarea { border-radius:13px !important; }

    div[data-baseweb="select"] > div,
    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea {
        border-color:#DDD3E4 !important;
        background:rgba(255,255,255,.96) !important;
    }

    div[data-testid="stAlert"] { border-radius:16px; border-width:1px; }

    details {
        background:rgba(255,255,255,.88);
        border:1px solid rgba(159,138,176,.15) !important;
        border-radius:16px !important;
        box-shadow:0 6px 18px rgba(69,52,82,.035);
        overflow:hidden;
    }
    details summary { font-weight:720 !important; color:#4A3B53 !important; }

    [data-testid="stMetric"] {
        background:rgba(255,255,255,.92);
        border:1px solid rgba(158,137,174,.14);
        border-radius:18px;
        padding:14px 16px;
        box-shadow:0 7px 22px rgba(69,52,82,.04);
    }
    [data-testid="stMetricLabel"] { color:#817486; font-weight:650; }
    [data-testid="stMetricValue"] { color:#3F3347; font-weight:850; }

    [data-baseweb="tab-list"] {
        gap:8px;
        background:rgba(239,233,244,.62);
        padding:6px;
        border-radius:15px;
    }
    [data-baseweb="tab"] { border-radius:11px; padding:8px 14px; }
    [aria-selected="true"][data-baseweb="tab"] {
        background:white;
        box-shadow:0 4px 12px rgba(65,51,78,.06);
    }

    hr {
        margin-top:1.7rem !important;
        margin-bottom:1.7rem !important;
        border-color:rgba(123,103,138,.12) !important;
    }

    [data-testid="stImage"] img {
        border-radius:18px;
        border:1px solid rgba(126,104,143,.12);
        box-shadow:0 10px 28px rgba(62,47,73,.07);
    }

    [data-testid="stDownloadButton"] button {
        border-radius:14px !important;
        font-weight:760 !important;
    }


    /* ---------- HISTORY QUESTION COMPOSER ---------- */
    .vp-question-label {
        color: #44384C;
        font-size: 0.92rem;
        font-weight: 800;
        margin: 0.25rem 0 0.45rem 0;
    }

    [data-testid="stTextArea"] textarea {
        color: #2F2933 !important;
        caret-color: #6F5483 !important;
        background: #FFFFFF !important;
        border: 1.5px solid #CDBFD8 !important;
        border-radius: 16px !important;
        font-size: 1rem !important;
        line-height: 1.45 !important;
        padding: 0.9rem 1rem !important;
        -webkit-text-fill-color: #2F2933 !important;
        opacity: 1 !important;
    }

    [data-testid="stTextArea"] textarea::placeholder {
        color: #9B909F !important;
        opacity: 1 !important;
        -webkit-text-fill-color: #9B909F !important;
    }

    [data-testid="stTextArea"] textarea:focus {
        border-color: #8E70A3 !important;
        box-shadow: 0 0 0 3px rgba(126, 96, 150, 0.12) !important;
        outline: none !important;
    }

    /* Prevent theme CSS from making typed form text invisible. */
    [data-testid="stTextInput"] input {
        color: #2F2933 !important;
        caret-color: #6F5483 !important;
        -webkit-text-fill-color: #2F2933 !important;
        opacity: 1 !important;
    }

    [data-testid="stTextInput"] input::placeholder {
        color: #9B909F !important;
        opacity: 1 !important;
    }

    @media (max-width:700px) {
        .block-container { padding-left:1rem; padding-right:1rem; }
        .vp-card { padding:16px 17px; border-radius:18px; }
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SHARED THEMES
# Every case has its own palette / aesthetic.
# =========================================================

THEMES = {
    "blush":       {"background": "#FFF8FC", "card": "#F7EAF4", "accent": "#A66C9D", "secondary": "#D9B8D3", "text": "#4A3547", "button": "#A66C9D"},
    "teal":        {"background": "#F4F8FA", "card": "#E3EEF1", "accent": "#315C66", "secondary": "#8FB5BD", "text": "#26383D", "button": "#315C66"},
    "sky":         {"background": "#F5FAFF", "card": "#E5F2FF", "accent": "#3D6E9E", "secondary": "#A8C8E8", "text": "#25384A", "button": "#3D6E9E"},
    "terracotta":  {"background": "#FFF8F4", "card": "#FBE9DE", "accent": "#A85D3C", "secondary": "#D9A48E", "text": "#4B342B", "button": "#A85D3C"},
    "violet":      {"background": "#FAF8FF", "card": "#EEE8FF", "accent": "#6D58A6", "secondary": "#B8A9DD", "text": "#39314D", "button": "#6D58A6"},
    "crimson":     {"background": "#FFF7F8", "card": "#FBE5E8", "accent": "#9C4050", "secondary": "#D7A3AC", "text": "#4B2B31", "button": "#9C4050"},
    "sage":        {"background": "#F8FBF6", "card": "#E7F0E1", "accent": "#5D7C55", "secondary": "#ACC2A2", "text": "#33432F", "button": "#5D7C55"},
    "amber":       {"background": "#FFFBF2", "card": "#F8EDCF", "accent": "#9A6A20", "secondary": "#D7BC7A", "text": "#4A3A20", "button": "#9A6A20"},
    "indigo":      {"background": "#F6F7FD", "card": "#E7E9F8", "accent": "#4F5D9A", "secondary": "#AAB1D5", "text": "#303651", "button": "#4F5D9A"},
    "mint":        {"background": "#F5FCFA", "card": "#DCF3EC", "accent": "#367D6A", "secondary": "#9ED3C4", "text": "#27483F", "button": "#367D6A"},
    "rose":        {"background": "#FFF7F9", "card": "#F9E4EA", "accent": "#A54864", "secondary": "#D9A0B0", "text": "#4C2E38", "button": "#A54864"},
    "slate":       {"background": "#F7F8FA", "card": "#E7EAEE", "accent": "#54606E", "secondary": "#B2BBC4", "text": "#30363D", "button": "#54606E"},
    "peach":       {"background": "#FFF9F5", "card": "#FBE6DA", "accent": "#B16945", "secondary": "#DDB096", "text": "#4C3428", "button": "#B16945"},
    "ocean":       {"background": "#F4FAFC", "card": "#DFF0F5", "accent": "#2D7184", "secondary": "#92C1CD", "text": "#24424A", "button": "#2D7184"},
    "plum":        {"background": "#FCF7FC", "card": "#F0E0F1", "accent": "#7B4B7D", "secondary": "#C5A4C6", "text": "#432F44", "button": "#7B4B7D"},
    "forest":      {"background": "#F6FAF6", "card": "#DDECDD", "accent": "#3E704A", "secondary": "#93B99B", "text": "#29402E", "button": "#3E704A"},
    "sand":        {"background": "#FCFAF4", "card": "#EFE8D6", "accent": "#8A6D3B", "secondary": "#C9B98E", "text": "#443A28", "button": "#8A6D3B"},
    "lavender":    {"background": "#FBF9FF", "card": "#ECE5FA", "accent": "#72579A", "secondary": "#B8A7D0", "text": "#3C324A", "button": "#72579A"},
    "aqua":        {"background": "#F5FCFC", "card": "#DDF2F1", "accent": "#3D7F7B", "secondary": "#9BC9C6", "text": "#294745", "button": "#3D7F7B"},
    "coral":       {"background": "#FFF8F6", "card": "#F9E3DD", "accent": "#A9584C", "secondary": "#D9A69D", "text": "#4A302C", "button": "#A9584C"},
    "bluegray":    {"background": "#F7F9FB", "card": "#E3EAF0", "accent": "#4B6C82", "secondary": "#A3BAC9", "text": "#2E3D47", "button": "#4B6C82"},
    "lemon":       {"background": "#FFFDF4", "card": "#F7F0C9", "accent": "#927827", "secondary": "#D5C778", "text": "#49401F", "button": "#927827"},
    "mulberry":    {"background": "#FCF7FA", "card": "#F1DEE8", "accent": "#814A68", "secondary": "#C29CB0", "text": "#442F3A", "button": "#814A68"},
    "ice":         {"background": "#F7FCFF", "card": "#E0F2FA", "accent": "#367795", "secondary": "#9ECADB", "text": "#29434E", "button": "#367795"},
    "olive":       {"background": "#FAFBF5", "card": "#E8ECD7", "accent": "#68763B", "secondary": "#B1BC83", "text": "#3B4028", "button": "#68763B"},
    "brick":       {"background": "#FFF8F6", "card": "#F2DED9", "accent": "#8C4A3C", "secondary": "#C99C92", "text": "#452E29", "button": "#8C4A3C"},
    "night":       {"background": "#F6F7FA", "card": "#E1E5ED", "accent": "#394B68", "secondary": "#98A5BA", "text": "#27303F", "button": "#394B68"},
    "orchid":      {"background": "#FDF8FF", "card": "#F0E2F4", "accent": "#824F91", "secondary": "#C3A4CC", "text": "#453149", "button": "#824F91"},
    "copper":      {"background": "#FFF9F5", "card": "#F1E2D7", "accent": "#8D6048", "secondary": "#C7A693", "text": "#49382F", "button": "#8D6048"},
    "seafoam":     {"background": "#F5FCF9", "card": "#DDF1E8", "accent": "#427967", "secondary": "#9BC6B7", "text": "#2B443B", "button": "#427967"},
    "berry":       {"background": "#FFF7FB", "card": "#F3E0EB", "accent": "#8C4B6B", "secondary": "#C7A1B4", "text": "#46313B", "button": "#8C4B6B"},
    "steel":       {"background": "#F7F9FA", "card": "#E3E8EA", "accent": "#526B73", "secondary": "#A4B7BC", "text": "#303C40", "button": "#526B73"},
}

# =========================================================
# DEFAULT RESPONSES
# Cases override the answers that matter.
# =========================================================

DEFAULT_RESPONSES = {
    "onset": ["I'm not completely sure when it started."],
    "location": ["It's hard to point to one exact place."],
    "severity": ["It's uncomfortable, but I'm not sure how to score it."],
    "character": ["It's difficult to describe."],
    "radiation": ["No, it doesn't really spread anywhere."],
    "aggravating": ["I haven't noticed anything in particular making it worse."],
    "relieving": ["Nothing seems to help much."],
    "breathlessness": ["No, I'm not short of breath."],
    "cough": ["No cough."],
    "sputum": ["No sputum."],
    "wheeze": ["No wheezing."],
    "chest_pain": ["No chest pain."],
    "palpitations": ["No palpitations."],
    "syncope": ["No, I haven't fainted."],
    "sweating": ["No unusual sweating."],
    "fever": ["I don't think I've had a fever."],
    "chills": ["No chills."],
    "nausea": ["No nausea."],
    "vomiting": ["No vomiting."],
    "appetite": ["My appetite is about normal."],
    "bowels": ["Nothing unusual with my bowels."],
    "diarrhea": ["No diarrhoea."],
    "constipation": ["No constipation."],
    "blood_stool": ["No blood in my stool."],
    "urine": ["No urinary problems."],
    "dysuria": ["No pain or burning when I pass urine."],
    "frequency": ["I'm not going more often than usual."],
    "hematuria": ["No blood in my urine."],
    "pregnancy": ["Pregnancy isn't relevant in my case."],
    "vaginal_bleeding": ["No vaginal bleeding."],
    "vaginal_discharge": ["No unusual discharge."],
    "lmp": ["My periods have been normal."],
    "headache": ["No headache."],
    "photophobia": ["Light doesn't bother me."],
    "vision": ["No changes in my vision."],
    "weakness": ["No weakness."],
    "numbness": ["No numbness or tingling."],
    "speech": ["No problems with my speech."],
    "seizure": ["No seizures."],
    "neck_stiffness": ["My neck doesn't feel stiff."],
    "rash": ["No rash."],
    "joint": ["No joint pain."],
    "swelling": ["I haven't noticed any swelling."],
    "leg_pain": ["No leg pain."],
    "weight_loss": ["No unexpected weight loss."],
    "thirst": ["I haven't been unusually thirsty."],
    "polyuria": ["I haven't been urinating more than usual."],
    "travel": ["No recent travel."],
    "immobilization": ["I haven't been stuck in bed or sitting for long periods recently."],
    "sick_contacts": ["No one close to me has been ill."],
    "medical_history": ["I'm usually healthy."],
    "surgery": ["I've never had any major surgery."],
    "medications": ["I don't take regular medication."],
    "allergies": ["No known allergies."],
    "smoking": ["I don't smoke."],
    "alcohol": ["I drink occasionally."],
    "recreational_drugs": ["No recreational drugs."],
    "family_history": ["Nothing important that I know of."],
}

# =========================================================
# PATIENT CASES
# 32 total: your original 2 + 30 more.
# =========================================================

CASES = {
    "Case 01 - Abdominal Pain": {
        "name": "Anna K.", "age": 24, "setting": "Emergency Department", "avatar": "🌸", "theme": "blush",
        "personality": {"anxiety": "high", "talkativeness": "medium", "style": "polite but visibly worried"},
        "chief_complaint": "I have really bad stomach pain.",
        "responses": {
            "onset": ["It started yesterday evening.", "Sometime last night."],
            "location": ["It started around my belly button, but now it's mostly on the lower right side."],
            "severity": ["About a 7 out of 10."],
            "character": ["It's sharp and constant."],
            "radiation": ["No, it doesn't really spread."],
            "aggravating": ["Moving around makes it worse."],
            "relieving": ["Nothing really helps."],
            "nausea": ["Yeah, I've felt pretty nauseous."],
            "vomiting": ["I vomited once this morning."],
            "appetite": ["I really don't want to eat."],
            "fever": ["I feel a bit feverish."],
            "bowels": ["Nothing unusual."],
            "urine": ["No urinary problems."],
            "pregnancy": ["No, I don't think I could be pregnant."],
            "lmp": ["My last period was about two weeks ago and was normal."],
            "medical_history": ["I'm normally healthy."],
            "surgery": ["I've never had surgery."],
            "medications": ["I don't take regular medication."],
            "allergies": ["No known allergies."],
            "smoking": ["No, I don't smoke."],
            "alcohol": ["Only socially."],
            "family_history": ["Nothing important that I know of."]
        },
        "required_topics": ["Onset","Site","Severity","Character","Aggravating factors","Nausea","Vomiting","Appetite","Fever","Bowel symptoms","Urinary symptoms","Pregnancy/LMP","Medical history","Medications","Allergies"],
        "diagnosis_keywords": ["appendicitis", "acute appendicitis"],
        "diagnosis_display": "Acute Appendicitis",
        "diagnosis_explanation": ["Migratory periumbilical to right lower quadrant pain", "Anorexia", "Nausea/vomiting", "Low-grade fever"]
    },

    "Case 02 - Chest Pain": {
        "name": "Michael T.", "age": 54, "setting": "Emergency Department", "avatar": "🧔🏻", "theme": "teal",
        "personality": {"anxiety": "medium", "talkativeness": "low", "style": "stoic and brief"},
        "chief_complaint": "I've got this pressure in my chest.",
        "responses": {
            "onset": ["It started about an hour ago, quite suddenly."],
            "location": ["Right in the middle of my chest."],
            "severity": ["About an 8 out of 10."],
            "character": ["It feels like a heavy crushing pressure."],
            "radiation": ["It goes into my left arm and a bit into my jaw."],
            "aggravating": ["Walking makes it worse."],
            "relieving": ["Stopping and resting hasn't completely taken it away."],
            "breathlessness": ["Yes, I'm a little short of breath."],
            "nausea": ["Yes, I feel nauseous."],
            "sweating": ["I've been sweating a lot."],
            "medical_history": ["I have high blood pressure and high cholesterol."],
            "medications": ["I take tablets for my blood pressure and cholesterol."],
            "allergies": ["No known allergies."],
            "smoking": ["Yes, about 10 cigarettes a day."],
            "alcohol": ["A few drinks on weekends."],
            "family_history": ["My dad had a heart attack in his early sixties."]
        },
        "required_topics": ["Onset","Site","Severity","Character","Radiation","Aggravating factors","Breathlessness","Nausea","Sweating","Medical history","Medications","Smoking","Family history"],
        "diagnosis_keywords": ["myocardial infarction", "heart attack", "stemi", "acute coronary syndrome", "acs"],
        "diagnosis_display": "Acute Myocardial Infarction",
        "diagnosis_explanation": ["Central crushing chest pressure", "Radiation to arm/jaw", "Autonomic symptoms", "Multiple cardiovascular risk factors"]
    },

    "Case 03 - Shortness of Breath": {
        "name": "Sofia M.", "age": 21, "setting": "Urgent Care", "avatar": "🫧", "theme": "sky",
        "personality": {"anxiety": "medium", "talkativeness": "medium", "style": "fast-talking between breaths"},
        "chief_complaint": "I can't seem to catch my breath.",
        "responses": {
            "onset": ["It started this afternoon and got worse over a few hours."],
            "severity": ["It's pretty bad right now."],
            "breathlessness": ["Yes, I feel tight and short of breath."],
            "wheeze": ["Yes, I've been wheezing."],
            "cough": ["A little dry cough."],
            "aggravating": ["Walking quickly makes it worse."],
            "relieving": ["My inhaler helped a bit, but not enough."],
            "medical_history": ["I've had asthma since I was a child."],
            "medications": ["I use a blue reliever inhaler when I need it."],
            "allergies": ["I'm allergic to cats and pollen."],
            "smoking": ["I don't smoke."]
        },
        "required_topics": ["Onset","Severity","Breathlessness","Wheeze","Cough","Aggravating factors","Relieving factors","Medical history","Medications","Allergies","Smoking"],
        "diagnosis_keywords": ["asthma", "asthma exacerbation", "acute asthma"],
        "diagnosis_display": "Acute Asthma Exacerbation",
        "diagnosis_explanation": ["Known asthma", "Wheeze and breathlessness", "Partial response to reliever inhaler", "Allergic background"]
    },

    "Case 04 - Fever and Cough": {
        "name": "Andreas P.", "age": 46, "setting": "Emergency Department", "avatar": "🧣", "theme": "terracotta",
        "personality": {"anxiety": "low", "talkativeness": "medium", "style": "tired and raspy"},
        "chief_complaint": "I've had a fever and a horrible cough for a few days.",
        "responses": {
            "onset": ["It started about four days ago."],
            "fever": ["Yes, I've had a high fever."],
            "chills": ["I've had shaking chills at night."],
            "cough": ["Yes, a deep cough."],
            "sputum": ["I'm bringing up yellow-green phlegm."],
            "breathlessness": ["I'm more short of breath than usual."],
            "chest_pain": ["It hurts on the right side when I take a deep breath."],
            "sick_contacts": ["My son had a cold last week."],
            "smoking": ["I used to smoke, but I quit five years ago."]
        },
        "required_topics": ["Onset","Fever","Chills","Cough","Sputum","Breathlessness","Chest pain","Sick contacts","Smoking"],
        "diagnosis_keywords": ["pneumonia", "community acquired pneumonia", "cap"],
        "diagnosis_display": "Community-Acquired Pneumonia",
        "diagnosis_explanation": ["Fever and rigors", "Productive cough", "Pleuritic chest pain", "Breathlessness"]
    },

    "Case 05 - Sudden Breathlessness": {
        "name": "Elena V.", "age": 37, "setting": "Emergency Department", "avatar": "🧳", "theme": "violet",
        "personality": {"anxiety": "high", "talkativeness": "low", "style": "frightened and concise"},
        "chief_complaint": "I suddenly became really short of breath.",
        "responses": {
            "onset": ["It started suddenly about two hours ago."],
            "breathlessness": ["Yes, very suddenly."],
            "chest_pain": ["I have a sharp pain on the right side when I breathe in."],
            "leg_pain": ["My left calf has been sore since yesterday."],
            "swelling": ["My left calf looks a little swollen."],
            "travel": ["I flew back from New York yesterday."],
            "immobilization": ["I was sitting on the plane for about nine hours."],
            "medications": ["I'm on the combined contraceptive pill."],
            "smoking": ["I smoke occasionally."]
        },
        "required_topics": ["Onset","Breathlessness","Chest pain","Leg pain","Swelling","Travel","Immobilization","Medications","Smoking"],
        "diagnosis_keywords": ["pulmonary embolism", "pe"],
        "diagnosis_display": "Pulmonary Embolism",
        "diagnosis_explanation": ["Sudden dyspnoea", "Pleuritic chest pain", "Calf symptoms", "Recent long-haul travel", "Oestrogen exposure"]
    },

    "Case 06 - Recurrent Headache": {
        "name": "Nikos D.", "age": 29, "setting": "Primary Care", "avatar": "🎧", "theme": "indigo",
        "personality": {"anxiety": "low", "talkativeness": "medium", "style": "calm and descriptive"},
        "chief_complaint": "I've got another one of these awful headaches.",
        "responses": {
            "onset": ["It built up over about half an hour."],
            "location": ["Mostly on the left side of my head."],
            "severity": ["About an 8 out of 10."],
            "character": ["It's throbbing."],
            "headache": ["It's one-sided and pounding."],
            "photophobia": ["Yes, bright light is horrible."],
            "vision": ["Before it starts I see zig-zag lights for about 20 minutes."],
            "nausea": ["I feel nauseous with it."],
            "family_history": ["My mum gets migraines too."]
        },
        "required_topics": ["Onset","Site","Severity","Character","Headache features","Photophobia","Vision","Nausea","Family history"],
        "diagnosis_keywords": ["migraine", "migraine with aura"],
        "diagnosis_display": "Migraine with Aura",
        "diagnosis_explanation": ["Unilateral throbbing headache", "Visual aura", "Photophobia", "Nausea", "Family history"]
    },

    "Case 07 - Sudden Severe Headache": {
        "name": "Maria S.", "age": 43, "setting": "Emergency Department", "avatar": "⚡", "theme": "crimson",
        "personality": {"anxiety": "high", "talkativeness": "low", "style": "distressed and fearful"},
        "chief_complaint": "This is the worst headache I've ever had.",
        "responses": {
            "onset": ["It hit me suddenly, within seconds."],
            "severity": ["Ten out of ten."],
            "headache": ["It was like being hit in the head."],
            "neck_stiffness": ["My neck feels really stiff."],
            "nausea": ["Yes, I'm very nauseous."],
            "vomiting": ["I vomited once."],
            "photophobia": ["The light bothers me."],
            "weakness": ["No weakness that I've noticed."],
            "seizure": ["No seizures."]
        },
        "required_topics": ["Onset","Severity","Headache features","Neck stiffness","Nausea","Vomiting","Photophobia","Weakness","Seizure"],
        "diagnosis_keywords": ["subarachnoid hemorrhage", "subarachnoid haemorrhage", "sah"],
        "diagnosis_display": "Subarachnoid Haemorrhage",
        "diagnosis_explanation": ["Thunderclap onset", "Worst-ever headache", "Neck stiffness", "Vomiting and photophobia"]
    },

    "Case 08 - Sudden Weakness": {
        "name": "George L.", "age": 68, "setting": "Emergency Department", "avatar": "🧓🏻", "theme": "slate",
        "personality": {"anxiety": "medium", "talkativeness": "low", "style": "frustrated because speech is difficult"},
        "chief_complaint": "My right arm suddenly went weak.",
        "responses": {
            "onset": ["It started suddenly about 45 minutes ago."],
            "weakness": ["My right arm and leg feel weak."],
            "numbness": ["The right side feels a bit numb too."],
            "speech": ["My wife says my speech became slurred."],
            "vision": ["No major change in my vision."],
            "headache": ["No headache."],
            "medical_history": ["I have atrial fibrillation and high blood pressure."],
            "medications": ["I take blood pressure tablets, but I stopped my blood thinner a month ago."]
        },
        "required_topics": ["Onset","Weakness","Numbness","Speech","Vision","Headache features","Medical history","Medications"],
        "diagnosis_keywords": ["stroke", "ischemic stroke", "ischaemic stroke", "cva"],
        "diagnosis_display": "Acute Ischaemic Stroke",
        "diagnosis_explanation": ["Sudden focal weakness", "Sensory change", "Dysarthria", "Atrial fibrillation", "Anticoagulation interruption"]
    },

    "Case 09 - Fever and Flank Pain": {
        "name": "Eleni R.", "age": 31, "setting": "Emergency Department", "avatar": "🌿", "theme": "sage",
        "personality": {"anxiety": "medium", "talkativeness": "medium", "style": "uncomfortable but cooperative"},
        "chief_complaint": "I've got pain in my side and a fever.",
        "responses": {
            "onset": ["It started two days ago."],
            "location": ["It's in my left side, around my back."],
            "severity": ["About a 7 out of 10."],
            "fever": ["Yes, I've had a fever."],
            "chills": ["I've had chills and shaking."],
            "dysuria": ["It burns when I pee."],
            "frequency": ["I'm going much more often than usual."],
            "nausea": ["I feel nauseous."],
            "pregnancy": ["No, I'm not pregnant."]
        },
        "required_topics": ["Onset","Site","Severity","Fever","Chills","Dysuria","Urinary frequency","Nausea","Pregnancy/LMP"],
        "diagnosis_keywords": ["pyelonephritis", "kidney infection"],
        "diagnosis_display": "Acute Pyelonephritis",
        "diagnosis_explanation": ["Flank pain", "Fever and rigors", "Dysuria", "Urinary frequency", "Nausea"]
    },

    "Case 10 - Colicky Flank Pain": {
        "name": "Christos A.", "age": 35, "setting": "Emergency Department", "avatar": "🪨", "theme": "amber",
        "personality": {"anxiety": "high", "talkativeness": "low", "style": "restless and unable to sit still"},
        "chief_complaint": "I've got unbearable pain in my side.",
        "responses": {
            "onset": ["It started suddenly this morning."],
            "location": ["It starts in my right flank."],
            "severity": ["Nine out of ten."],
            "character": ["It comes in waves."],
            "radiation": ["It travels down toward my groin."],
            "hematuria": ["I noticed a bit of blood in my urine."],
            "nausea": ["Yes, I feel sick."],
            "vomiting": ["I vomited once."],
            "fever": ["No fever."]
        },
        "required_topics": ["Onset","Site","Severity","Character","Radiation","Haematuria","Nausea","Vomiting","Fever"],
        "diagnosis_keywords": ["renal colic", "kidney stone", "ureteric stone", "nephrolithiasis"],
        "diagnosis_display": "Renal Colic due to Ureteric Stone",
        "diagnosis_explanation": ["Severe colicky flank pain", "Radiation to groin", "Haematuria", "Nausea/vomiting", "No fever"]
    },

    "Case 11 - Right Upper Abdominal Pain": {
        "name": "Danae K.", "age": 42, "setting": "Emergency Department", "avatar": "🍋", "theme": "lemon",
        "personality": {"anxiety": "medium", "talkativeness": "medium", "style": "irritable from pain"},
        "chief_complaint": "I've got pain under my right ribs.",
        "responses": {
            "onset": ["It started last night after dinner."],
            "location": ["Under my right ribs."],
            "severity": ["About a 7 out of 10."],
            "character": ["It's a steady aching pain."],
            "radiation": ["It goes to my right shoulder blade."],
            "aggravating": ["Food, especially fatty food, seems to make it worse."],
            "fever": ["I feel feverish."],
            "nausea": ["Yes, I feel nauseous."],
            "vomiting": ["I vomited once."]
        },
        "required_topics": ["Onset","Site","Severity","Character","Radiation","Aggravating factors","Fever","Nausea","Vomiting"],
        "diagnosis_keywords": ["cholecystitis", "acute cholecystitis"],
        "diagnosis_display": "Acute Cholecystitis",
        "diagnosis_explanation": ["Right upper quadrant pain", "Radiation to right scapula", "Post-prandial worsening", "Fever", "Nausea/vomiting"]
    },

    "Case 12 - Severe Epigastric Pain": {
        "name": "Petros N.", "age": 49, "setting": "Emergency Department", "avatar": "🥃", "theme": "copper",
        "personality": {"anxiety": "medium", "talkativeness": "medium", "style": "guarded and slightly embarrassed"},
        "chief_complaint": "I've got severe pain at the top of my stomach.",
        "responses": {
            "onset": ["It started early this morning."],
            "location": ["Right in the upper middle of my abdomen."],
            "severity": ["Eight out of ten."],
            "character": ["It's deep and constant."],
            "radiation": ["It goes straight through to my back."],
            "nausea": ["Yes."],
            "vomiting": ["I've vomited three times."],
            "alcohol": ["I drink most evenings, probably more than I should."],
            "medical_history": ["I've had high triglycerides before."]
        },
        "required_topics": ["Onset","Site","Severity","Character","Radiation","Nausea","Vomiting","Alcohol","Medical history"],
        "diagnosis_keywords": ["pancreatitis", "acute pancreatitis"],
        "diagnosis_display": "Acute Pancreatitis",
        "diagnosis_explanation": ["Severe epigastric pain radiating to back", "Persistent vomiting", "Alcohol excess", "Hypertriglyceridaemia history"]
    },

    "Case 13 - Black Stools": {
        "name": "Katerina F.", "age": 57, "setting": "Emergency Department", "avatar": "☕", "theme": "sand",
        "personality": {"anxiety": "medium", "talkativeness": "medium", "style": "concerned but composed"},
        "chief_complaint": "My stools have turned black and I feel dizzy.",
        "responses": {
            "onset": ["The black stools started yesterday."],
            "blood_stool": ["They're black, sticky and really dark."],
            "syncope": ["I haven't fainted, but I nearly did when I stood up."],
            "nausea": ["A little."],
            "vomiting": ["No vomiting."],
            "medical_history": ["I have arthritis."],
            "medications": ["I take ibuprofen most days for my knees."],
            "alcohol": ["A glass or two of wine most evenings."]
        },
        "required_topics": ["Onset","Blood in stool","Syncope","Nausea","Vomiting","Medical history","Medications","Alcohol"],
        "diagnosis_keywords": ["upper gi bleed", "upper gastrointestinal bleed", "peptic ulcer", "gi bleed", "gastrointestinal bleed"],
        "diagnosis_display": "Upper Gastrointestinal Bleed, likely Peptic Ulcer",
        "diagnosis_explanation": ["Melena", "Postural presyncope", "Regular NSAID use", "Compatible ulcer risk profile"]
    },

    "Case 14 - Chronic Diarrhoea": {
        "name": "Alex B.", "age": 26, "setting": "Gastroenterology Clinic", "avatar": "🌱", "theme": "forest",
        "personality": {"anxiety": "low", "talkativeness": "high", "style": "open and detailed"},
        "chief_complaint": "I've had diarrhoea and stomach cramps for weeks.",
        "responses": {
            "onset": ["It's been getting worse over about six weeks."],
            "location": ["Mostly cramping on the lower right side."],
            "diarrhea": ["About five or six loose stools a day."],
            "blood_stool": ["Sometimes there's a little blood."],
            "weight_loss": ["I've lost about five kilos without trying."],
            "appetite": ["My appetite isn't great."],
            "fever": ["Sometimes I feel a bit feverish."],
            "family_history": ["My aunt has Crohn's disease."]
        },
        "required_topics": ["Onset","Site","Diarrhoea","Blood in stool","Weight loss","Appetite","Fever","Family history"],
        "diagnosis_keywords": ["crohn", "crohn's disease", "crohns disease"],
        "diagnosis_display": "Crohn's Disease",
        "diagnosis_explanation": ["Chronic diarrhoea", "Right lower quadrant pain", "Weight loss", "Intermittent blood", "Family history"]
    },

    "Case 15 - Bloody Diarrhoea": {
        "name": "Irene H.", "age": 33, "setting": "Gastroenterology Clinic", "avatar": "🍒", "theme": "berry",
        "personality": {"anxiety": "medium", "talkativeness": "medium", "style": "matter-of-fact but tired"},
        "chief_complaint": "I've been passing blood with diarrhoea.",
        "responses": {
            "onset": ["It's been going on for about three weeks."],
            "diarrhea": ["I'm going eight or nine times a day."],
            "blood_stool": ["There's bright red blood mixed in."],
            "location": ["I get cramping low down in my abdomen."],
            "weight_loss": ["I've lost around three kilos."],
            "fever": ["I've had a low fever a few times."],
            "family_history": ["No inflammatory bowel disease in the family."]
        },
        "required_topics": ["Onset","Diarrhoea","Blood in stool","Site","Weight loss","Fever","Family history"],
        "diagnosis_keywords": ["ulcerative colitis", "uc"],
        "diagnosis_display": "Ulcerative Colitis Flare",
        "diagnosis_explanation": ["Frequent bloody diarrhoea", "Lower abdominal cramps", "Weight loss", "Systemic symptoms"]
    },

    "Case 16 - Thirst and Vomiting": {
        "name": "Leon G.", "age": 19, "setting": "Emergency Department", "avatar": "💧", "theme": "aqua",
        "personality": {"anxiety": "medium", "talkativeness": "low", "style": "exhausted and slow"},
        "chief_complaint": "I'm really thirsty, sick, and exhausted.",
        "responses": {
            "onset": ["I've felt worse over the last two days."],
            "thirst": ["I'm constantly thirsty."],
            "polyuria": ["I'm peeing all the time."],
            "nausea": ["Yes, badly."],
            "vomiting": ["I've vomited several times."],
            "weight_loss": ["I've lost about six kilos in a month."],
            "medical_history": ["I have type 1 diabetes."],
            "medications": ["I use insulin, but I've missed a few doses this week."],
            "breathlessness": ["I feel like I'm breathing really deeply and quickly."]
        },
        "required_topics": ["Onset","Thirst","Polyuria","Nausea","Vomiting","Weight loss","Medical history","Medications","Breathlessness"],
        "diagnosis_keywords": ["dka", "diabetic ketoacidosis", "ketoacidosis"],
        "diagnosis_display": "Diabetic Ketoacidosis",
        "diagnosis_explanation": ["Type 1 diabetes", "Missed insulin", "Polyuria/polydipsia", "Vomiting", "Weight loss", "Deep rapid breathing"]
    },

    "Case 17 - Confusion and Sweating": {
        "name": "Eva C.", "age": 63, "setting": "Emergency Department", "avatar": "🍬", "theme": "peach",
        "personality": {"anxiety": "low", "talkativeness": "low", "style": "confused and shaky"},
        "chief_complaint": "I suddenly felt shaky, sweaty and confused.",
        "responses": {
            "onset": ["It came on suddenly about 20 minutes ago."],
            "sweating": ["Yes, I was drenched in sweat."],
            "palpitations": ["My heart was racing."],
            "weakness": ["I felt weak all over."],
            "medical_history": ["I have type 2 diabetes."],
            "medications": ["I take insulin with meals."],
            "appetite": ["I skipped lunch today."]
        },
        "required_topics": ["Onset","Sweating","Palpitations","Weakness","Medical history","Medications","Appetite"],
        "diagnosis_keywords": ["hypoglycemia", "hypoglycaemia", "low blood sugar"],
        "diagnosis_display": "Hypoglycaemia",
        "diagnosis_explanation": ["Sudden adrenergic symptoms", "Confusion", "Insulin use", "Missed meal"]
    },

    "Case 18 - Palpitations and Weight Loss": {
        "name": "Yiannis M.", "age": 28, "setting": "Endocrine Clinic", "avatar": "🔥", "theme": "coral",
        "personality": {"anxiety": "high", "talkativeness": "high", "style": "restless and energetic"},
        "chief_complaint": "My heart keeps racing and I'm losing weight.",
        "responses": {
            "onset": ["It's been building up over about two months."],
            "palpitations": ["Yes, my heart races even when I'm sitting."],
            "weight_loss": ["I've lost seven kilos even though I'm eating more."],
            "appetite": ["I'm hungry all the time."],
            "sweating": ["I'm constantly hot and sweaty."],
            "bowels": ["I've been going more often than usual."],
            "medical_history": ["No major health problems."],
            "family_history": ["My mother has thyroid disease."]
        },
        "required_topics": ["Onset","Palpitations","Weight loss","Appetite","Sweating","Bowel symptoms","Family history"],
        "diagnosis_keywords": ["hyperthyroidism", "thyrotoxicosis", "graves"],
        "diagnosis_display": "Hyperthyroidism",
        "diagnosis_explanation": ["Palpitations", "Weight loss despite increased appetite", "Heat intolerance/sweating", "Increased bowel frequency", "Family thyroid history"]
    },

    "Case 19 - Tiredness and Weight Gain": {
        "name": "Marina O.", "age": 45, "setting": "Primary Care", "avatar": "🧶", "theme": "lavender",
        "personality": {"anxiety": "low", "talkativeness": "medium", "style": "quiet and fatigued"},
        "chief_complaint": "I'm exhausted all the time and I've been gaining weight.",
        "responses": {
            "onset": ["It's been gradual over six months."],
            "weight_loss": ["Actually, I've gained about eight kilos."],
            "appetite": ["My appetite is normal."],
            "constipation": ["Yes, I've become quite constipated."],
            "medical_history": ["I have vitiligo."],
            "family_history": ["My sister has Hashimoto's thyroiditis."],
            "character": ["I feel slow, cold and tired most of the day."]
        },
        "required_topics": ["Onset","Character","Constipation","Medical history","Family history"],
        "diagnosis_keywords": ["hypothyroidism", "hashimoto", "hashimoto's"],
        "diagnosis_display": "Hypothyroidism",
        "diagnosis_explanation": ["Fatigue", "Weight gain", "Constipation", "Autoimmune background", "Family history"]
    },

    "Case 20 - Fatigue and Breathlessness": {
        "name": "Thomas J.", "age": 39, "setting": "Primary Care", "avatar": "📚", "theme": "bluegray",
        "personality": {"anxiety": "low", "talkativeness": "medium", "style": "calm but frustrated"},
        "chief_complaint": "I'm tired all the time and get breathless on stairs.",
        "responses": {
            "onset": ["It's been getting worse for a few months."],
            "breathlessness": ["Mostly when I climb stairs."],
            "palpitations": ["Sometimes my heart races when I exert myself."],
            "appetite": ["My appetite is okay."],
            "blood_stool": ["No visible blood in my stool."],
            "medical_history": ["I have chronic gastritis."],
            "medications": ["I take omeprazole regularly."]
        },
        "required_topics": ["Onset","Breathlessness","Palpitations","Appetite","Blood in stool","Medical history","Medications"],
        "diagnosis_keywords": ["iron deficiency anemia", "iron deficiency anaemia", "anemia", "anaemia"],
        "diagnosis_display": "Iron Deficiency Anaemia",
        "diagnosis_explanation": ["Progressive fatigue", "Exertional dyspnoea", "Palpitations", "Possible chronic GI iron loss/malabsorption context"]
    },

    "Case 21 - Sudden Rash and Breathing Difficulty": {
        "name": "Chloe E.", "age": 23, "setting": "Emergency Department", "avatar": "🥜", "theme": "rose",
        "personality": {"anxiety": "high", "talkativeness": "low", "style": "panicked and breathless"},
        "chief_complaint": "My throat feels tight and I'm covered in a rash.",
        "responses": {
            "onset": ["It started within minutes of eating dessert."],
            "breathlessness": ["Yes, my throat feels tight and breathing feels difficult."],
            "rash": ["I've got itchy raised welts all over."],
            "swelling": ["My lips feel swollen."],
            "nausea": ["I feel sick."],
            "allergies": ["I'm allergic to peanuts."],
            "medical_history": ["I have asthma."]
        },
        "required_topics": ["Onset","Breathlessness","Rash","Swelling","Nausea","Allergies","Medical history"],
        "diagnosis_keywords": ["anaphylaxis", "anaphylactic reaction"],
        "diagnosis_display": "Anaphylaxis",
        "diagnosis_explanation": ["Rapid onset after likely allergen exposure", "Airway/breathing symptoms", "Urticarial rash", "Lip swelling", "Known peanut allergy"]
    },

    "Case 22 - Fever, Headache and Stiff Neck": {
        "name": "Stefanos Q.", "age": 20, "setting": "Emergency Department", "avatar": "🧊", "theme": "ice",
        "personality": {"anxiety": "medium", "talkativeness": "low", "style": "drowsy and irritable"},
        "chief_complaint": "My head is killing me and my neck is stiff.",
        "responses": {
            "onset": ["It started yesterday and got much worse overnight."],
            "fever": ["Yes, I've had a high fever."],
            "headache": ["It's severe and all over my head."],
            "neck_stiffness": ["Yes, my neck is very stiff."],
            "photophobia": ["The light really hurts my eyes."],
            "vomiting": ["I've vomited twice."],
            "rash": ["I haven't noticed a rash."],
            "sick_contacts": ["One person in my university residence was sick recently."]
        },
        "required_topics": ["Onset","Fever","Headache features","Neck stiffness","Photophobia","Vomiting","Rash","Sick contacts"],
        "diagnosis_keywords": ["meningitis", "bacterial meningitis"],
        "diagnosis_display": "Acute Meningitis",
        "diagnosis_explanation": ["Fever", "Severe headache", "Neck stiffness", "Photophobia", "Vomiting", "Possible exposure"]
    },

    "Case 23 - Sore Throat and Fatigue": {
        "name": "Zoe I.", "age": 18, "setting": "Primary Care", "avatar": "🫖", "theme": "mint",
        "personality": {"anxiety": "low", "talkativeness": "high", "style": "chatty but exhausted"},
        "chief_complaint": "My throat hurts and I'm unbelievably tired.",
        "responses": {
            "onset": ["It's been about a week."],
            "fever": ["I've had a mild fever."],
            "appetite": ["Eating hurts because my throat is sore."],
            "medical_history": ["I'm normally healthy."],
            "sick_contacts": ["A few people at university have been ill."],
            "character": ["My throat is very sore and my neck glands feel swollen."],
            "rash": ["No rash."]
        },
        "required_topics": ["Onset","Fever","Appetite","Character","Sick contacts","Rash"],
        "diagnosis_keywords": ["infectious mononucleosis", "mononucleosis", "glandular fever", "ebv"],
        "diagnosis_display": "Infectious Mononucleosis",
        "diagnosis_explanation": ["Prolonged sore throat", "Marked fatigue", "Fever", "Cervical lymph node symptoms", "Young adult setting"]
    },

    "Case 24 - Spinning Dizziness": {
        "name": "Dimitra W.", "age": 52, "setting": "Primary Care", "avatar": "🎠", "theme": "orchid",
        "personality": {"anxiety": "medium", "talkativeness": "medium", "style": "careful and descriptive"},
        "chief_complaint": "The room spins whenever I turn my head.",
        "responses": {
            "onset": ["It started three days ago."],
            "character": ["It feels like the whole room is spinning."],
            "aggravating": ["Rolling over in bed or looking up triggers it."],
            "relieving": ["If I keep still, it settles within less than a minute."],
            "nausea": ["I feel nauseous during the spinning."],
            "vomiting": ["No vomiting."],
            "weakness": ["No weakness."],
            "speech": ["No speech problems."],
            "vision": ["No double vision."]
        },
        "required_topics": ["Onset","Character","Aggravating factors","Relieving factors","Nausea","Vomiting","Weakness","Speech","Vision"],
        "diagnosis_keywords": ["bppv", "benign paroxysmal positional vertigo", "positional vertigo"],
        "diagnosis_display": "Benign Paroxysmal Positional Vertigo",
        "diagnosis_explanation": ["Brief spinning episodes", "Triggered by head position", "Settles with stillness", "No focal neurological symptoms"]
    },

    "Case 25 - Red Painful Leg": {
        "name": "Dimitris Y.", "age": 61, "setting": "Urgent Care", "avatar": "🧦", "theme": "brick",
        "personality": {"anxiety": "low", "talkativeness": "low", "style": "practical and blunt"},
        "chief_complaint": "My lower leg is red, hot and painful.",
        "responses": {
            "onset": ["It started two days ago."],
            "location": ["It's my left lower leg."],
            "severity": ["About a 6 out of 10."],
            "fever": ["I've had a mild fever."],
            "swelling": ["Yes, it's swollen."],
            "rash": ["The skin is red and warm, not really a rash."],
            "medical_history": ["I have type 2 diabetes."],
            "surgery": ["No recent surgery."]
        },
        "required_topics": ["Onset","Site","Severity","Fever","Swelling","Rash","Medical history","Surgical history"],
        "diagnosis_keywords": ["cellulitis"],
        "diagnosis_display": "Cellulitis",
        "diagnosis_explanation": ["Acute unilateral erythema", "Warmth and swelling", "Pain", "Fever", "Diabetes as risk factor"]
    },

    "Case 26 - Sudden Hot Joint": {
        "name": "Manolis Z.", "age": 58, "setting": "Urgent Care", "avatar": "🦶", "theme": "olive",
        "personality": {"anxiety": "low", "talkativeness": "medium", "style": "grumpy because of pain"},
        "chief_complaint": "My big toe is killing me.",
        "responses": {
            "onset": ["It started suddenly in the middle of the night."],
            "location": ["The base of my right big toe."],
            "severity": ["Nine out of ten."],
            "joint": ["It's red, hot, swollen and incredibly tender."],
            "aggravating": ["Even the bedsheet touching it hurts."],
            "alcohol": ["I had quite a lot of beer at a barbecue yesterday."],
            "medical_history": ["I have high blood pressure."],
            "medications": ["I take a thiazide water tablet."]
        },
        "required_topics": ["Onset","Site","Severity","Joint symptoms","Aggravating factors","Alcohol","Medical history","Medications"],
        "diagnosis_keywords": ["gout", "acute gout"],
        "diagnosis_display": "Acute Gout",
        "diagnosis_explanation": ["Acute first-MTP monoarthritis", "Extreme tenderness", "Erythema/swelling", "Alcohol trigger", "Thiazide use"]
    },

    "Case 27 - Lower Abdominal Pain and Bleeding": {
        "name": "Lydia P.", "age": 27, "setting": "Emergency Department", "avatar": "🌙", "theme": "mulberry",
        "personality": {"anxiety": "high", "talkativeness": "medium", "style": "scared and hesitant"},
        "chief_complaint": "I've got lower stomach pain and some bleeding.",
        "responses": {
            "onset": ["The pain started this morning."],
            "location": ["Mostly on the left lower side."],
            "severity": ["About a 7 out of 10."],
            "character": ["It's a sharp pain."],
            "vaginal_bleeding": ["I've had light vaginal bleeding since yesterday."],
            "lmp": ["My last period was about seven weeks ago."],
            "pregnancy": ["I took a home pregnancy test yesterday and it was positive."],
            "syncope": ["I felt very dizzy earlier but didn't fully faint."],
            "shoulder_tip": ["I noticed an ache at the tip of my left shoulder."]
        },
        "required_topics": ["Onset","Site","Severity","Character","Vaginal bleeding","Pregnancy/LMP","Syncope","Shoulder-tip pain"],
        "diagnosis_keywords": ["ectopic pregnancy", "ectopic"],
        "diagnosis_display": "Ectopic Pregnancy",
        "diagnosis_explanation": ["Positive pregnancy test", "Amenorrhoea", "Unilateral pelvic pain", "Vaginal bleeding", "Presyncope/shoulder-tip pain"]
    },

    "Case 28 - Sudden Testicular Pain": {
        "name": "Panos U.", "age": 17, "setting": "Emergency Department", "avatar": "⚽", "theme": "steel",
        "personality": {"anxiety": "high", "talkativeness": "low", "style": "embarrassed and distressed"},
        "chief_complaint": "I've got sudden severe pain in my testicle.",
        "responses": {
            "onset": ["It started suddenly about two hours ago."],
            "location": ["It's my left testicle."],
            "severity": ["Ten out of ten."],
            "character": ["It's constant and severe."],
            "nausea": ["Yes, I feel sick."],
            "vomiting": ["I vomited once."],
            "urine": ["No urinary symptoms."],
            "fever": ["No fever."],
            "medical_history": ["I'm normally healthy."]
        },
        "required_topics": ["Onset","Site","Severity","Character","Nausea","Vomiting","Urinary symptoms","Fever","Medical history"],
        "diagnosis_keywords": ["testicular torsion", "torsion"],
        "diagnosis_display": "Testicular Torsion",
        "diagnosis_explanation": ["Sudden severe unilateral testicular pain", "Nausea/vomiting", "No urinary symptoms", "Adolescent age group"]
    },

    "Case 29 - Racing Heart and Tingling": {
        "name": "Alexandra C.", "age": 25, "setting": "Emergency Department", "avatar": "🫀", "theme": "seafoam",
        "personality": {"anxiety": "very high", "talkativeness": "high", "style": "rapid speech and visibly panicked"},
        "chief_complaint": "My heart is racing and I feel like I can't breathe.",
        "responses": {
            "onset": ["It came on suddenly about 15 minutes ago."],
            "palpitations": ["Yes, my heart feels like it's pounding."],
            "breathlessness": ["I feel like I can't get enough air."],
            "chest_pain": ["There's a tight feeling in my chest."],
            "numbness": ["My fingers and lips are tingling."],
            "syncope": ["I feel light-headed but haven't fainted."],
            "medical_history": ["I've had a few similar episodes during stressful periods."],
            "recreational_drugs": ["No drugs."],
            "smoking": ["I don't smoke."]
        },
        "required_topics": ["Onset","Palpitations","Breathlessness","Chest pain","Numbness","Syncope","Medical history","Recreational drugs","Smoking"],
        "diagnosis_keywords": ["panic attack", "panic disorder"],
        "diagnosis_display": "Panic Attack",
        "diagnosis_explanation": ["Abrupt panic symptoms", "Palpitations and dyspnoea", "Perioral/finger tingling", "Prior similar stress-related episodes", "No substance trigger"]
    },

    "Case 30 - Facial Weakness": {
        "name": "Olivia N.", "age": 34, "setting": "Urgent Care", "avatar": "🪞", "theme": "plum",
        "personality": {"anxiety": "medium", "talkativeness": "medium", "style": "worried but focused"},
        "chief_complaint": "One side of my face suddenly stopped moving properly.",
        "responses": {
            "onset": ["I noticed it when I woke up this morning."],
            "weakness": ["The whole left side of my face feels weak."],
            "speech": ["My speech sounds a little odd because my mouth droops, but I can find my words normally."],
            "vision": ["My left eye feels dry because I can't close it fully."],
            "numbness": ["It doesn't really feel numb."],
            "weakness_limb": ["My arms and legs are completely normal."],
            "headache": ["No headache."],
            "medical_history": ["I had a cold last week."]
        },
        "required_topics": ["Onset","Facial weakness","Speech","Vision","Numbness","Limb weakness","Headache features","Medical history"],
        "diagnosis_keywords": ["bell's palsy", "bells palsy", "facial nerve palsy"],
        "diagnosis_display": "Bell's Palsy",
        "diagnosis_explanation": ["Acute unilateral complete facial weakness", "Impaired eye closure", "No limb weakness", "No cortical speech deficit", "Recent viral illness"]
    },

    "Case 31 - Jaw Pain and Headache": {
        "name": "Markos T.", "age": 72, "setting": "Emergency Assessment Unit", "avatar": "🕰️", "theme": "night",
        "personality": {"anxiety": "low", "talkativeness": "medium", "style": "measured and serious"},
        "chief_complaint": "I've had a new headache and my jaw hurts when I chew.",
        "responses": {
            "onset": ["It started about ten days ago."],
            "location": ["Mostly over my right temple."],
            "severity": ["About a 6 out of 10."],
            "headache": ["It's a new, persistent ache over my temple."],
            "vision": ["Yesterday my vision went blurry for a few minutes."],
            "character": ["My scalp is tender when I brush my hair."],
            "jaw_claudication": ["My jaw starts aching after chewing for a little while."],
            "weight_loss": ["I've lost a few kilos and haven't felt hungry."]
        },
        "required_topics": ["Onset","Site","Severity","Headache features","Vision","Character","Jaw claudication","Weight loss"],
        "diagnosis_keywords": ["giant cell arteritis", "temporal arteritis", "gca"],
        "diagnosis_display": "Giant Cell Arteritis",
        "diagnosis_explanation": ["New temporal headache in older adult", "Scalp tenderness", "Jaw claudication", "Transient visual symptoms", "Constitutional symptoms"]
    },

    "Case 32 - Swollen Painful Calf": {
        "name": "Rania X.", "age": 48, "setting": "Urgent Care", "avatar": "🧳", "theme": "ocean",
        "personality": {"anxiety": "medium", "talkativeness": "medium", "style": "concerned and practical"},
        "chief_complaint": "My calf has become swollen and painful.",
        "responses": {
            "onset": ["It started yesterday."],
            "location": ["My right calf."],
            "severity": ["About a 5 out of 10."],
            "swelling": ["Yes, the right calf is definitely more swollen."],
            "leg_pain": ["It's tender and aches when I walk."],
            "travel": ["I came back from a seven-hour coach journey two days ago."],
            "immobilization": ["I was sitting almost the whole journey."],
            "breathlessness": ["No shortness of breath."],
            "chest_pain": ["No chest pain."],
            "medical_history": ["I had breast cancer three years ago and finished treatment."]
        },
        "required_topics": ["Onset","Site","Severity","Swelling","Leg pain","Travel","Immobilization","Breathlessness","Chest pain","Medical history"],
        "diagnosis_keywords": ["deep vein thrombosis", "dvt"],
        "diagnosis_display": "Deep Vein Thrombosis",
        "diagnosis_explanation": ["Unilateral calf swelling", "Calf pain/tenderness", "Recent prolonged travel", "Past malignancy", "No current PE symptoms"]
    },
}




# =========================================================
# VISUAL INVESTIGATION ASSETS
# Put image files inside an "images" folder next to app.py.
#
# IMPORTANT:
# - The app only shows an image when the corresponding test is ordered.
# - If an image file is missing, the text result still works.
# - Use de-identified, legally reusable educational images.
# =========================================================

VISUAL_ASSETS = {
    "Case 01 - Abdominal Pain": {
        "Abdominal ultrasound": {
            "file": "images/appendicitis_ultrasound.png",
            "caption": "Abdominal ultrasound — right lower quadrant",
            "teaching_note": "Look for a non-compressible blind-ending tubular structure >6 mm."
        },
        "CT abdomen/pelvis": {
            "file": "images/appendicitis_ct.png",
            "caption": "CT abdomen/pelvis",
            "teaching_note": "Look for an enlarged appendix and periappendiceal fat stranding."
        }
    },

    "Case 02 - Chest Pain": {
        "ECG": {
            "file": "images/inferior_stemi_ecg.png",
            "caption": "12-lead ECG",
            "teaching_note": "Look for ST elevation in leads II, III and aVF."
        },
        "Chest X-ray": {
            "file": "images/normal_cxr.png",
            "caption": "Chest X-ray",
            "teaching_note": "No acute pulmonary abnormality."
        }
    },

    "Case 03 - Shortness of Breath": {
        "Chest X-ray": {
            "file": "images/asthma_cxr.png",
            "caption": "Chest X-ray",
            "teaching_note": "Often normal or mildly hyperinflated in asthma."
        }
    },

    "Case 04 - Fever and Cough": {
        "Chest X-ray": {
            "file": "images/pneumonia_rll_cxr.png",
            "caption": "Chest X-ray",
            "teaching_note": "Look for right lower lobe air-space consolidation."
        }
    },

    "Case 05 - Sudden Breathlessness": {
        "CT pulmonary angiography": {
            "file": "images/pe_ctpa.png",
            "caption": "CT pulmonary angiography",
            "teaching_note": "Look for an intraluminal filling defect in a pulmonary artery."
        },
        "Lower-limb Doppler ultrasound": {
            "file": "images/dvt_ultrasound.png",
            "caption": "Compression ultrasound of the left leg",
            "teaching_note": "A thrombosed vein fails to compress."
        }
    },

    "Case 07 - Sudden Severe Headache": {
        "Non-contrast CT head": {
            "file": "images/sah_ct_head.png",
            "caption": "Non-contrast CT head",
            "teaching_note": "Look for hyperdense blood in the basal cisterns and sulci."
        },
        "CT angiography": {
            "file": "images/sah_cta_aneurysm.png",
            "caption": "CT angiography",
            "teaching_note": "Look for the causative intracranial aneurysm."
        }
    },

    "Case 08 - Sudden Weakness": {
        "Non-contrast CT head": {
            "file": "images/ischemic_stroke_ct.png",
            "caption": "Non-contrast CT head",
            "teaching_note": "Early ischaemic change may be subtle; first exclude haemorrhage."
        },
        "CT angiography": {
            "file": "images/mca_occlusion_cta.png",
            "caption": "CT angiography",
            "teaching_note": "Look for a left middle cerebral artery occlusion."
        },
        "ECG": {
            "file": "images/atrial_fibrillation_ecg.png",
            "caption": "12-lead ECG",
            "teaching_note": "Irregularly irregular rhythm with no consistent P waves."
        }
    },

    "Case 10 - Colicky Flank Pain": {
        "Non-contrast CT KUB": {
            "file": "images/ureteric_stone_ct.png",
            "caption": "Non-contrast CT KUB",
            "teaching_note": "Look for a hyperdense ureteric calculus and upstream dilatation."
        },
        "Renal ultrasound": {
            "file": "images/hydronephrosis_ultrasound.png",
            "caption": "Renal ultrasound",
            "teaching_note": "Look for dilatation of the renal pelvis and calyces."
        }
    },

    "Case 11 - Right Upper Abdominal Pain": {
        "Ultrasound abdomen": {
            "file": "images/cholecystitis_ultrasound.png",
            "caption": "Gallbladder ultrasound",
            "teaching_note": "Look for gallstones, wall thickening and pericholecystic fluid."
        },
        "CT abdomen": {
            "file": "images/cholecystitis_ct.png",
            "caption": "CT abdomen",
            "teaching_note": "CT can support the diagnosis but ultrasound is usually first-line."
        }
    },

    "Case 12 - Severe Epigastric Pain": {
        "CT abdomen": {
            "file": "images/pancreatitis_ct.png",
            "caption": "Contrast-enhanced CT abdomen",
            "teaching_note": "Look for pancreatic enlargement and surrounding inflammatory fat stranding."
        },
        "Abdominal ultrasound": {
            "file": "images/pancreas_gallbladder_ultrasound.png",
            "caption": "Upper abdominal ultrasound",
            "teaching_note": "Useful for looking for a gallstone cause."
        }
    },

    "Case 13 - Black Stools": {
        "Upper GI endoscopy": {
            "file": "images/bleeding_gastric_ulcer_endoscopy.png",
            "caption": "Upper GI endoscopy",
            "teaching_note": "Look for an ulcer with active bleeding or stigmata of recent haemorrhage."
        }
    },

    "Case 14 - Chronic Diarrhoea": {
        "Colonoscopy": {
            "file": "images/crohn_colonoscopy.png",
            "caption": "Colonoscopy",
            "teaching_note": "Look for patchy inflammation, deep ulceration and skip lesions."
        },
        "Colonic biopsy": {
            "file": "images/crohn_histology.png",
            "caption": "Colonic biopsy histology",
            "teaching_note": "Look for chronic active inflammation; granulomas may be present."
        }
    },

    "Case 15 - Bloody Diarrhoea": {
        "Colonoscopy": {
            "file": "images/uc_colonoscopy.png",
            "caption": "Colonoscopy",
            "teaching_note": "Look for continuous mucosal inflammation beginning at the rectum."
        },
        "Colonic biopsy": {
            "file": "images/uc_histology.png",
            "caption": "Colonic biopsy histology",
            "teaching_note": "Look for crypt architectural distortion and cryptitis/crypt abscesses."
        }
    },

    "Case 18 - Palpitations and Weight Loss": {
        "ECG": {
            "file": "images/sinus_tachycardia_ecg.png",
            "caption": "12-lead ECG",
            "teaching_note": "Sinus tachycardia."
        }
    },

    "Case 20 - Fatigue and Breathlessness": {
        "Blood film": {
            "file": "images/iron_deficiency_blood_film.png",
            "caption": "Peripheral blood film",
            "teaching_note": "Look for microcytic, hypochromic red cells with anisopoikilocytosis."
        }
    },

    "Case 23 - Sore Throat and Fatigue": {
        "FBC": {
            "file": "images/ebv_blood_film.png",
            "caption": "Peripheral blood film",
            "teaching_note": "Look for atypical lymphocytes."
        }
    },

    "Case 24 - Spinning Dizziness": {
        "Dix-Hallpike manoeuvre": {
            "file": "images/dix_hallpike_diagram.png",
            "caption": "Dix-Hallpike manoeuvre",
            "teaching_note": "In BPPV, the manoeuvre reproduces vertigo and positional nystagmus."
        }
    },

    "Case 26 - Sudden Hot Joint": {
        "Joint aspiration": {
            "file": "images/gout_crystals.png",
            "caption": "Polarised microscopy of joint aspirate",
            "teaching_note": "Needle-shaped, negatively birefringent monosodium urate crystals."
        },
        "X-ray foot": {
            "file": "images/gout_foot_xray.png",
            "caption": "Foot X-ray",
            "teaching_note": "Early gout may have a normal X-ray."
        }
    },

    "Case 27 - Lower Abdominal Pain and Bleeding": {
        "Transvaginal ultrasound": {
            "file": "images/ectopic_ultrasound.png",
            "caption": "Transvaginal ultrasound",
            "teaching_note": "Look for an adnexal mass, free fluid and absence of an intrauterine pregnancy."
        }
    },

    "Case 28 - Sudden Testicular Pain": {
        "Scrotal Doppler ultrasound": {
            "file": "images/testicular_torsion_doppler.png",
            "caption": "Scrotal Doppler ultrasound",
            "teaching_note": "Look for reduced or absent blood flow to the affected testis."
        }
    },

    "Case 29 - Racing Heart and Tingling": {
        "ECG": {
            "file": "images/sinus_tachycardia_ecg.png",
            "caption": "12-lead ECG",
            "teaching_note": "Sinus tachycardia with no acute ischaemic changes."
        }
    },

    "Case 31 - Jaw Pain and Headache": {
        "Temporal artery ultrasound": {
            "file": "images/gca_temporal_artery_ultrasound.png",
            "caption": "Temporal artery ultrasound",
            "teaching_note": "Look for the hypoechoic halo sign around the arterial lumen."
        },
        "Fundoscopy": {
            "file": "images/gca_fundoscopy.png",
            "caption": "Fundoscopic examination",
            "teaching_note": "Assess the optic disc and retina for ischaemic changes."
        }
    },

    "Case 32 - Swollen Painful Calf": {
        "Compression ultrasound": {
            "file": "images/dvt_ultrasound.png",
            "caption": "Compression ultrasound",
            "teaching_note": "A thrombosed vein remains non-compressible."
        }
    }
}

# =========================================================
# SELECTIVE INVESTIGATION CATALOGUE
# Each investigation has:
# - result: what the student sees
# - value: "essential", "useful", or "low_value"
# =========================================================

TEST_CATALOG = {
    "Case 01 - Abdominal Pain": {
        "FBC": {"value": "useful", "result": "WBC 14.8 ×10⁹/L with neutrophilia."},
        "CRP": {"value": "useful", "result": "Elevated."},
        "Urinalysis": {"value": "useful", "result": "No significant abnormality."},
        "β-hCG": {"value": "essential", "result": "Negative."},
        "Abdominal ultrasound": {"value": "essential", "result": "Non-compressible blind-ending tubular structure in the right lower quadrant, ~8 mm diameter."},
        "CT abdomen/pelvis": {"value": "useful", "result": "Inflamed appendix with periappendiceal fat stranding."}
    },
    "Case 02 - Chest Pain": {
        "ECG": {"value": "essential", "result": "ST-segment elevation in leads II, III and aVF."},
        "High-sensitivity troponin": {"value": "essential", "result": "Elevated."},
        "FBC": {"value": "useful", "result": "No major acute abnormality."},
        "Electrolytes/U&E": {"value": "useful", "result": "No major acute abnormality."},
        "Chest X-ray": {"value": "useful", "result": "No acute pulmonary abnormality."},
        "D-dimer": {"value": "low_value", "result": "Not clinically useful in this high-suspicion ACS presentation."}
    },
    "Case 03 - Shortness of Breath": {
        "Peak expiratory flow": {"value": "essential", "result": "~45% of predicted."},
        "ABG": {"value": "useful", "result": "Mild respiratory alkalosis with hypoxaemia."},
        "Chest X-ray": {"value": "useful", "result": "No focal consolidation or pneumothorax."},
        "FBC": {"value": "useful", "result": "No major abnormality."},
        "Troponin": {"value": "low_value", "result": "Normal."}
    },
    "Case 04 - Fever and Cough": {
        "FBC": {"value": "useful", "result": "Neutrophilic leukocytosis."},
        "CRP": {"value": "useful", "result": "Markedly elevated."},
        "Chest X-ray": {"value": "essential", "result": "Right lower lobe consolidation."},
        "Blood cultures": {"value": "useful", "result": "Taken before antibiotics; no growth yet."},
        "Sputum culture": {"value": "useful", "result": "Purulent sample sent; result pending."}
    },
    "Case 05 - Sudden Breathlessness": {
        "ECG": {"value": "useful", "result": "Sinus tachycardia."},
        "D-dimer": {"value": "useful", "result": "Elevated."},
        "CT pulmonary angiography": {"value": "essential", "result": "Segmental pulmonary artery filling defect consistent with pulmonary embolism."},
        "Lower-limb Doppler ultrasound": {"value": "useful", "result": "Thrombus in the left popliteal vein."},
        "Troponin": {"value": "useful", "result": "Mildly elevated."}
    },
    "Case 06 - Recurrent Headache": {
        "No investigation": {"value": "essential", "result": "Reasonable in a typical migraine presentation with a normal neurological examination and no red flags."},
        "CT head": {"value": "low_value", "result": "No acute intracranial abnormality."},
        "MRI brain": {"value": "low_value", "result": "No acute intracranial abnormality."},
        "FBC": {"value": "low_value", "result": "Normal."}
    },
    "Case 07 - Sudden Severe Headache": {
        "Non-contrast CT head": {"value": "essential", "result": "Acute blood in the basal cisterns."},
        "CT angiography": {"value": "useful", "result": "Intracranial aneurysm identified."},
        "Lumbar puncture": {"value": "useful", "result": "Would be considered if CT were non-diagnostic and suspicion remained high, after appropriate timing and safety review."},
        "FBC": {"value": "useful", "result": "No major abnormality."}
    },
    "Case 08 - Sudden Weakness": {
        "Capillary glucose": {"value": "essential", "result": "Normal."},
        "Non-contrast CT head": {"value": "essential", "result": "No intracranial haemorrhage."},
        "CT angiography": {"value": "essential", "result": "Left middle cerebral artery occlusion."},
        "ECG": {"value": "useful", "result": "Atrial fibrillation."},
        "FBC": {"value": "useful", "result": "No major abnormality."}
    },
    "Case 09 - Fever and Flank Pain": {
        "Urinalysis": {"value": "essential", "result": "Positive nitrites, leukocytes and blood."},
        "Urine culture": {"value": "essential", "result": "Pyuria and significant bacteriuria."},
        "FBC": {"value": "useful", "result": "Leukocytosis."},
        "CRP": {"value": "useful", "result": "Elevated."},
        "Pregnancy test": {"value": "essential", "result": "Negative."},
        "Renal ultrasound": {"value": "useful", "result": "No hydronephrosis."}
    },
    "Case 10 - Colicky Flank Pain": {
        "Urinalysis": {"value": "useful", "result": "Microscopic haematuria."},
        "Renal function": {"value": "useful", "result": "Normal."},
        "Non-contrast CT KUB": {"value": "essential", "result": "5 mm right distal ureteric calculus with mild hydroureter."},
        "Renal ultrasound": {"value": "useful", "result": "Mild right-sided hydronephrosis."}
    },
    "Case 11 - Right Upper Abdominal Pain": {
        "FBC": {"value": "useful", "result": "Leukocytosis."},
        "CRP": {"value": "useful", "result": "Elevated."},
        "Liver function tests": {"value": "useful", "result": "Mildly abnormal."},
        "Ultrasound abdomen": {"value": "essential", "result": "Gallstones, thickened gallbladder wall and pericholecystic fluid."},
        "CT abdomen": {"value": "low_value", "result": "Findings are compatible with cholecystitis, but ultrasound is the preferred first-line test."}
    },
    "Case 12 - Severe Epigastric Pain": {
        "Serum lipase": {"value": "essential", "result": "Markedly elevated."},
        "CRP": {"value": "useful", "result": "Elevated."},
        "Liver function tests": {"value": "useful", "result": "Mildly abnormal."},
        "Triglycerides": {"value": "useful", "result": "Elevated."},
        "Abdominal ultrasound": {"value": "useful", "result": "No gallstones seen."},
        "CT abdomen": {"value": "useful", "result": "Pancreatic inflammation and surrounding fat stranding."}
    },
    "Case 13 - Black Stools": {
        "FBC": {"value": "essential", "result": "Haemoglobin is reduced."},
        "Urea/creatinine": {"value": "useful", "result": "Urea is disproportionately elevated relative to creatinine."},
        "Group and save / crossmatch": {"value": "essential", "result": "Sample sent and compatible blood available."},
        "Upper GI endoscopy": {"value": "essential", "result": "Bleeding gastric ulcer."},
        "CT abdomen": {"value": "low_value", "result": "Not the preferred first-line investigation for this presentation."}
    },
    "Case 14 - Chronic Diarrhoea": {
        "FBC": {"value": "useful", "result": "Mild anaemia."},
        "CRP": {"value": "useful", "result": "Elevated."},
        "Faecal calprotectin": {"value": "essential", "result": "Elevated."},
        "Colonoscopy": {"value": "essential", "result": "Patchy ulceration with skip lesions."},
        "Colonic biopsy": {"value": "essential", "result": "Inflammatory changes compatible with Crohn disease."}
    },
    "Case 15 - Bloody Diarrhoea": {
        "FBC": {"value": "useful", "result": "Anaemia."},
        "CRP": {"value": "useful", "result": "Elevated."},
        "Faecal calprotectin": {"value": "essential", "result": "Elevated."},
        "Colonoscopy": {"value": "essential", "result": "Continuous inflammation beginning at the rectum."},
        "Colonic biopsy": {"value": "essential", "result": "Mucosal inflammation compatible with ulcerative colitis."}
    },
    "Case 16 - Thirst and Vomiting": {
        "Capillary glucose": {"value": "essential", "result": "28 mmol/L."},
        "Blood ketones": {"value": "essential", "result": "Markedly elevated."},
        "Venous blood gas": {"value": "essential", "result": "Metabolic acidosis with low bicarbonate."},
        "Electrolytes/U&E": {"value": "essential", "result": "Potassium is elevated initially."},
        "Urinalysis": {"value": "useful", "result": "Glucose and ketones present."}
    },
    "Case 17 - Confusion and Sweating": {
        "Capillary glucose": {"value": "essential", "result": "2.4 mmol/L."},
        "ECG": {"value": "useful", "result": "Sinus tachycardia."},
        "FBC": {"value": "low_value", "result": "No acute abnormality."},
        "CT head": {"value": "low_value", "result": "No acute intracranial abnormality; glucose should be checked first in this presentation."}
    },
    "Case 18 - Palpitations and Weight Loss": {
        "TSH": {"value": "essential", "result": "Suppressed."},
        "Free T4": {"value": "essential", "result": "Elevated."},
        "Free T3": {"value": "useful", "result": "Elevated."},
        "TSH receptor antibodies": {"value": "useful", "result": "Positive."},
        "ECG": {"value": "useful", "result": "Sinus tachycardia."}
    },
    "Case 19 - Tiredness and Weight Gain": {
        "TSH": {"value": "essential", "result": "Elevated."},
        "Free T4": {"value": "essential", "result": "Low."},
        "Anti-TPO antibodies": {"value": "useful", "result": "Positive."},
        "FBC": {"value": "useful", "result": "Mild normocytic anaemia."}
    },
    "Case 20 - Fatigue and Breathlessness": {
        "FBC": {"value": "essential", "result": "Haemoglobin low with microcytosis."},
        "Ferritin": {"value": "essential", "result": "Low."},
        "Transferrin saturation": {"value": "useful", "result": "Low."},
        "Blood film": {"value": "useful", "result": "Microcytic, hypochromic red cells."},
        "B12/folate": {"value": "low_value", "result": "Within normal range."}
    },
    "Case 21 - Sudden Rash and Breathing Difficulty": {
        "No investigation before treatment": {"value": "essential", "result": "Correct: this is a clinical emergency and treatment should not wait for tests."},
        "Serum tryptase": {"value": "useful", "result": "May be elevated; sample should be taken after initial emergency treatment."},
        "ECG": {"value": "useful", "result": "Sinus tachycardia."},
        "Chest X-ray": {"value": "low_value", "result": "No focal acute abnormality; should not delay treatment."}
    },
    "Case 22 - Fever, Headache and Stiff Neck": {
        "FBC": {"value": "useful", "result": "Leukocytosis."},
        "CRP": {"value": "useful", "result": "Markedly elevated."},
        "Blood cultures": {"value": "essential", "result": "Taken before antibiotics where this does not delay treatment."},
        "Lumbar puncture": {"value": "essential", "result": "Cloudy CSF, neutrophilic pleocytosis, high protein and low glucose."},
        "CT head": {"value": "useful", "result": "No mass effect or acute haemorrhage."}
    },
    "Case 23 - Sore Throat and Fatigue": {
        "FBC": {"value": "useful", "result": "Lymphocytosis with atypical lymphocytes."},
        "Heterophile antibody test": {"value": "essential", "result": "Positive."},
        "EBV serology": {"value": "useful", "result": "Consistent with acute EBV infection."},
        "Throat culture": {"value": "low_value", "result": "No Group A streptococcus isolated."}
    },
    "Case 24 - Spinning Dizziness": {
        "Dix-Hallpike manoeuvre": {"value": "essential", "result": "Reproduces vertigo with brief positional nystagmus."},
        "No imaging": {"value": "essential", "result": "Appropriate in a classic presentation without neurological red flags."},
        "CT head": {"value": "low_value", "result": "No acute intracranial abnormality."},
        "MRI brain": {"value": "low_value", "result": "No acute intracranial abnormality."}
    },
    "Case 25 - Red Painful Leg": {
        "FBC": {"value": "useful", "result": "Mild leukocytosis."},
        "CRP": {"value": "useful", "result": "Elevated."},
        "Blood glucose": {"value": "useful", "result": "Mildly elevated."},
        "Ultrasound soft tissues": {"value": "useful", "result": "No drainable abscess."},
        "D-dimer": {"value": "low_value", "result": "Not helpful when the clinical picture is more consistent with cellulitis."}
    },
    "Case 26 - Sudden Hot Joint": {
        "Joint aspiration": {"value": "essential", "result": "Needle-shaped, negatively birefringent monosodium urate crystals; Gram stain shows no organisms."},
        "Serum urate": {"value": "useful", "result": "Elevated."},
        "FBC": {"value": "useful", "result": "Mild leukocytosis."},
        "CRP": {"value": "useful", "result": "Elevated."},
        "X-ray foot": {"value": "low_value", "result": "No acute bony abnormality."}
    },
    "Case 27 - Lower Abdominal Pain and Bleeding": {
        "Urine pregnancy test": {"value": "essential", "result": "Positive."},
        "Serum β-hCG": {"value": "essential", "result": "Positive."},
        "Transvaginal ultrasound": {"value": "essential", "result": "No intrauterine gestational sac; left adnexal mass and small amount of free pelvic fluid."},
        "FBC": {"value": "useful", "result": "Mild anaemia."},
        "Blood group and Rh": {"value": "useful", "result": "Blood group documented; Rh status available."}
    },
    "Case 28 - Sudden Testicular Pain": {
        "Urgent urology review": {"value": "essential", "result": "Correct: immediate surgical assessment is indicated."},
        "Scrotal Doppler ultrasound": {"value": "useful", "result": "Reduced/absent blood flow to the left testis. Imaging should not delay surgery if clinical suspicion is high."},
        "Urinalysis": {"value": "useful", "result": "No significant abnormality."},
        "STI screen": {"value": "low_value", "result": "Negative; should not delay urgent management."}
    },
    "Case 29 - Racing Heart and Tingling": {
        "ECG": {"value": "essential", "result": "Sinus tachycardia."},
        "Capillary glucose": {"value": "useful", "result": "Normal."},
        "FBC": {"value": "useful", "result": "No acute abnormality."},
        "Electrolytes/U&E": {"value": "useful", "result": "Normal."},
        "Troponin": {"value": "low_value", "result": "Normal."}
    },
    "Case 30 - Facial Weakness": {
        "No routine imaging": {"value": "essential", "result": "Appropriate in an otherwise typical isolated lower motor neuron facial palsy."},
        "Capillary glucose": {"value": "useful", "result": "Normal."},
        "CT head": {"value": "low_value", "result": "No acute intracranial abnormality."},
        "MRI brain": {"value": "low_value", "result": "No acute intracranial abnormality."}
    },
    "Case 31 - Jaw Pain and Headache": {
        "ESR": {"value": "essential", "result": "Markedly elevated."},
        "CRP": {"value": "essential", "result": "Markedly elevated."},
        "Platelets": {"value": "useful", "result": "Elevated."},
        "Temporal artery ultrasound": {"value": "essential", "result": "Halo sign present."},
        "Fundoscopy": {"value": "useful", "result": "Optic disc appears pale and swollen, concerning for ischaemic optic neuropathy."},
        "Temporal artery biopsy": {"value": "useful", "result": "Granulomatous arteritis with giant cells."}
    },
    "Case 32 - Swollen Painful Calf": {
        "D-dimer": {"value": "useful", "result": "Elevated."},
        "Compression ultrasound": {"value": "essential", "result": "Non-compressible right popliteal vein consistent with thrombosis."},
        "CT pulmonary angiography": {"value": "low_value", "result": "No pulmonary embolism; patient has no current chest symptoms."},
        "FBC": {"value": "useful", "result": "No major acute abnormality."}
    },
}

# =========================================================
# EXAMINATION / INVESTIGATION DATA
# These are revealed only when the student requests them.
# =========================================================

EXAM_DATA = {
    "Case 01 - Abdominal Pain": {
        "vitals": [
            "Temperature: 37.9 °C",
            "Heart rate: 102 bpm",
            "Blood pressure: 118/72 mmHg",
            "Respiratory rate: 18/min",
            "SpO₂: 99% on room air"
        ],
        "examination": [
            "Patient lies relatively still because movement worsens the pain.",
            "Abdomen: maximal tenderness in the right lower quadrant.",
            "Guarding is present.",
            "Rebound tenderness is present.",
            "Rovsing sign is positive."
        ],
        "investigations": [
            "FBC: WBC 14.8 ×10⁹/L with neutrophilia.",
            "CRP: elevated.",
            "Urinalysis: no significant abnormality.",
            "β-hCG: negative.",
            "Ultrasound abdomen: non-compressible blind-ending tubular structure in the right lower quadrant, ~8 mm diameter."
        ]
    },

    "Case 02 - Chest Pain": {
        "vitals": [
            "Heart rate: 104 bpm",
            "Blood pressure: 156/92 mmHg",
            "Respiratory rate: 22/min",
            "SpO₂: 95% on room air",
            "Temperature: 36.7 °C"
        ],
        "examination": [
            "Patient appears pale and clammy.",
            "Cardiovascular exam: tachycardic, regular rhythm, no obvious murmur.",
            "Chest is clear on auscultation.",
            "No reproducible chest-wall tenderness."
        ],
        "investigations": [
            "ECG: ST-segment elevation in leads II, III and aVF.",
            "High-sensitivity troponin: elevated.",
            "FBC and electrolytes: no major acute abnormality.",
            "Chest X-ray: no acute pulmonary abnormality."
        ]
    },

    "Case 03 - Shortness of Breath": {
        "vitals": [
            "Heart rate: 112 bpm",
            "Blood pressure: 128/74 mmHg",
            "Respiratory rate: 28/min",
            "SpO₂: 92% on room air",
            "Temperature: 36.8 °C"
        ],
        "examination": [
            "Patient is speaking in short sentences.",
            "Accessory muscles of respiration are in use.",
            "Chest: widespread bilateral expiratory wheeze.",
            "Air entry is reduced but present bilaterally."
        ],
        "investigations": [
            "Peak expiratory flow: ~45% of predicted.",
            "ABG: mild respiratory alkalosis with hypoxaemia.",
            "Chest X-ray: no focal consolidation or pneumothorax."
        ]
    },

    "Case 04 - Fever and Cough": {
        "vitals": [
            "Temperature: 39.1 °C",
            "Heart rate: 108 bpm",
            "Blood pressure: 124/76 mmHg",
            "Respiratory rate: 24/min",
            "SpO₂: 93% on room air"
        ],
        "examination": [
            "Patient looks unwell and febrile.",
            "Chest: reduced air entry at the right base.",
            "Coarse crackles over the right lower zone.",
            "Dullness to percussion at the right base."
        ],
        "investigations": [
            "FBC: neutrophilic leukocytosis.",
            "CRP: markedly elevated.",
            "Chest X-ray: right lower lobe consolidation.",
            "Blood cultures: taken before antibiotics."
        ]
    },

    "Case 05 - Sudden Breathlessness": {
        "vitals": [
            "Heart rate: 118 bpm",
            "Blood pressure: 108/68 mmHg",
            "Respiratory rate: 30/min",
            "SpO₂: 90% on room air",
            "Temperature: 36.9 °C"
        ],
        "examination": [
            "Patient is anxious and tachypnoeic.",
            "Chest is clear on auscultation.",
            "Left calf is mildly swollen and tender compared with the right.",
            "No obvious signs of pneumonia."
        ],
        "investigations": [
            "ECG: sinus tachycardia.",
            "D-dimer: elevated.",
            "CT pulmonary angiography: filling defect in a segmental pulmonary artery.",
            "Lower-limb Doppler ultrasound: thrombus in the left popliteal vein."
        ]
    },

    "Case 06 - Recurrent Headache": {
        "vitals": [
            "Temperature: 36.6 °C",
            "Heart rate: 78 bpm",
            "Blood pressure: 118/70 mmHg",
            "SpO₂: 99% on room air"
        ],
        "examination": [
            "Neurological examination is normal between episodes.",
            "No meningism.",
            "Fundoscopy: no papilloedema.",
            "No focal neurological deficit."
        ],
        "investigations": [
            "No urgent investigation is required from the current history and normal examination.",
            "If imaging is performed because of atypical features: no acute intracranial abnormality."
        ]
    },

    "Case 07 - Sudden Severe Headache": {
        "vitals": [
            "Temperature: 37.2 °C",
            "Heart rate: 96 bpm",
            "Blood pressure: 168/96 mmHg",
            "Respiratory rate: 20/min"
        ],
        "examination": [
            "Patient is distressed and photophobic.",
            "Neck stiffness is present.",
            "No obvious focal motor deficit.",
            "GCS: 14/15 due to confusion."
        ],
        "investigations": [
            "Non-contrast CT head: acute blood in the basal cisterns.",
            "If CT were non-diagnostic and suspicion remained high: lumbar puncture would be considered after appropriate timing and safety assessment."
        ]
    },

    "Case 08 - Sudden Weakness": {
        "vitals": [
            "Heart rate: 96 bpm, irregularly irregular",
            "Blood pressure: 176/98 mmHg",
            "Respiratory rate: 18/min",
            "SpO₂: 97% on room air"
        ],
        "examination": [
            "Right facial droop.",
            "Right arm power: 2/5.",
            "Right leg power: 3/5.",
            "Dysarthria present.",
            "Left side power is normal."
        ],
        "investigations": [
            "Capillary glucose: normal.",
            "Non-contrast CT head: no intracranial haemorrhage.",
            "CT angiography: left middle cerebral artery occlusion."
        ]
    },

    "Case 09 - Fever and Flank Pain": {
        "vitals": [
            "Temperature: 39.0 °C",
            "Heart rate: 110 bpm",
            "Blood pressure: 112/70 mmHg",
            "Respiratory rate: 20/min"
        ],
        "examination": [
            "Marked left costovertebral angle tenderness.",
            "Mild suprapubic tenderness.",
            "No peritonism."
        ],
        "investigations": [
            "Urinalysis: positive nitrites, leukocytes and blood.",
            "Urine microscopy/culture: pyuria and bacteriuria.",
            "FBC: leukocytosis.",
            "CRP: elevated.",
            "Pregnancy test: negative."
        ]
    },

    "Case 10 - Colicky Flank Pain": {
        "vitals": [
            "Temperature: 36.7 °C",
            "Heart rate: 98 bpm",
            "Blood pressure: 142/86 mmHg"
        ],
        "examination": [
            "Patient is restless and unable to find a comfortable position.",
            "Right loin tenderness.",
            "No guarding or rebound tenderness."
        ],
        "investigations": [
            "Urinalysis: microscopic haematuria.",
            "Renal function: normal.",
            "Non-contrast CT KUB: 5 mm right distal ureteric calculus with mild hydroureter."
        ]
    },

    "Case 11 - Right Upper Abdominal Pain": {
        "vitals": [
            "Temperature: 38.2 °C",
            "Heart rate: 104 bpm",
            "Blood pressure: 126/78 mmHg"
        ],
        "examination": [
            "Right upper quadrant tenderness.",
            "Murphy sign is positive.",
            "No generalized peritonism."
        ],
        "investigations": [
            "FBC: leukocytosis.",
            "CRP: elevated.",
            "Liver enzymes: mildly abnormal.",
            "Ultrasound: gallstones, thickened gallbladder wall and pericholecystic fluid."
        ]
    },

    "Case 12 - Severe Epigastric Pain": {
        "vitals": [
            "Heart rate: 112 bpm",
            "Blood pressure: 104/68 mmHg",
            "Temperature: 37.8 °C",
            "Respiratory rate: 22/min"
        ],
        "examination": [
            "Epigastric tenderness without rigid abdomen.",
            "Bowel sounds are reduced.",
            "Patient appears dehydrated."
        ],
        "investigations": [
            "Serum lipase: markedly elevated.",
            "CRP: elevated.",
            "LFTs: mildly abnormal.",
            "Ultrasound: no gallstones seen.",
            "Triglycerides: elevated."
        ]
    },

    "Case 13 - Black Stools": {
        "vitals": [
            "Heart rate: 108 bpm",
            "Blood pressure: 102/64 mmHg lying; 88/56 mmHg standing",
            "Respiratory rate: 20/min"
        ],
        "examination": [
            "Patient is pale.",
            "Mild epigastric tenderness.",
            "Rectal exam: black, tarry stool."
        ],
        "investigations": [
            "Haemoglobin: reduced.",
            "Urea: disproportionately elevated relative to creatinine.",
            "Group and save / crossmatch performed.",
            "Upper GI endoscopy: bleeding gastric ulcer."
        ]
    },

    "Case 14 - Chronic Diarrhoea": {
        "vitals": [
            "Temperature: 37.5 °C",
            "Heart rate: 92 bpm",
            "Blood pressure: 116/72 mmHg"
        ],
        "examination": [
            "Mild right lower quadrant abdominal tenderness.",
            "Patient appears mildly underweight.",
            "Small perianal skin tag is present."
        ],
        "investigations": [
            "FBC: mild anaemia.",
            "CRP: elevated.",
            "Faecal calprotectin: elevated.",
            "Colonoscopy: patchy ulceration with skip lesions.",
            "Biopsy: transmural inflammatory changes compatible with Crohn disease."
        ]
    },

    "Case 15 - Bloody Diarrhoea": {
        "vitals": [
            "Temperature: 37.8 °C",
            "Heart rate: 98 bpm",
            "Blood pressure: 114/70 mmHg"
        ],
        "examination": [
            "Mild left lower quadrant tenderness.",
            "No peritonism.",
            "Patient looks mildly pale."
        ],
        "investigations": [
            "FBC: anaemia.",
            "CRP: elevated.",
            "Faecal calprotectin: elevated.",
            "Colonoscopy: continuous inflammation beginning at the rectum.",
            "Biopsy: mucosal inflammation compatible with ulcerative colitis."
        ]
    },

    "Case 16 - Thirst and Vomiting": {
        "vitals": [
            "Heart rate: 124 bpm",
            "Blood pressure: 98/60 mmHg",
            "Respiratory rate: 30/min with deep respirations",
            "SpO₂: 99% on room air"
        ],
        "examination": [
            "Patient appears dehydrated.",
            "Dry mucous membranes.",
            "Deep, rapid Kussmaul-type breathing.",
            "Fruity/acetone odour on breath."
        ],
        "investigations": [
            "Capillary glucose: 28 mmol/L.",
            "Blood ketones: markedly elevated.",
            "Venous blood gas: metabolic acidosis with low bicarbonate.",
            "Potassium: elevated initially.",
            "Urinalysis: glucose and ketones present."
        ]
    },

    "Case 17 - Confusion and Sweating": {
        "vitals": [
            "Heart rate: 112 bpm",
            "Blood pressure: 136/78 mmHg",
            "Respiratory rate: 20/min"
        ],
        "examination": [
            "Patient is sweaty and tremulous.",
            "Confused but able to follow simple commands.",
            "No focal neurological deficit."
        ],
        "investigations": [
            "Capillary blood glucose: 2.4 mmol/L.",
            "Symptoms improve rapidly after oral/IV glucose."
        ]
    },

    "Case 18 - Palpitations and Weight Loss": {
        "vitals": [
            "Heart rate: 116 bpm",
            "Blood pressure: 142/68 mmHg",
            "Temperature: 37.3 °C"
        ],
        "examination": [
            "Fine tremor of the hands.",
            "Warm, moist skin.",
            "Diffuse non-tender goitre.",
            "Brisk reflexes.",
            "Mild lid retraction."
        ],
        "investigations": [
            "TSH: suppressed.",
            "Free T4: elevated.",
            "Free T3: elevated.",
            "TSH receptor antibodies: positive."
        ]
    },

    "Case 19 - Tiredness and Weight Gain": {
        "vitals": [
            "Heart rate: 56 bpm",
            "Blood pressure: 124/76 mmHg",
            "Temperature: 36.0 °C"
        ],
        "examination": [
            "Dry skin.",
            "Slow-relaxing reflexes.",
            "Mild non-pitting facial puffiness.",
            "Thyroid may feel mildly enlarged and firm."
        ],
        "investigations": [
            "TSH: elevated.",
            "Free T4: low.",
            "Anti-TPO antibodies: positive."
        ]
    },

    "Case 20 - Fatigue and Breathlessness": {
        "vitals": [
            "Heart rate: 102 bpm",
            "Blood pressure: 118/72 mmHg",
            "SpO₂: 99% on room air"
        ],
        "examination": [
            "Conjunctival pallor.",
            "No jaundice.",
            "Soft systolic flow murmur."
        ],
        "investigations": [
            "Haemoglobin: low.",
            "MCV: low.",
            "Ferritin: low.",
            "Transferrin saturation: low.",
            "Blood film: microcytic, hypochromic red cells."
        ]
    },

    "Case 21 - Sudden Rash and Breathing Difficulty": {
        "vitals": [
            "Heart rate: 126 bpm",
            "Blood pressure: 86/54 mmHg",
            "Respiratory rate: 30/min",
            "SpO₂: 89% on room air"
        ],
        "examination": [
            "Diffuse urticaria.",
            "Lip and facial swelling.",
            "Widespread wheeze.",
            "Patient is hypotensive and distressed."
        ],
        "investigations": [
            "This is a clinical emergency; treatment should not wait for tests.",
            "Serum tryptase may be measured after initial emergency treatment."
        ]
    },

    "Case 22 - Fever, Headache and Stiff Neck": {
        "vitals": [
            "Temperature: 39.4 °C",
            "Heart rate: 118 bpm",
            "Blood pressure: 106/66 mmHg",
            "Respiratory rate: 22/min"
        ],
        "examination": [
            "Patient is photophobic and drowsy.",
            "Neck stiffness is present.",
            "No focal neurological deficit.",
            "No obvious non-blanching rash."
        ],
        "investigations": [
            "FBC: leukocytosis.",
            "CRP: markedly elevated.",
            "Blood cultures: taken.",
            "Lumbar puncture: cloudy CSF, high neutrophils, high protein, low glucose."
        ]
    },

    "Case 23 - Sore Throat and Fatigue": {
        "vitals": [
            "Temperature: 38.0 °C",
            "Heart rate: 92 bpm"
        ],
        "examination": [
            "Enlarged erythematous tonsils with exudate.",
            "Tender posterior cervical lymphadenopathy.",
            "Mild splenomegaly."
        ],
        "investigations": [
            "FBC: lymphocytosis with atypical lymphocytes.",
            "Heterophile antibody test / EBV serology: positive."
        ]
    },

    "Case 24 - Spinning Dizziness": {
        "vitals": [
            "Heart rate: 76 bpm",
            "Blood pressure: 126/74 mmHg",
            "Temperature: 36.6 °C"
        ],
        "examination": [
            "Neurological examination is otherwise normal.",
            "Dix-Hallpike manoeuvre reproduces vertigo with a brief positional nystagmus.",
            "No focal cerebellar signs."
        ],
        "investigations": [
            "No routine imaging is required when the history and examination are typical and there are no neurological red flags."
        ]
    },

    "Case 25 - Red Painful Leg": {
        "vitals": [
            "Temperature: 38.1 °C",
            "Heart rate: 98 bpm",
            "Blood pressure: 122/74 mmHg"
        ],
        "examination": [
            "Left lower leg is erythematous, warm and tender.",
            "Borders are poorly demarcated.",
            "No fluctuance suggesting an abscess.",
            "No crepitus."
        ],
        "investigations": [
            "FBC: mild leukocytosis.",
            "CRP: elevated.",
            "Blood glucose: mildly elevated.",
            "Imaging is not routinely required unless deeper infection is suspected."
        ]
    },

    "Case 26 - Sudden Hot Joint": {
        "vitals": [
            "Temperature: 37.2 °C",
            "Heart rate: 90 bpm",
            "Blood pressure: 148/88 mmHg"
        ],
        "examination": [
            "First MTP joint is red, hot, swollen and exquisitely tender.",
            "Even light touch causes severe pain."
        ],
        "investigations": [
            "Serum urate: elevated, though this is not diagnostic by itself.",
            "Joint aspirate: needle-shaped, negatively birefringent monosodium urate crystals.",
            "Gram stain: no organisms."
        ]
    },

    "Case 27 - Lower Abdominal Pain and Bleeding": {
        "vitals": [
            "Heart rate: 108 bpm",
            "Blood pressure: 98/62 mmHg",
            "Respiratory rate: 20/min"
        ],
        "examination": [
            "Left lower quadrant tenderness.",
            "Mild guarding.",
            "Pelvic examination: left adnexal tenderness.",
            "Small amount of vaginal bleeding."
        ],
        "investigations": [
            "Urine pregnancy test: positive.",
            "Serum β-hCG: positive.",
            "Transvaginal ultrasound: no intrauterine gestational sac; left adnexal mass and small amount of free pelvic fluid."
        ]
    },

    "Case 28 - Sudden Testicular Pain": {
        "vitals": [
            "Heart rate: 110 bpm",
            "Blood pressure: 132/78 mmHg",
            "Temperature: 36.7 °C"
        ],
        "examination": [
            "Left testis is high-riding and extremely tender.",
            "Cremasteric reflex is absent on the left.",
            "No urethral discharge."
        ],
        "investigations": [
            "This is primarily a clinical diagnosis requiring urgent surgical review.",
            "If Doppler ultrasound is obtained without delaying treatment: reduced/absent blood flow to the left testis."
        ]
    },

    "Case 29 - Racing Heart and Tingling": {
        "vitals": [
            "Heart rate: 118 bpm",
            "Blood pressure: 138/84 mmHg",
            "Respiratory rate: 30/min",
            "SpO₂: 100% on room air"
        ],
        "examination": [
            "Patient appears acutely anxious and is hyperventilating.",
            "Cardiovascular and respiratory examinations are otherwise normal.",
            "Neurological examination is normal."
        ],
        "investigations": [
            "ECG: sinus tachycardia.",
            "Capillary glucose: normal.",
            "Basic blood tests: no acute abnormality.",
            "Further testing is guided by red flags and clinical context."
        ]
    },

    "Case 30 - Facial Weakness": {
        "vitals": [
            "Temperature: 36.8 °C",
            "Heart rate: 78 bpm",
            "Blood pressure: 124/72 mmHg"
        ],
        "examination": [
            "Complete left lower motor neuron facial weakness, including the forehead.",
            "Unable to fully close the left eye.",
            "Limb power and sensation are normal.",
            "No aphasia."
        ],
        "investigations": [
            "No routine imaging is required in a typical isolated peripheral facial palsy.",
            "Further tests would be considered if there were atypical features or another neurological deficit."
        ]
    },

    "Case 31 - Jaw Pain and Headache": {
        "vitals": [
            "Temperature: 37.4 °C",
            "Heart rate: 88 bpm",
            "Blood pressure: 146/82 mmHg"
        ],
        "examination": [
            "Right temporal artery is tender and feels thickened.",
            "Scalp tenderness is present.",
            "Visual acuity is mildly reduced on the right."
        ],
        "investigations": [
            "ESR: markedly elevated.",
            "CRP: markedly elevated.",
            "Platelets: elevated.",
            "Temporal artery ultrasound: halo sign.",
            "Temporal artery biopsy may be used to confirm the diagnosis."
        ]
    },

    "Case 32 - Swollen Painful Calf": {
        "vitals": [
            "Heart rate: 86 bpm",
            "Blood pressure: 128/76 mmHg",
            "SpO₂: 98% on room air",
            "Temperature: 36.8 °C"
        ],
        "examination": [
            "Right calf circumference is larger than the left.",
            "Right calf is tender and mildly warm.",
            "No signs of cellulitis.",
            "Chest examination is normal."
        ],
        "investigations": [
            "D-dimer: elevated.",
            "Compression ultrasound: non-compressible right popliteal vein consistent with thrombosis."
        ]
    },
}

# =========================================================
# EXTRA RESPONSE KEYS USED BY A FEW CASES
# =========================================================

SPECIAL_KEYS = {
    "shoulder_tip": ["shoulder tip", "shoulder-tip", "shoulder pain"],
    "weakness_limb": ["arm weakness", "leg weakness", "limb weakness", "arms and legs"],
    "jaw_claudication": ["jaw", "chewing", "jaw pain", "jaw ache"],
}

# =========================================================
# QUESTION INTENTS
# The first matching intent wins.
# =========================================================

INTENTS = [
    ("onset", "Onset", ["when did", "when was", "how long", "start", "begin", "suddenly"]),
    ("location", "Site", ["where is", "where does", "where exactly", "which side", "location", "where's"]),
    ("severity", "Severity", ["how bad", "how severe", "out of 10", "rate the", "pain score"]),
    ("character", "Character", ["what does it feel like", "what is it like", "describe the pain", "describe it", "sharp", "dull", "crushing", "burning", "throbbing", "pressure"]),
    ("radiation", "Radiation", ["radiate", "spread", "go anywhere", "move anywhere"]),
    ("aggravating", "Aggravating factors", ["worse", "make it worse", "aggravate", "trigger"]),
    ("relieving", "Relieving factors", ["better", "relieve", "help it", "improve"]),
    ("breathlessness", "Breathlessness", ["short of breath", "breathless", "breathing", "catch your breath"]),
    ("wheeze", "Wheeze", ["wheeze", "wheezing"]),
    ("cough", "Cough", ["cough"]),
    ("sputum", "Sputum", ["sputum", "phlegm", "mucus"]),
    ("chest_pain", "Chest pain", ["chest pain", "chest tight", "chest discomfort"]),
    ("palpitations", "Palpitations", ["palpitation", "heart racing", "heart pounding", "heart beat"]),
    ("syncope", "Syncope", ["faint", "passed out", "black out", "dizzy", "light-headed", "lightheaded"]),
    ("sweating", "Sweating", ["sweat", "sweating", "clammy"]),
    ("fever", "Fever", ["fever", "feverish", "temperature"]),
    ("chills", "Chills", ["chill", "rigor", "shaking"]),
    ("nausea", "Nausea", ["nausea", "nauseous", "feel sick", "feeling sick"]),
    ("vomiting", "Vomiting", ["vomit", "vomiting", "thrown up", "throw up", "been sick"]),
    ("appetite", "Appetite", ["appetite", "eating", "food"]),
    ("diarrhea", "Diarrhoea", ["diarrhea", "diarrhoea", "loose stool"]),
    ("constipation", "Constipation", ["constipation", "constipated"]),
    ("blood_stool", "Blood in stool", ["blood in stool", "blood in your stool", "black stool", "black stools", "melena", "melaena", "bloody stool"]),
    ("bowels", "Bowel symptoms", ["bowel", "stool", "poo", "poop"]),
    ("dysuria", "Dysuria", ["burn when", "burning when", "pain when you pee", "pain passing urine"]),
    ("frequency", "Urinary frequency", ["pee often", "urinate often", "frequency", "going more often", "passing urine often"]),
    ("hematuria", "Haematuria", ["blood in urine", "blood in your urine", "hematuria", "haematuria"]),
    ("urine", "Urinary symptoms", ["urine", "urinary", "pee", "peeing", "waterworks"]),
    ("vaginal_bleeding", "Vaginal bleeding", ["vaginal bleeding", "bleeding down below", "bleeding from vagina"]),
    ("vaginal_discharge", "Vaginal discharge", ["vaginal discharge", "discharge"]),
    ("lmp", "Pregnancy/LMP", ["last period", "last menstrual", "period"]),
    ("pregnancy", "Pregnancy/LMP", ["pregnant", "pregnancy", "pregnancy test"]),
    ("headache", "Headache features", ["headache", "head pain"]),
    ("photophobia", "Photophobia", ["light bother", "bright light", "photophobia"]),
    ("vision", "Vision", ["vision", "see", "sight", "double vision", "blurred"]),
    ("weakness", "Weakness", ["weakness", "weak", "power"]),
    ("numbness", "Numbness", ["numb", "tingling", "pins and needles"]),
    ("speech", "Speech", ["speech", "slurred", "talking", "words"]),
    ("seizure", "Seizure", ["seizure", "fit", "convulsion"]),
    ("neck_stiffness", "Neck stiffness", ["stiff neck", "neck stiff"]),
    ("rash", "Rash", ["rash", "spots", "welts", "hives"]),
    ("joint", "Joint symptoms", ["joint", "toe", "knee", "ankle"]),
    ("swelling", "Swelling", ["swelling", "swollen"]),
    ("leg_pain", "Leg pain", ["leg pain", "calf pain", "calf sore", "leg sore"]),
    ("weight_loss", "Weight loss", ["weight loss", "lost weight", "losing weight", "gained weight", "weight gain"]),
    ("thirst", "Thirst", ["thirst", "thirsty"]),
    ("polyuria", "Polyuria", ["peeing all the time", "urinating all the time", "polyuria"]),
    ("travel", "Travel", ["travel", "flight", "plane", "journey", "trip"]),
    ("immobilization", "Immobilization", ["immobile", "immobil", "bed rest", "sitting for", "long journey"]),
    ("sick_contacts", "Sick contacts", ["sick contact", "anyone ill", "anyone sick", "people around you"]),
    ("medical_history", "Medical history", ["medical history", "past medical", "health problems", "conditions", "illnesses", "diseases"]),
    ("surgery", "Surgical history", ["surgery", "surgeries", "operation", "operations"]),
    ("medications", "Medications", ["medication", "medications", "medicine", "medicines", "tablets", "pills", "take anything"]),
    ("allergies", "Allergies", ["allergy", "allergies", "allergic"]),
    ("smoking", "Smoking", ["smoke", "smoking", "cigarette", "vape"]),
    ("alcohol", "Alcohol", ["alcohol", "drink alcohol", "do you drink"]),
    ("recreational_drugs", "Recreational drugs", ["recreational drugs", "illegal drugs", "cocaine", "cannabis", "drug use"]),
    ("family_history", "Family history", ["family history", "runs in the family", "parents", "siblings"]),
]

SOCIAL_GREETINGS = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]
SOCIAL_REASSURE = ["don't worry", "do not worry", "we'll help", "we will help", "you're safe", "you are safe"]
SOCIAL_THANKS = ["thank you", "thanks"]


# =========================================================
# HUMAN-LIKE PATIENT BEHAVIOUR
# Adds tone, hesitations, occasional tangents and patient questions
# without changing the underlying clinical facts.
# =========================================================

PATIENT_BEHAVIOR = {
    "Case 01 - Abdominal Pain": {
        "mood": "worried",
        "hesitations": ["Um...", "I think...", "Sorry, I'm just a bit nervous..."],
        "tangents": ["I nearly didn't come in because I thought it might settle.", "I haven't really been able to get comfortable."],
        "concerns": ["Do you think this could be something serious?", "Am I going to need an operation?"]
    },
    "Case 02 - Chest Pain": {
        "mood": "stoic",
        "hesitations": ["Yeah...", "Right...", "It's hard to explain, but..."],
        "tangents": ["I thought it was indigestion at first.", "My wife told me not to ignore it."],
        "concerns": ["Is this my heart?", "Should I be worried?"]
    },
    "Case 03 - Shortness of Breath": {
        "mood": "breathless",
        "hesitations": ["Just... give me a second.", "Sorry... I'm a bit out of breath."],
        "tangents": ["I was fine earlier today.", "My inhaler usually works faster than this."],
        "concerns": ["Why isn't my inhaler helping properly?", "Am I getting worse?"]
    },
    "Case 04 - Fever and Cough": {
        "mood": "tired",
        "hesitations": ["Honestly...", "I think so...", "I've felt pretty rough."],
        "tangents": ["I've barely slept because of the coughing.", "I thought it was just a bad cold."],
        "concerns": ["Could this be pneumonia?", "Do I need to stay in hospital?"]
    },
    "Case 05 - Sudden Breathlessness": {
        "mood": "frightened",
        "hesitations": ["It was so sudden...", "I don't know, it just came on."],
        "tangents": ["I only got back from travelling yesterday.", "I honestly thought I was having a panic attack."],
        "concerns": ["Could this be a blood clot?", "Am I in danger?"]
    },
    "Case 06 - Recurrent Headache": {
        "mood": "frustrated",
        "hesitations": ["It's the same sort of thing again.", "Usually..."],
        "tangents": ["I had to leave work because of it.", "I normally just lie in a dark room."],
        "concerns": ["Why does this keep happening?", "Is there anything I can do to stop them coming back?"]
    },
    "Case 07 - Sudden Severe Headache": {
        "mood": "distressed",
        "hesitations": ["It just hit me...", "I can barely think straight."],
        "tangents": ["I've never had anything like this before.", "It was instant."],
        "concerns": ["Is something bleeding in my head?", "Please tell me this isn't serious."]
    },
    "Case 08 - Sudden Weakness": {
        "mood": "frustrated",
        "hesitations": ["My words aren't coming out right.", "It happened all at once."],
        "tangents": ["My wife noticed before I did.", "I was just sitting at home."],
        "concerns": ["Am I having a stroke?", "Will this get better?"]
    },
    "Case 09 - Fever and Flank Pain": {
        "mood": "unwell",
        "hesitations": ["Yeah... it's been getting worse.", "I think..."],
        "tangents": ["I kept hoping it was just a simple urine infection.", "I couldn't sleep last night."],
        "concerns": ["Has the infection gone to my kidney?", "Do I need antibiotics through a drip?"]
    },
    "Case 10 - Colicky Flank Pain": {
        "mood": "restless",
        "hesitations": ["It comes in waves.", "It's really hard to sit still."],
        "tangents": ["I keep pacing because lying down doesn't help.", "I've never had pain like this."],
        "concerns": ["Is this a kidney stone?", "Will I need surgery?"]
    },
    "Case 11 - Right Upper Abdominal Pain": {
        "mood": "irritable",
        "hesitations": ["It started after I ate.", "It's mostly here..."],
        "tangents": ["I've had milder episodes before after heavy meals.", "This time it didn't go away."],
        "concerns": ["Is it my gallbladder?", "Will I need an operation?"]
    },
    "Case 12 - Severe Epigastric Pain": {
        "mood": "guarded",
        "hesitations": ["I suppose...", "It's pretty constant."],
        "tangents": ["I know I probably drink more than I should.", "I couldn't keep anything down."],
        "concerns": ["Is this pancreatitis?", "How serious is this?"]
    },
    "Case 13 - Black Stools": {
        "mood": "concerned",
        "hesitations": ["I didn't know if it was important...", "It looked really dark."],
        "tangents": ["I thought maybe it was something I ate.", "Then I got dizzy standing up."],
        "concerns": ["Am I bleeding internally?", "Will I need a camera test?"]
    },
    "Case 14 - Chronic Diarrhoea": {
        "mood": "open",
        "hesitations": ["It's been going on for a while.", "I know this is a bit awkward..."],
        "tangents": ["I've started planning my day around toilets.", "It's really affecting university/work."],
        "concerns": ["Could this be inflammatory bowel disease?", "Is this something long term?"]
    },
    "Case 15 - Bloody Diarrhoea": {
        "mood": "tired",
        "hesitations": ["It's embarrassing, but...", "There's definitely blood."],
        "tangents": ["I'm exhausted from going so often.", "I don't really want to eat much."],
        "concerns": ["Could this be colitis?", "Am I losing too much blood?"]
    },
    "Case 16 - Thirst and Vomiting": {
        "mood": "exhausted",
        "hesitations": ["I'm really tired...", "I know I missed some insulin."],
        "tangents": ["I've been drinking water constantly.", "I didn't think missing a few doses would do this."],
        "concerns": ["Is this because I missed my insulin?", "Is this dangerous?"]
    },
    "Case 17 - Confusion and Sweating": {
        "mood": "confused",
        "hesitations": ["I feel a bit fuzzy...", "Sorry, what did you ask?"],
        "tangents": ["I didn't eat lunch.", "I suddenly got really shaky."],
        "concerns": ["Is my sugar too low?", "Can I have something sweet?"]
    },
    "Case 18 - Palpitations and Weight Loss": {
        "mood": "restless",
        "hesitations": ["My heart just won't slow down.", "It's been building up."],
        "tangents": ["Everyone keeps telling me I'm too energetic lately.", "I'm eating more but still losing weight."],
        "concerns": ["Could this be my thyroid?", "Why am I losing weight?"]
    },
    "Case 19 - Tiredness and Weight Gain": {
        "mood": "low-energy",
        "hesitations": ["Everything feels slow lately.", "I don't know..."],
        "tangents": ["I feel cold even when everyone else is fine.", "I thought I was just overworked."],
        "concerns": ["Could this be my thyroid?", "Why am I so tired all the time?"]
    },
    "Case 20 - Fatigue and Breathlessness": {
        "mood": "frustrated",
        "hesitations": ["I've just got no energy.", "It's been gradual."],
        "tangents": ["Stairs never used to bother me.", "I thought I was just unfit."],
        "concerns": ["Could I be anaemic?", "Do I need iron tablets?"]
    },
    "Case 21 - Sudden Rash and Breathing Difficulty": {
        "mood": "panicked",
        "hesitations": ["My throat feels tight...", "Please..."],
        "tangents": ["It started right after dessert.", "I have a peanut allergy."],
        "concerns": ["Am I having an allergic reaction?", "Can you help me breathe?"]
    },
    "Case 22 - Fever, Headache and Stiff Neck": {
        "mood": "drowsy",
        "hesitations": ["My head really hurts.", "The light is awful."],
        "tangents": ["I barely slept last night.", "I feel worse today."],
        "concerns": ["Could this be meningitis?", "Why is my neck so stiff?"]
    },
    "Case 23 - Sore Throat and Fatigue": {
        "mood": "chatty-tired",
        "hesitations": ["It's been about a week.", "Honestly..."],
        "tangents": ["I've basically been sleeping all day.", "Everyone at uni seems ill."],
        "concerns": ["Is this glandular fever?", "How long is this going to last?"]
    },
    "Case 24 - Spinning Dizziness": {
        "mood": "careful",
        "hesitations": ["If I move my head...", "It only lasts a short time."],
        "tangents": ["Rolling over in bed is the worst.", "I try not to move suddenly now."],
        "concerns": ["Is something wrong with my brain?", "Why does turning my head trigger it?"]
    },
    "Case 25 - Red Painful Leg": {
        "mood": "practical",
        "hesitations": ["It just got redder.", "It's definitely warmer."],
        "tangents": ["I thought I'd knocked it on something.", "It's getting more uncomfortable."],
        "concerns": ["Is this an infection?", "Do I need antibiotics?"]
    },
    "Case 26 - Sudden Hot Joint": {
        "mood": "grumpy",
        "hesitations": ["Don't touch it.", "It hurts even with the sheet on it."],
        "tangents": ["It woke me up in the night.", "I did have quite a few beers yesterday."],
        "concerns": ["Is this gout?", "How do I stop this happening again?"]
    },
    "Case 27 - Lower Abdominal Pain and Bleeding": {
        "mood": "scared",
        "hesitations": ["I'm really worried.", "I only found out yesterday..."],
        "tangents": ["The pregnancy test was positive.", "I wasn't expecting this pain."],
        "concerns": ["Is the pregnancy okay?", "Could this be ectopic?"]
    },
    "Case 28 - Sudden Testicular Pain": {
        "mood": "embarrassed",
        "hesitations": ["It's... my left testicle.", "Sorry, this is awkward."],
        "tangents": ["It started out of nowhere.", "I've never had this before."],
        "concerns": ["Am I going to lose the testicle?", "Do I need surgery?"]
    },
    "Case 29 - Racing Heart and Tingling": {
        "mood": "panicked",
        "hesitations": ["I can't slow my breathing.", "My hands are tingling."],
        "tangents": ["This happened once during exams too.", "I thought I was dying last time."],
        "concerns": ["Is this my heart?", "Am I having a panic attack?"]
    },
    "Case 30 - Facial Weakness": {
        "mood": "worried",
        "hesitations": ["I noticed it in the mirror.", "My face just feels strange."],
        "tangents": ["I had a cold last week.", "I can't close my eye properly."],
        "concerns": ["Is this a stroke?", "Will my face go back to normal?"]
    },
    "Case 31 - Jaw Pain and Headache": {
        "mood": "serious",
        "hesitations": ["It's a new headache for me.", "My jaw gets tired when I chew."],
        "tangents": ["My scalp even hurts when I brush my hair.", "The blurry vision scared me."],
        "concerns": ["Could I lose my sight?", "Why does chewing make my jaw hurt?"]
    },
    "Case 32 - Swollen Painful Calf": {
        "mood": "concerned",
        "hesitations": ["It's definitely more swollen than the other side.", "It started yesterday."],
        "tangents": ["I was sitting for hours on that coach.", "I noticed it when I got home."],
        "concerns": ["Could this be a blood clot?", "Can it travel to my lungs?"]
    },
}

def humanize_response(patient, selected_case, response):
    """Add personality without changing the clinical facts."""
    behavior = PATIENT_BEHAVIOR.get(selected_case, {})
    anxiety = patient["personality"].get("anxiety", "medium")
    talkativeness = patient["personality"].get("talkativeness", "medium")

    # Occasional hesitation before the answer.
    hesitation_chance = 0.10
    if anxiety in ["high", "very high"]:
        hesitation_chance = 0.20
    if random.random() < hesitation_chance and behavior.get("hesitations"):
        response = choose_response(behavior["hesitations"]) + " " + response

    # Chatty patients sometimes volunteer a harmless extra detail.
    tangent_chance = {
        "low": 0.03,
        "medium": 0.08,
        "high": 0.16
    }.get(talkativeness, 0.08)

    if random.random() < tangent_chance and behavior.get("tangents"):
        response += " " + choose_response(behavior["tangents"])

    # Worried patients occasionally ask the student something back.
    concern_chance = 0.03
    if anxiety == "medium":
        concern_chance = 0.06
    elif anxiety == "high":
        concern_chance = 0.10
    elif anxiety == "very high":
        concern_chance = 0.14

    if random.random() < concern_chance and behavior.get("concerns"):
        response += " " + choose_response(behavior["concerns"])

    return response



# =========================================================
# ADVANCED CLINICAL-REASONING FEATURES
# =========================================================

DIFFERENTIAL_CATALOG = {
    "Case 01 - Abdominal Pain": ["Gastroenteritis", "Ectopic pregnancy", "Ovarian torsion", "Renal colic"],
    "Case 02 - Chest Pain": ["Unstable angina", "Pulmonary embolism", "Aortic dissection", "Pericarditis"],
    "Case 03 - Shortness of Breath": ["Pneumonia", "Pneumothorax", "Pulmonary embolism", "Anaphylaxis"],
    "Case 04 - Fever and Cough": ["Viral respiratory infection", "Asthma exacerbation", "Pulmonary embolism", "Heart failure"],
    "Case 05 - Sudden Breathlessness": ["Pneumothorax", "Acute coronary syndrome", "Pneumonia", "Panic attack"],
    "Case 06 - Recurrent Headache": ["Tension headache", "Cluster headache", "Subarachnoid haemorrhage", "Meningitis"],
    "Case 07 - Sudden Severe Headache": ["Migraine", "Meningitis", "Cerebral venous sinus thrombosis", "Intracerebral haemorrhage"],
    "Case 08 - Sudden Weakness": ["Intracerebral haemorrhage", "Hypoglycaemia", "Todd paralysis", "Migraine with aura"],
    "Case 09 - Fever and Flank Pain": ["Renal colic", "Cystitis", "Appendicitis", "Pelvic inflammatory disease"],
    "Case 10 - Colicky Flank Pain": ["Pyelonephritis", "Abdominal aortic aneurysm", "Musculoskeletal pain", "Appendicitis"],
    "Case 11 - Right Upper Abdominal Pain": ["Biliary colic", "Cholangitis", "Hepatitis", "Peptic ulcer disease"],
    "Case 12 - Severe Epigastric Pain": ["Perforated peptic ulcer", "Acute coronary syndrome", "Cholecystitis", "Mesenteric ischaemia"],
    "Case 13 - Black Stools": ["Gastritis", "Oesophageal varices", "Upper GI malignancy", "Mallory-Weiss tear"],
    "Case 14 - Chronic Diarrhoea": ["Ulcerative colitis", "Coeliac disease", "IBS", "Chronic infection"],
    "Case 15 - Bloody Diarrhoea": ["Crohn disease", "Infectious colitis", "Ischaemic colitis", "Colorectal cancer"],
    "Case 16 - Thirst and Vomiting": ["Hyperosmolar hyperglycaemic state", "Gastroenteritis", "Sepsis", "Lactic acidosis"],
    "Case 17 - Confusion and Sweating": ["Stroke", "Sepsis", "Syncope", "Drug intoxication"],
    "Case 18 - Palpitations and Weight Loss": ["Anxiety disorder", "Atrial fibrillation", "Phaeochromocytoma", "Anaemia"],
    "Case 19 - Tiredness and Weight Gain": ["Depression", "Iron-deficiency anaemia", "Cushing syndrome", "Sleep apnoea"],
    "Case 20 - Fatigue and Breathlessness": ["B12 deficiency", "Hypothyroidism", "Chronic disease anaemia", "Haemoglobinopathy"],
    "Case 21 - Sudden Rash and Breathing Difficulty": ["Severe asthma", "Panic attack", "Angioedema", "Pulmonary embolism"],
    "Case 22 - Fever, Headache and Stiff Neck": ["Viral meningitis", "Subarachnoid haemorrhage", "Encephalitis", "Migraine"],
    "Case 23 - Sore Throat and Fatigue": ["Streptococcal pharyngitis", "CMV infection", "Acute HIV infection", "Tonsillitis"],
    "Case 24 - Spinning Dizziness": ["Vestibular neuritis", "Ménière disease", "Posterior circulation stroke", "Labyrinthitis"],
    "Case 25 - Red Painful Leg": ["DVT", "Contact dermatitis", "Venous stasis dermatitis", "Necrotising soft-tissue infection"],
    "Case 26 - Sudden Hot Joint": ["Septic arthritis", "Pseudogout", "Trauma", "Reactive arthritis"],
    "Case 27 - Lower Abdominal Pain and Bleeding": ["Miscarriage", "Ovarian torsion", "Pelvic inflammatory disease", "Ruptured ovarian cyst"],
    "Case 28 - Sudden Testicular Pain": ["Epididymitis", "Torsion of appendix testis", "Incarcerated hernia", "Trauma"],
    "Case 29 - Racing Heart and Tingling": ["Arrhythmia", "Hyperthyroidism", "Pulmonary embolism", "Hypoglycaemia"],
    "Case 30 - Facial Weakness": ["Stroke", "Ramsay Hunt syndrome", "Lyme disease", "Parotid lesion"],
    "Case 31 - Jaw Pain and Headache": ["Migraine", "Temporomandibular disorder", "Tension headache", "Carotid disease"],
    "Case 32 - Swollen Painful Calf": ["Cellulitis", "Ruptured Baker cyst", "Muscle strain", "Superficial thrombophlebitis"],
}

RED_FLAG_FEEDBACK = {
    "Case 02 - Chest Pain": "Chest pain with autonomic symptoms should trigger urgent ACS assessment and ECG.",
    "Case 05 - Sudden Breathlessness": "Sudden dyspnoea with thromboembolic risk factors can represent a life-threatening PE.",
    "Case 07 - Sudden Severe Headache": "A thunderclap headache is a neurological emergency until subarachnoid haemorrhage is excluded.",
    "Case 08 - Sudden Weakness": "New focal neurological deficit is time-critical: establish last-known-well time and activate the stroke pathway.",
    "Case 13 - Black Stools": "GI bleeding can deteriorate quickly; haemodynamic assessment and resuscitation come first.",
    "Case 16 - Thirst and Vomiting": "DKA requires urgent fluids, insulin, potassium monitoring and repeated biochemical reassessment.",
    "Case 17 - Confusion and Sweating": "Always check bedside glucose early in altered consciousness.",
    "Case 21 - Sudden Rash and Breathing Difficulty": "Airway/breathing compromise with an allergic reaction requires immediate IM adrenaline.",
    "Case 22 - Fever, Headache and Stiff Neck": "Suspected bacterial meningitis is time-critical; do not delay antibiotics for investigations.",
    "Case 27 - Lower Abdominal Pain and Bleeding": "Pregnancy plus abdominal pain/bleeding must be treated as ectopic pregnancy until excluded.",
    "Case 28 - Sudden Testicular Pain": "Suspected testicular torsion is a surgical emergency; do not delay definitive review for unnecessary tests.",
    "Case 31 - Jaw Pain and Headache": "Visual symptoms in suspected giant cell arteritis require immediate steroids and urgent ophthalmic assessment.",
    "Case 32 - Swollen Painful Calf": "Consider PE symptoms in any patient with suspected or confirmed DVT.",
}

EXAM_SYSTEM_KEYWORDS = {
    "General appearance": ["patient", "appears", "distressed", "unwell", "comfortable", "pale", "sweaty", "dehydrated", "lies", "alert"],
    "Cardiovascular": ["heart", "cardiac", "pulse", "jvp", "murmur", "capillary", "perfusion"],
    "Respiratory": ["chest", "lung", "breath", "wheeze", "crackle", "air entry", "respiratory"],
    "Abdominal": ["abdomen", "abdominal", "tender", "guarding", "rebound", "murphy", "bowel", "mass", "rigidity"],
    "Neurological": ["neurolog", "power", "weakness", "sensation", "reflex", "cranial", "speech", "gcs", "coordination", "nystagmus"],
    "Peripheral / vascular": ["leg", "calf", "oedema", "edema", "swelling", "warm", "erythema", "peripheral", "dorsalis", "vein"],
    "Head, neck & ENT": ["throat", "tonsil", "neck", "lymph", "temporal", "scalp", "ear", "facial"],
    "Eyes": ["eye", "pupil", "fund", "vision", "visual", "optic"],
    "Genitourinary / pelvic": ["test", "scrot", "pelvic", "cervix", "adnex", "vaginal"],
    "Skin": ["skin", "rash", "urticaria", "lesion"],
}

QUESTION_NORMALISATIONS = {
    "does it move anywhere": "does the pain radiate",
    "does the pain move": "does the pain radiate",
    "does it spread": "does the pain radiate",
    "where does it go": "does the pain radiate",
    "when did this begin": "when did it start",
    "when did this come on": "when did it start",
    "what makes it better": "what relieves it",
    "anything help": "what relieves it",
    "what makes it worse": "what aggravates it",
    "anything worsen": "what aggravates it",
    "how bad": "severity",
    "out of ten": "severity",
    "what does it feel like": "character",
    "describe the pain": "character",
    "pee": "urine",
    "passing water": "urine",
    "poo": "bowels",
    "stool": "bowels",
    "meds": "medications",
    "tablets": "medications",
    "drug allergies": "allergies",
    "drink alcohol": "alcohol",
    "smoke cigarettes": "smoking",
    "any conditions": "medical history",
    "health problems": "medical history",
}

def normalise_question(text):
    q = re.sub(r"[^a-z0-9\s]", " ", text.lower())
    q = re.sub(r"\s+", " ", q).strip()
    for source, target in QUESTION_NORMALISATIONS.items():
        if source in q:
            q = q.replace(source, target)
    return q

def phrase_similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def smart_intent_match(question):
    """Return the best INTENTS entry using phrases, token overlap and fuzzy similarity."""
    q = normalise_question(question)

    # Strong substring match first.
    for key, topic, phrases in INTENTS:
        if any(p in q for p in phrases):
            return key, topic

    q_tokens = set(q.split())
    best = None
    best_score = 0.0

    for key, topic, phrases in INTENTS:
        for phrase in phrases:
            p = normalise_question(phrase)
            p_tokens = set(p.split())
            overlap = len(q_tokens & p_tokens) / max(len(p_tokens), 1)
            fuzzy = phrase_similarity(q, p)
            score = max(overlap, fuzzy * 0.78)
            if score > best_score:
                best_score = score
                best = (key, topic)

    return best if best_score >= 0.52 else None

def classify_exam_findings(findings):
    grouped = {name: [] for name in EXAM_SYSTEM_KEYWORDS}
    grouped["Other focused findings"] = []

    for finding in findings:
        low = finding.lower()
        matched_systems = []
        for system, words in EXAM_SYSTEM_KEYWORDS.items():
            if any(word in low for word in words):
                matched_systems.append(system)

        if matched_systems:
            # Put each finding in the most specific first matching system.
            grouped[matched_systems[0]].append(finding)
        else:
            grouped["Other focused findings"].append(finding)

    return {k: v for k, v in grouped.items() if v}

def update_patient_emotion(question):
    """Simple consultation dynamics: empathy builds trust; dismissive language reduces it."""
    q = question.lower()

    empathic = [
        "sorry", "that sounds difficult", "that sounds painful", "i understand",
        "thank you for telling me", "take your time", "i'm here to help",
        "we'll look after you", "are you worried", "what worries you"
    ]
    dismissive = [
        "calm down", "just relax", "you're fine", "nothing wrong",
        "stop worrying", "don't be dramatic", "hurry up"
    ]

    if any(p in q for p in empathic):
        st.session_state.patient_trust = min(3, st.session_state.patient_trust + 1)
    if any(p in q for p in dismissive):
        st.session_state.patient_trust = max(-3, st.session_state.patient_trust - 1)

def emotion_label(patient, trust):
    base = patient.get("personality", {}).get("anxiety", "medium")
    if trust >= 2:
        return "more reassured and open"
    if trust <= -2:
        return "guarded and less comfortable"
    if base in ["high", "very high"]:
        return "visibly anxious"
    if base == "low":
        return "fairly calm"
    return "a little concerned"

def case_handover(patient):
    return (
        f"You are the medical student seeing **{patient['name']}**, "
        f"a **{patient['age']}-year-old** patient in the **{patient['setting']}**. "
        f"The presenting complaint documented at triage is: **“{patient['chief_complaint']}”** "
        "Take a focused history, examine appropriately, request investigations, and formulate a plan."
    )

def make_clinical_note(patient, selected_case, discovered_topics, revealed_data, ordered_tests, diagnosis_text, management):
    lines = []
    lines.append("CLINICAL CLERKING NOTE — EDUCATIONAL SIMULATION")
    lines.append("=" * 54)
    lines.append(f"Patient: {patient['name']}, age {patient['age']}")
    lines.append(f"Setting: {patient['setting']}")
    lines.append(f"Presenting complaint: {patient['chief_complaint']}")
    lines.append("")
    lines.append("HISTORY")
    if discovered_topics:
        lines.append("Domains elicited: " + ", ".join(sorted(discovered_topics)) + ".")
    else:
        lines.append("No structured history domains were recorded.")
    lines.append("")
    lines.append("EXAMINATION")
    clinical = EXAM_DATA.get(selected_case, {})
    if "vitals" in revealed_data:
        lines.extend(["- " + x for x in clinical.get("vitals", [])])
    examined_systems = [x.split("exam:", 1)[1] for x in revealed_data if x.startswith("exam:")]
    grouped = classify_exam_findings(clinical.get("examination", []))
    for system in examined_systems:
        for finding in grouped.get(system, []):
            lines.append(f"- {system}: {finding}")
    if "examination" in revealed_data and not examined_systems:
        lines.extend(["- " + x for x in clinical.get("examination", [])])
    if "vitals" not in revealed_data and not examined_systems and "examination" not in revealed_data:
        lines.append("No examination findings recorded.")
    lines.append("")
    lines.append("INVESTIGATIONS")
    if ordered_tests:
        for name, info in ordered_tests.items():
            lines.append(f"- {name}: {info['result']}")
    else:
        lines.append("No investigations ordered.")
    lines.append("")
    lines.append("ASSESSMENT")
    lines.append(f"Working diagnosis: {diagnosis_text or patient['diagnosis_display']}")
    lines.append("")
    lines.append("PLAN")
    if management:
        lines.extend(["- " + action for action in management])
    else:
        lines.append("Management plan not yet submitted.")
    return "\n".join(lines)


# =========================================================
# HELPERS
# =========================================================

def contains_any(text, phrases):
    return any(phrase in text for phrase in phrases)

def choose_response(options):
    return random.choice(options)

def reset_consultation():
    st.session_state.messages = []
    st.session_state.topics_asked = set()
    st.session_state.consultation_finished = False
    st.session_state.diagnosis_submitted = False
    st.session_state.diagnosis_correct = False
    st.session_state.revealed_clinical_data = set()
    st.session_state.ordered_tests = {}
    st.session_state.selected_management = []
    st.session_state.management_submitted = False
    st.session_state.differentials = ["", "", ""]
    st.session_state.differentials_submitted = False
    st.session_state.patient_trust = 0
    st.session_state.final_diagnosis_text = ""
    st.session_state.management_score = None

def get_response_options(patient, key):
    return patient.get("responses", {}).get(key, DEFAULT_RESPONSES.get(key, ["I'm not sure."]))

def apply_personality(patient, response):
    anxiety = patient["personality"].get("anxiety", "medium")
    talkativeness = patient["personality"].get("talkativeness", "medium")

    if anxiety in ["high", "very high"] and random.random() < 0.10:
        response += " I'm quite worried about this."
    elif anxiety == "medium" and random.random() < 0.04:
        response += " I'm a little worried."

    if talkativeness == "high" and random.random() < 0.08:
        response += " Sorry, I know I'm talking a lot."
    return response

def theme_css(theme):
    return f"""
    <style>
    .stApp {{
        background-color: {theme["background"]};
    }}
    h1, h2, h3 {{
        color: {theme["accent"]};
    }}
    div[data-testid="stAlert"] {{
        background-color: {theme["card"]};
        border: 1px solid {theme["secondary"]};
        border-radius: 16px;
    }}
    div.stButton > button {{
        background-color: {theme["button"]};
        color: white;
        border: none;
        border-radius: 12px;
        font-weight: 600;
    }}
    div.stButton > button:hover {{
        filter: brightness(0.92);
        color: white;
        border: none;
    }}
    div[data-testid="stChatMessage"] {{
        border-radius: 16px;
    }}
    </style>
    """


def show_test_visual(selected_case, test_name, difficulty):
    visual = VISUAL_ASSETS.get(selected_case, {}).get(test_name)

    if not visual:
        return

    image_path = Path(__file__).resolve().parent / visual["file"]

    if image_path.exists():
        st.image(
            str(image_path),
            caption=visual["caption"],
            use_container_width=True
        )

        # Teaching notes are deliberately hidden in OSCE / Hard mode.
        if difficulty == "Easy":
            st.caption("💡 " + visual["teaching_note"])

    else:
        st.info(
            f"🖼️ Visual available for this investigation, but the image file "
            f"`{visual['file']}` has not been added yet."
        )



# =========================================================
# MANAGEMENT / TREATMENT STAGE
#
# "essential" = core immediate / first-line action
# "useful"    = appropriate adjunct, referral, monitoring, or follow-up
# "harmful"   = inappropriate, unsafe, or unnecessarily delaying action
#
# This is a simplified educational model for simulated cases.
# =========================================================

MANAGEMENT_CATALOG = {
    "Case 01 - Abdominal Pain": {
        "Keep nil by mouth and obtain surgical review": {"value": "essential", "feedback": "Appropriate while appendicitis is being assessed for operative management."},
        "IV fluids": {"value": "useful", "feedback": "Useful if the patient is dehydrated or unable to maintain oral intake."},
        "Analgesia and antiemetic": {"value": "useful", "feedback": "Pain and nausea should be treated rather than withheld."},
        "IV antibiotics according to local surgical protocol": {"value": "essential", "feedback": "Appropriate once acute appendicitis is established, especially around operative management."},
        "Laparoscopic appendicectomy / urgent surgical management": {"value": "essential", "feedback": "Definitive management for uncomplicated acute appendicitis in this simulated case."},
        "Send home with laxatives only": {"value": "harmful", "feedback": "This would delay treatment of a surgical abdomen."},
    },

    "Case 02 - Chest Pain": {
        "Activate urgent reperfusion / PCI pathway": {"value": "essential", "feedback": "ST-elevation myocardial infarction requires urgent reperfusion."},
        "Aspirin if no contraindication": {"value": "essential", "feedback": "Immediate antiplatelet therapy is a core part of ACS management."},
        "Continuous cardiac monitoring and IV access": {"value": "essential", "feedback": "Appropriate in an acute myocardial infarction."},
        "GTN for ongoing pain if blood pressure permits": {"value": "useful", "feedback": "May help ischaemic pain when haemodynamics allow."},
        "High-intensity statin": {"value": "useful", "feedback": "Appropriate secondary-prevention therapy."},
        "Routine antibiotics": {"value": "harmful", "feedback": "There is no evidence of infection requiring antibiotics."},
    },

    "Case 03 - Shortness of Breath": {
        "Controlled oxygen if hypoxaemic": {"value": "essential", "feedback": "Oxygen is appropriate when saturation is low."},
        "Repeated inhaled/nebulised short-acting beta-2 agonist": {"value": "essential", "feedback": "First-line bronchodilator treatment in acute asthma."},
        "Add inhaled ipratropium in a significant exacerbation": {"value": "useful", "feedback": "Useful in moderate-to-severe exacerbations."},
        "Systemic corticosteroid": {"value": "essential", "feedback": "Early systemic steroids reduce relapse and speed recovery."},
        "Reassess peak flow, work of breathing and oxygenation": {"value": "essential", "feedback": "Frequent reassessment is important because asthma can deteriorate."},
        "Sedate the patient to slow breathing": {"value": "harmful", "feedback": "Sedation can worsen respiratory compromise."},
    },

    "Case 04 - Fever and Cough": {
        "Start appropriate empiric antibiotics": {"value": "essential", "feedback": "The presentation is consistent with bacterial community-acquired pneumonia."},
        "Give oxygen if hypoxaemic": {"value": "essential", "feedback": "Her oxygen saturation is below normal."},
        "Fluids and antipyretic/analgesic care": {"value": "useful", "feedback": "Supportive care is appropriate."},
        "Assess severity and need for admission": {"value": "essential", "feedback": "Severity assessment guides site and intensity of care."},
        "Review cultures and narrow antibiotics when appropriate": {"value": "useful", "feedback": "Antimicrobial stewardship is appropriate once results are available."},
        "Treat with bronchodilator alone": {"value": "harmful", "feedback": "This would not address the likely bacterial pneumonia."},
    },

    "Case 05 - Sudden Breathlessness": {
        "Start therapeutic anticoagulation if no contraindication": {"value": "essential", "feedback": "Confirmed pulmonary embolism generally requires therapeutic anticoagulation."},
        "Give oxygen if hypoxaemic": {"value": "essential", "feedback": "The patient is hypoxaemic."},
        "Assess haemodynamic stability and PE severity": {"value": "essential", "feedback": "This determines whether escalation such as thrombolysis is needed."},
        "Analgesia": {"value": "useful", "feedback": "Pleuritic pain can be treated symptomatically."},
        "Escalate urgently if shock develops": {"value": "useful", "feedback": "Haemodynamic deterioration changes management substantially."},
        "Send home without anticoagulation": {"value": "harmful", "feedback": "A confirmed PE requires treatment unless there is a specific contraindication."},
    },

    "Case 06 - Recurrent Headache": {
        "Treat early with an appropriate simple analgesic or NSAID if suitable": {"value": "essential", "feedback": "Acute migraine treatment should be given early when possible."},
        "Consider a triptan if suitable": {"value": "essential", "feedback": "A triptan is an appropriate migraine-specific option in many patients."},
        "Antiemetic if nausea is troublesome": {"value": "useful", "feedback": "This can improve symptoms and medication tolerance."},
        "Discuss trigger management and headache diary": {"value": "useful", "feedback": "Useful for recurrent migraine."},
        "Consider preventive therapy if attacks are frequent/disabling": {"value": "useful", "feedback": "Prophylaxis may be appropriate depending on frequency and impact."},
        "Emergency neurosurgery": {"value": "harmful", "feedback": "The case has typical migraine features and a normal neurological examination."},
    },

    "Case 07 - Sudden Severe Headache": {
        "Urgent neurosurgical / neurovascular referral": {"value": "essential", "feedback": "Subarachnoid haemorrhage requires urgent specialist management."},
        "Stabilise airway, breathing and circulation": {"value": "essential", "feedback": "Initial stabilisation is essential."},
        "Give nimodipine unless contraindicated": {"value": "essential", "feedback": "Nimodipine is used to reduce delayed cerebral ischaemia after aneurysmal SAH."},
        "Control pain, nausea and severe hypertension carefully": {"value": "useful", "feedback": "Supportive physiological management is important."},
        "Definitive aneurysm securing by coiling or clipping": {"value": "essential", "feedback": "The bleeding source needs definitive treatment."},
        "Discharge with migraine medication": {"value": "harmful", "feedback": "A thunderclap headache with SAH requires emergency treatment."},
    },

    "Case 08 - Sudden Weakness": {
        "Activate acute stroke pathway": {"value": "essential", "feedback": "Time-sensitive stroke treatment requires immediate pathway activation."},
        "Determine eligibility for IV thrombolysis": {"value": "essential", "feedback": "The patient is within a potential treatment window if no contraindication exists."},
        "Urgent thrombectomy assessment for large-vessel occlusion": {"value": "essential", "feedback": "CTA shows an MCA occlusion, so thrombectomy assessment is crucial."},
        "Swallow screen before oral intake": {"value": "useful", "feedback": "Dysphagia screening reduces aspiration risk."},
        "Secondary prevention after acute treatment": {"value": "useful", "feedback": "Risk-factor management and antithrombotic planning are important."},
        "Rapidly lower blood pressure to normal in every case": {"value": "harmful", "feedback": "Overly aggressive BP reduction can be harmful in acute ischaemic stroke."},
    },

    "Case 09 - Fever and Flank Pain": {
        "Start appropriate antibiotics": {"value": "essential", "feedback": "Acute pyelonephritis requires antimicrobial treatment."},
        "Encourage/replace fluids as appropriate": {"value": "useful", "feedback": "Hydration is useful, particularly if oral intake is poor."},
        "Analgesia and antipyretics": {"value": "useful", "feedback": "Symptom control is appropriate."},
        "Review urine culture and sensitivities": {"value": "essential", "feedback": "Therapy should be adjusted to microbiology when available."},
        "Assess for sepsis or obstruction": {"value": "essential", "feedback": "Complicated infection or sepsis requires escalation."},
        "Treat with laxatives": {"value": "harmful", "feedback": "This would not treat an upper urinary tract infection."},
    },

    "Case 10 - Colicky Flank Pain": {
        "NSAID analgesia if not contraindicated": {"value": "essential", "feedback": "NSAIDs are effective first-line analgesia for renal colic."},
        "Antiemetic if needed": {"value": "useful", "feedback": "Nausea and vomiting are common and can be treated."},
        "Encourage normal hydration rather than forced fluids": {"value": "useful", "feedback": "Forced excessive fluids do not speed stone passage."},
        "Safety-net for fever, anuria or worsening pain": {"value": "essential", "feedback": "These may indicate obstruction with infection or another complication."},
        "Urology review if obstruction, infection, renal impairment or uncontrolled pain": {"value": "essential", "feedback": "Complicated stones require specialist intervention."},
        "Start antibiotics routinely despite no infection": {"value": "harmful", "feedback": "Antibiotics are not indicated without evidence of infection."},
    },

    "Case 11 - Right Upper Abdominal Pain": {
        "Keep nil by mouth initially": {"value": "useful", "feedback": "Useful during acute surgical assessment."},
        "IV fluids as needed": {"value": "useful", "feedback": "Appropriate if oral intake is poor or the patient is dehydrated."},
        "Analgesia and antiemetic": {"value": "essential", "feedback": "Symptom control is part of acute management."},
        "Antibiotics when acute cholecystitis is suspected/confirmed": {"value": "essential", "feedback": "Antimicrobial treatment is appropriate in this infected/inflamed gallbladder presentation."},
        "Early surgical review for laparoscopic cholecystectomy": {"value": "essential", "feedback": "Definitive management generally involves cholecystectomy."},
        "Discharge with antacids only": {"value": "harmful", "feedback": "This would delay treatment of acute cholecystitis."},
    },

    "Case 12 - Severe Epigastric Pain": {
        "IV crystalloid fluid resuscitation": {"value": "essential", "feedback": "Early fluid management is important in acute pancreatitis."},
        "Adequate analgesia": {"value": "essential", "feedback": "Pain control is a core part of treatment."},
        "Antiemetic and electrolyte monitoring": {"value": "useful", "feedback": "Vomiting and metabolic disturbances are common."},
        "Early oral/enteral nutrition as tolerated": {"value": "useful", "feedback": "Prolonged unnecessary fasting is generally avoided."},
        "Identify and treat the underlying cause": {"value": "essential", "feedback": "Alcohol, gallstones, triglycerides and other causes should be addressed."},
        "Routine prophylactic antibiotics for sterile pancreatitis": {"value": "harmful", "feedback": "Routine antibiotics are not indicated in uncomplicated sterile pancreatitis."},
    },

    "Case 13 - Black Stools": {
        "ABC resuscitation and large-bore IV access": {"value": "essential", "feedback": "GI bleeding can become haemodynamically unstable."},
        "IV fluids and blood products when indicated": {"value": "essential", "feedback": "Resuscitation should be guided by haemodynamics and haemoglobin."},
        "IV proton-pump inhibitor according to local protocol": {"value": "essential", "feedback": "PPI therapy is appropriate in suspected peptic ulcer bleeding."},
        "Urgent upper GI endoscopy with haemostasis if required": {"value": "essential", "feedback": "Endoscopy is diagnostic and potentially therapeutic."},
        "Stop NSAIDs where possible": {"value": "useful", "feedback": "NSAIDs are an important ulcer/bleeding risk factor."},
        "Give more ibuprofen for epigastric pain": {"value": "harmful", "feedback": "NSAIDs can worsen peptic ulcer bleeding."},
    },

    "Case 14 - Chronic Diarrhoea": {
        "Gastroenterology-led induction therapy": {"value": "essential", "feedback": "Active Crohn disease requires disease-modifying treatment tailored to severity."},
        "Assess nutrition, iron and vitamin deficiencies": {"value": "useful", "feedback": "Malnutrition and micronutrient deficiency are common."},
        "Smoking cessation if applicable": {"value": "useful", "feedback": "Smoking worsens Crohn disease outcomes."},
        "Consider corticosteroids for induction when appropriate": {"value": "essential", "feedback": "Steroids are commonly used for induction, not long-term maintenance."},
        "Plan maintenance therapy and monitoring": {"value": "essential", "feedback": "Relapsing inflammatory bowel disease needs long-term follow-up."},
        "Long-term NSAIDs for abdominal pain": {"value": "harmful", "feedback": "NSAIDs may exacerbate inflammatory bowel disease."},
    },

    "Case 15 - Bloody Diarrhoea": {
        "Assess flare severity and hydration": {"value": "essential", "feedback": "Severity determines outpatient versus inpatient management."},
        "5-ASA therapy for appropriate mild-to-moderate disease": {"value": "essential", "feedback": "Mesalazine is a common first-line treatment in appropriate UC flares."},
        "Systemic corticosteroids for a significant flare": {"value": "useful", "feedback": "Steroids may be required for moderate/severe active disease."},
        "VTE prophylaxis if admitted unless contraindicated": {"value": "useful", "feedback": "Hospitalised active IBD carries increased thrombosis risk."},
        "Gastroenterology follow-up and maintenance plan": {"value": "essential", "feedback": "Long-term control and surveillance are important."},
        "Antidiarrhoeal medication alone in severe colitis": {"value": "harmful", "feedback": "This can be dangerous in severe colitis and does not treat inflammation."},
    },

    "Case 16 - Thirst and Vomiting": {
        "IV 0.9% sodium chloride fluid resuscitation": {"value": "essential", "feedback": "Fluid replacement is the first major treatment step in DKA."},
        "Fixed-rate IV insulin infusion after initial assessment": {"value": "essential", "feedback": "Insulin is required to stop ketogenesis."},
        "Frequent potassium monitoring and replacement as indicated": {"value": "essential", "feedback": "Potassium can change rapidly during DKA treatment."},
        "Frequent glucose, ketone and acid-base monitoring": {"value": "essential", "feedback": "Response to treatment must be monitored closely."},
        "Identify and treat the precipitating cause": {"value": "useful", "feedback": "Missed insulin, infection and other triggers should be addressed."},
        "Give a large insulin bolus without fluids or potassium monitoring": {"value": "harmful", "feedback": "This is unsafe and does not follow standard DKA treatment principles."},
    },

    "Case 17 - Confusion and Sweating": {
        "Give rapid-acting glucose if able to swallow safely": {"value": "essential", "feedback": "Immediate glucose treatment is required."},
        "Use IV dextrose or glucagon if unable to take oral glucose": {"value": "essential", "feedback": "A parenteral route is needed if consciousness or swallowing is impaired."},
        "Recheck capillary glucose after treatment": {"value": "essential", "feedback": "Confirm that hypoglycaemia has resolved."},
        "Give longer-acting carbohydrate once recovered": {"value": "useful", "feedback": "This reduces recurrent hypoglycaemia when appropriate."},
        "Review insulin regimen and missed meals": {"value": "useful", "feedback": "The precipitating cause should be addressed."},
        "Give more insulin": {"value": "harmful", "feedback": "Additional insulin would worsen hypoglycaemia."},
    },

    "Case 18 - Palpitations and Weight Loss": {
        "Beta-blocker for symptomatic adrenergic symptoms if suitable": {"value": "useful", "feedback": "This can reduce tremor and palpitations."},
        "Start appropriate antithyroid therapy": {"value": "essential", "feedback": "Thionamide therapy is a standard treatment option for hyperthyroidism."},
        "Endocrinology review": {"value": "essential", "feedback": "Cause, severity and longer-term treatment need specialist assessment."},
        "Discuss definitive options when appropriate": {"value": "useful", "feedback": "Radioiodine or surgery may be considered in selected patients."},
        "Monitor thyroid function tests": {"value": "essential", "feedback": "Biochemical response and overtreatment need monitoring."},
        "Start levothyroxine as sole initial treatment": {"value": "harmful", "feedback": "Levothyroxine would worsen untreated hyperthyroidism."},
    },

    "Case 19 - Tiredness and Weight Gain": {
        "Start levothyroxine": {"value": "essential", "feedback": "Thyroxine replacement is standard treatment for primary hypothyroidism."},
        "Recheck TSH after an appropriate interval": {"value": "essential", "feedback": "Dose adjustment is guided by follow-up thyroid function."},
        "Counsel on how to take levothyroxine consistently": {"value": "useful", "feedback": "Absorption is affected by food and other medications."},
        "Screen for associated autoimmune disease when clinically appropriate": {"value": "useful", "feedback": "Autoimmune conditions can coexist."},
        "Long-term follow-up": {"value": "useful", "feedback": "Most patients require ongoing replacement and monitoring."},
        "Start antithyroid medication": {"value": "harmful", "feedback": "Antithyroid medication would worsen hypothyroidism."},
    },

    "Case 20 - Fatigue and Breathlessness": {
        "Start iron replacement": {"value": "essential", "feedback": "Confirmed iron deficiency requires iron repletion."},
        "Look for the underlying source of iron deficiency": {"value": "essential", "feedback": "Treatment should not stop at replacing iron; the cause must be established."},
        "Dietary counselling on iron intake": {"value": "useful", "feedback": "Helpful as an adjunct, though not a substitute for treating significant deficiency."},
        "Repeat FBC and iron studies to document response": {"value": "essential", "feedback": "Response to therapy should be confirmed."},
        "Consider IV iron if oral therapy is unsuitable or ineffective": {"value": "useful", "feedback": "IV iron is appropriate in selected situations."},
        "Start folic acid alone despite normal folate": {"value": "harmful", "feedback": "This does not treat iron deficiency."},
    },

    "Case 21 - Sudden Rash and Breathing Difficulty": {
        "IM adrenaline immediately": {"value": "essential", "feedback": "Intramuscular adrenaline is first-line treatment for anaphylaxis."},
        "Call for emergency help and manage ABC": {"value": "essential", "feedback": "Anaphylaxis can deteriorate rapidly."},
        "High-flow oxygen": {"value": "essential", "feedback": "The patient is hypoxaemic."},
        "IV crystalloid bolus for hypotension": {"value": "essential", "feedback": "Fluid resuscitation is appropriate in anaphylactic shock."},
        "Repeat IM adrenaline if symptoms persist according to protocol": {"value": "useful", "feedback": "Repeated doses may be needed."},
        "Give antihistamine alone and wait": {"value": "harmful", "feedback": "Antihistamines do not replace adrenaline in anaphylaxis."},
    },

    "Case 22 - Fever, Headache and Stiff Neck": {
        "Start empiric IV antibiotics promptly": {"value": "essential", "feedback": "Suspected bacterial meningitis is time-critical."},
        "Give dexamethasone according to protocol": {"value": "essential", "feedback": "Early corticosteroid therapy is appropriate in selected bacterial meningitis presentations."},
        "Take blood cultures without delaying antibiotics": {"value": "useful", "feedback": "Cultures are valuable but treatment should not be delayed."},
        "Support airway, breathing, circulation and fluids": {"value": "essential", "feedback": "Sepsis and neurological deterioration can occur."},
        "Use infection-control precautions when indicated": {"value": "useful", "feedback": "Some bacterial causes require droplet precautions and contact management."},
        "Wait for lumbar puncture results before giving antibiotics": {"value": "harmful", "feedback": "Antibiotics should not be delayed in a strongly suspected bacterial meningitis case."},
    },

    "Case 23 - Sore Throat and Fatigue": {
        "Supportive care with fluids and analgesia": {"value": "essential", "feedback": "Most EBV infectious mononucleosis is treated supportively."},
        "Avoid contact sports while splenomegaly is a concern": {"value": "essential", "feedback": "This reduces risk of splenic rupture."},
        "Safety-net for abdominal pain, breathing difficulty or deterioration": {"value": "useful", "feedback": "Complications require reassessment."},
        "Avoid routine amoxicillin/ampicillin": {"value": "useful", "feedback": "These antibiotics can provoke a characteristic rash in EBV and are not routinely indicated."},
        "Steroids only for selected severe complications": {"value": "useful", "feedback": "They are not routine treatment but may be used for specific complications."},
        "Routine broad-spectrum antibiotics": {"value": "harmful", "feedback": "This viral illness does not routinely require antibiotics."},
    },

    "Case 24 - Spinning Dizziness": {
        "Perform a canalith repositioning manoeuvre": {"value": "essential", "feedback": "Epley-type manoeuvres are effective for posterior-canal BPPV."},
        "Explain the benign positional nature of the condition": {"value": "useful", "feedback": "Reassurance and education are helpful."},
        "Provide fall-safety advice during symptomatic periods": {"value": "useful", "feedback": "Vertigo can increase fall risk."},
        "Arrange reassessment if neurological red flags develop": {"value": "essential", "feedback": "New focal signs would suggest a central cause."},
        "Short-term vestibular suppressant only if severe symptoms require it": {"value": "useful", "feedback": "These are not the main definitive treatment."},
        "Emergency thrombolysis despite normal neuro exam": {"value": "harmful", "feedback": "The presentation is typical of peripheral positional vertigo, not stroke."},
    },

    "Case 25 - Red Painful Leg": {
        "Start appropriate antibiotics": {"value": "essential", "feedback": "Cellulitis is a bacterial skin/soft-tissue infection."},
        "Elevate the affected limb": {"value": "useful", "feedback": "This can reduce swelling."},
        "Analgesia": {"value": "useful", "feedback": "Pain should be treated."},
        "Mark/monitor the edge of erythema": {"value": "useful", "feedback": "Useful for tracking progression."},
        "Optimise diabetes control": {"value": "useful", "feedback": "Diabetes can impair infection outcomes."},
        "Incise the leg despite no abscess": {"value": "harmful", "feedback": "There is no drainable collection to incise."},
    },

    "Case 26 - Sudden Hot Joint": {
        "NSAID, colchicine, or corticosteroid for the acute attack as appropriate": {"value": "essential", "feedback": "Anti-inflammatory therapy is the main acute treatment."},
        "Rest and ice the joint": {"value": "useful", "feedback": "Supportive measures can reduce pain."},
        "Review contributing drugs and alcohol intake": {"value": "useful", "feedback": "Modifiable precipitants should be addressed."},
        "Consider long-term urate-lowering therapy based on recurrence/risk": {"value": "useful", "feedback": "Long-term therapy is considered after assessing overall gout burden."},
        "Exclude septic arthritis when clinically necessary": {"value": "essential", "feedback": "A hot swollen joint can be septic, which is a medical emergency."},
        "Start antibiotics automatically despite crystal-proven gout and no infection": {"value": "harmful", "feedback": "Antibiotics are not indicated without evidence of infection."},
    },

    "Case 27 - Lower Abdominal Pain and Bleeding": {
        "Urgent gynaecology review": {"value": "essential", "feedback": "Ectopic pregnancy is potentially life-threatening."},
        "Assess haemodynamic stability and establish IV access": {"value": "essential", "feedback": "Internal bleeding can cause rapid deterioration."},
        "Surgical management if unstable or rupture is suspected": {"value": "essential", "feedback": "Unstable/ruptured ectopic pregnancy requires urgent surgery."},
        "Consider methotrexate only if strict eligibility criteria are met": {"value": "useful", "feedback": "Medical management is appropriate only in selected stable cases."},
        "Check blood group/Rh and manage Rh status according to protocol": {"value": "useful", "feedback": "Rh status may influence management."},
        "Discharge without follow-up because bleeding is light": {"value": "harmful", "feedback": "Even light bleeding can accompany a dangerous ectopic pregnancy."},
    },

    "Case 28 - Sudden Testicular Pain": {
        "Immediate urology / surgical assessment": {"value": "essential", "feedback": "Testicular torsion is a time-critical surgical emergency."},
        "Urgent scrotal exploration and detorsion": {"value": "essential", "feedback": "Definitive treatment should not be delayed when torsion is strongly suspected."},
        "Bilateral orchidopexy during operative management": {"value": "essential", "feedback": "Fixation is commonly performed to reduce recurrence risk."},
        "Analgesia": {"value": "useful", "feedback": "Severe pain should be treated."},
        "Do not delay surgery for imaging if clinical suspicion is high": {"value": "essential", "feedback": "Time to detorsion matters for testicular salvage."},
        "Treat with antibiotics alone": {"value": "harmful", "feedback": "Antibiotics do not correct torsion."},
    },

    "Case 29 - Racing Heart and Tingling": {
        "Reassure after dangerous causes have been considered": {"value": "essential", "feedback": "Reassurance is appropriate once an acute medical cause has been excluded."},
        "Coach slow controlled breathing rather than paper-bag rebreathing": {"value": "essential", "feedback": "Controlled breathing can help hyperventilation; paper bags are unsafe."},
        "Reduce immediate environmental stressors": {"value": "useful", "feedback": "A calm environment can reduce symptoms."},
        "Discuss psychological follow-up if episodes recur": {"value": "useful", "feedback": "Recurrent panic attacks may benefit from CBT or other treatment."},
        "Safety-net for atypical or worsening chest symptoms": {"value": "useful", "feedback": "New red flags require reassessment."},
        "Use a paper bag for rebreathing": {"value": "harmful", "feedback": "Paper-bag rebreathing can be dangerous if the diagnosis is wrong or oxygenation is impaired."},
    },

    "Case 30 - Facial Weakness": {
        "Start oral corticosteroid promptly if appropriate": {"value": "essential", "feedback": "Early corticosteroids improve outcomes in Bell's palsy."},
        "Protect the affected eye": {"value": "essential", "feedback": "Lubrication and night-time protection prevent corneal injury when eye closure is weak."},
        "Explain expected recovery and arrange follow-up": {"value": "useful", "feedback": "Most patients improve, but follow-up identifies atypical recovery."},
        "Consider antiviral therapy in selected cases": {"value": "useful", "feedback": "This may be added in selected presentations, especially severe palsy or suspected zoster."},
        "Reassess urgently if other neurological deficits appear": {"value": "essential", "feedback": "Additional deficits would make an alternative diagnosis such as stroke more likely."},
        "Give thrombolysis for isolated complete LMN facial weakness": {"value": "harmful", "feedback": "This isolated peripheral facial palsy pattern is not an indication for thrombolysis."},
    },

    "Case 31 - Jaw Pain and Headache": {
        "Start high-dose corticosteroid immediately": {"value": "essential", "feedback": "Treatment should not wait for confirmatory biopsy when giant cell arteritis is strongly suspected."},
        "Urgent ophthalmology review for visual symptoms": {"value": "essential", "feedback": "Vision loss can become permanent."},
        "Arrange temporal artery imaging/biopsy without delaying treatment": {"value": "essential", "feedback": "Diagnostic confirmation is important but should not postpone steroids."},
        "Bone and gastric protection as appropriate during steroid therapy": {"value": "useful", "feedback": "Prolonged high-dose steroid treatment has important adverse effects."},
        "Monitor inflammatory markers and symptoms": {"value": "useful", "feedback": "Response and relapse need monitoring."},
        "Wait for biopsy before starting steroids": {"value": "harmful", "feedback": "Delay can risk irreversible visual loss."},
    },

    "Case 32 - Swollen Painful Calf": {
        "Start therapeutic anticoagulation if no contraindication": {"value": "essential", "feedback": "Confirmed proximal DVT requires treatment."},
        "Assess for PE symptoms and haemodynamic instability": {"value": "essential", "feedback": "A DVT can embolise to the lungs."},
        "Choose an appropriate anticoagulant and duration based on context": {"value": "essential", "feedback": "Duration depends on provoking factors, recurrence and bleeding risk."},
        "Encourage mobilisation when clinically appropriate": {"value": "useful", "feedback": "Routine prolonged bed rest is generally unnecessary once treatment begins."},
        "Review provoking factors and cancer history": {"value": "useful", "feedback": "Underlying risk factors influence duration and follow-up."},
        "Massage the swollen calf vigorously": {"value": "harmful", "feedback": "This is not a treatment and could worsen pain."},
    },
}

# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "topics_asked" not in st.session_state:
    st.session_state.topics_asked = set()

if "consultation_finished" not in st.session_state:
    st.session_state.consultation_finished = False

if "diagnosis_submitted" not in st.session_state:
    st.session_state.diagnosis_submitted = False

if "diagnosis_correct" not in st.session_state:
    st.session_state.diagnosis_correct = False

if "selected_management" not in st.session_state:
    st.session_state.selected_management = []

if "management_submitted" not in st.session_state:
    st.session_state.management_submitted = False

if "revealed_clinical_data" not in st.session_state:
    st.session_state.revealed_clinical_data = set()

if "ordered_tests" not in st.session_state:
    st.session_state.ordered_tests = {}

if "selected_case" not in st.session_state:
    st.session_state.selected_case = list(CASES.keys())[0]

if "difficulty" not in st.session_state:
    st.session_state.difficulty = "OSCE"

if "app_started" not in st.session_state:
    st.session_state.app_started = False


if "differentials" not in st.session_state:
    st.session_state.differentials = ["", "", ""]
if "differentials_submitted" not in st.session_state:
    st.session_state.differentials_submitted = False
if "patient_trust" not in st.session_state:
    st.session_state.patient_trust = 0
if "final_diagnosis_text" not in st.session_state:
    st.session_state.final_diagnosis_text = ""
if "management_score" not in st.session_state:
    st.session_state.management_score = None

# =========================================================
# HOME SCREEN
# =========================================================

if not st.session_state.app_started:

    st.markdown(
        """
        <style>
        /* ---------- GLOBAL HOME AESTHETIC ---------- */

        .stApp {
            background:
                radial-gradient(circle at 8% 8%, rgba(223, 210, 244, 0.65), transparent 28%),
                radial-gradient(circle at 92% 12%, rgba(210, 235, 244, 0.70), transparent 30%),
                radial-gradient(circle at 50% 100%, rgba(245, 222, 232, 0.45), transparent 32%),
                #FBFAFD;
        }

        [data-testid="stHeader"] {
            background: rgba(0,0,0,0);
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1050px;
        }

        /* ---------- HERO ---------- */

        .vp-hero {
            position: relative;
            overflow: hidden;
            padding: 38px 38px 32px 38px;
            border-radius: 30px;
            background:
                linear-gradient(135deg, rgba(255,255,255,0.97), rgba(247,243,252,0.95));
            border: 1px solid rgba(160, 137, 182, 0.18);
            box-shadow: 0 18px 50px rgba(89, 67, 107, 0.08);
            margin-bottom: 26px;
        }

        .vp-hero:before {
            content: "";
            position: absolute;
            width: 180px;
            height: 180px;
            border-radius: 50%;
            right: -55px;
            top: -65px;
            background: rgba(204, 228, 239, 0.55);
        }

        .vp-hero:after {
            content: "";
            position: absolute;
            width: 130px;
            height: 130px;
            border-radius: 50%;
            left: -45px;
            bottom: -58px;
            background: rgba(233, 212, 239, 0.55);
        }

        .vp-kicker {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 7px 13px;
            border-radius: 999px;
            background: #F0E9F7;
            color: #6C547E;
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.07em;
            text-transform: uppercase;
            margin-bottom: 16px;
        }

        .vp-title {
            position: relative;
            z-index: 2;
            font-size: clamp(2.25rem, 5vw, 4rem);
            line-height: 0.98;
            color: #302736;
            font-weight: 850;
            letter-spacing: -0.045em;
            margin: 0 0 16px 0;
            max-width: 760px;
        }

        .vp-title span {
            color: #795B91;
        }

        .vp-subtitle {
            position: relative;
            z-index: 2;
            color: #6E6474;
            font-size: 1.05rem;
            line-height: 1.65;
            max-width: 730px;
            margin: 0;
        }

        /* ---------- MINI STATS ---------- */

        .vp-stat {
            background: rgba(255,255,255,0.82);
            border: 1px solid rgba(163, 145, 177, 0.16);
            border-radius: 18px;
            padding: 15px 16px;
            text-align: center;
            min-height: 92px;
            box-shadow: 0 8px 26px rgba(74, 56, 87, 0.045);
        }

        .vp-stat-number {
            font-size: 1.38rem;
            font-weight: 850;
            color: #4A3B55;
            margin-bottom: 3px;
        }

        .vp-stat-label {
            font-size: 0.80rem;
            color: #84798A;
        }

        /* ---------- FLOW ---------- */

        .vp-section-title {
            font-size: 1.22rem;
            color: #403447;
            font-weight: 800;
            margin: 10px 0 12px 0;
        }

        .vp-flow-card {
            background: rgba(255,255,255,0.88);
            border: 1px solid rgba(163, 145, 177, 0.16);
            border-radius: 20px;
            padding: 17px 15px;
            min-height: 132px;
            box-shadow: 0 8px 26px rgba(74, 56, 87, 0.04);
        }

        .vp-flow-icon {
            font-size: 1.45rem;
            margin-bottom: 8px;
        }

        .vp-flow-step {
            font-size: 0.70rem;
            color: #9B8BA5;
            text-transform: uppercase;
            letter-spacing: 0.09em;
            font-weight: 800;
        }

        .vp-flow-title {
            margin-top: 4px;
            font-size: 0.96rem;
            color: #42374A;
            font-weight: 800;
        }

        .vp-flow-copy {
            margin-top: 5px;
            color: #817784;
            font-size: 0.82rem;
            line-height: 1.38;
        }

        /* ---------- START PANEL ---------- */

        .vp-start-panel {
            margin-top: 26px;
            padding: 24px;
            border-radius: 24px;
            background: rgba(255,255,255,0.86);
            border: 1px solid rgba(163, 145, 177, 0.17);
            box-shadow: 0 12px 36px rgba(74, 56, 87, 0.05);
        }

        .vp-start-title {
            font-size: 1.35rem;
            font-weight: 850;
            color: #3C3143;
            margin-bottom: 4px;
        }

        .vp-start-copy {
            color: #807585;
            font-size: 0.90rem;
            margin-bottom: 18px;
        }

        /* ---------- STREAMLIT CONTROLS ---------- */

        div[data-baseweb="select"] > div {
            border-radius: 14px !important;
            border-color: #DDD2E5 !important;
            background-color: rgba(255,255,255,0.96) !important;
        }

        div[data-testid="stAlert"] {
            border-radius: 16px;
        }

        div.stButton > button {
            border-radius: 15px;
            min-height: 3.1rem;
            font-weight: 800;
            border: none;
        }

        div.stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #785B91 0%, #607E91 100%);
            color: white;
            box-shadow: 0 10px 25px rgba(105, 83, 127, 0.18);
        }

        div.stButton > button[kind="primary"]:hover {
            filter: brightness(0.97);
            transform: translateY(-1px);
        }

        @media (max-width: 700px) {
            .vp-hero {
                padding: 28px 24px 25px 24px;
                border-radius: 24px;
            }

            .vp-title {
                font-size: 2.35rem;
            }

            .vp-flow-card {
                min-height: 115px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="vp-hero">
            <div class="vp-kicker">✦ Clinical skills • interactive practice</div>
            <div class="vp-title">Meet the patient.<br><span>Think like a clinician.</span></div>
            <p class="vp-subtitle">
                Work through realistic synthetic cases from first question to final management.
                Take the history, examine, investigate, diagnose and treat — then get structured feedback.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    stat1, stat2, stat3, stat4 = st.columns(4)

    stats = [
        ("32", "Patient cases"),
        ("34", "Clinical visuals"),
        ("3", "Difficulty levels"),
        ("5", "Reasoning stages"),
    ]

    for col, (number, label) in zip([stat1, stat2, stat3, stat4], stats):
        with col:
            st.markdown(
                f"""
                <div class="vp-stat">
                    <div class="vp-stat-number">{number}</div>
                    <div class="vp-stat-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown('<div class="vp-section-title">Your clinical workflow</div>', unsafe_allow_html=True)

    flow_cols = st.columns(5)

    flow = [
        ("🗣️", "01", "History", "Interview the patient"),
        ("🩺", "02", "Examine", "Request findings"),
        ("🧪", "03", "Investigate", "Choose tests"),
        ("🧠", "04", "Diagnose", "Commit to an answer"),
        ("💊", "05", "Manage", "Plan treatment"),
    ]

    for col, item in zip(flow_cols, flow):
        icon, number, title, copy = item
        with col:
            st.markdown(
                f"""
                <div class="vp-flow-card">
                    <div class="vp-flow-icon">{icon}</div>
                    <div class="vp-flow-step">Step {number}</div>
                    <div class="vp-flow-title">{title}</div>
                    <div class="vp-flow-copy">{copy}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown(
        """
        <div class="vp-start-panel">
            <div class="vp-start-title">Start your consultation</div>
            <div class="vp-start-copy">
                Choose a case and difficulty. The diagnosis stays hidden until you finish.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    select_col, difficulty_col = st.columns([2, 1])

    with select_col:
        home_case = st.selectbox(
            "Patient case",
            list(CASES.keys()),
            index=list(CASES.keys()).index(st.session_state.selected_case),
            key="home_case_selector"
        )

    with difficulty_col:
        home_difficulty = st.selectbox(
            "Difficulty",
            ["Easy", "OSCE", "Hard"],
            index=["Easy", "OSCE", "Hard"].index(st.session_state.difficulty),
            key="home_difficulty_selector"
        )

    difficulty_help = {
        "Easy": "🌷 **Easy** — extra guidance and teaching hints are visible.",
        "OSCE": "🩺 **OSCE** — clean exam-style practice without extra hints.",
        "Hard": "🔥 **Hard** — the patient may be vague, uncertain or less cooperative."
    }

    st.info(difficulty_help[home_difficulty])

    if st.button(
        "Begin case  →",
        type="primary",
        use_container_width=True
    ):
        st.session_state.selected_case = home_case
        st.session_state.difficulty = home_difficulty
        reset_consultation()
        st.session_state.app_started = True
        st.rerun()

    st.caption(
        "Synthetic educational cases and visuals. Designed for study and supervised clinical-skills practice."
    )

    st.stop()


# =========================================================
# ACTIVE CASE
# =========================================================

selected_case = st.session_state.selected_case
difficulty = st.session_state.difficulty

patient = CASES[selected_case]
theme = THEMES[patient["theme"]]
required_topics = set(patient["required_topics"])
first_name = patient["name"].split()[0]

st.markdown(theme_css(theme), unsafe_allow_html=True)

top_left, top_right = st.columns([1, 4])

with top_left:
    if st.button("← Home", use_container_width=True):
        reset_consultation()
        st.session_state.app_started = False
        st.rerun()

with top_right:
    st.markdown(
        f"""
        <div class="vp-card" style="padding:14px 18px; margin-top:0;">
            <span class="vp-section-pill">{difficulty} mode</span>
            <div class="vp-card-title">{selected_case}</div>
            <div class="vp-card-copy">Work through the case step by step. The diagnosis stays hidden until you commit.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# HEADER
# =========================================================

st.title("🩺 Virtual Patient Simulator")
st.write("Practise clinical history-taking with synthetic patient cases.")
st.caption(
    "Patients may hesitate, volunteer extra details, or react emotionally. "
    "Your wording can also make them more reassured or more guarded."
)

st.info(
    "Ask questions as you would in an OSCE. "
    "The diagnosis is hidden until you finish the consultation."
)

st.caption(
    "📷 Imaging, ECGs, endoscopy, histology and other visuals appear after "
    "you order the relevant investigation, when an image asset is available."
)

# =========================================================
# TRIAGE / OSCE HANDOVER
# =========================================================

st.markdown(
    f"""
    <div class="vp-card">
        <span class="vp-section-pill">Triage handover</span>
        <div class="vp-card-title">📋 Before you meet the patient</div>
        <div class="vp-card-copy">{case_handover(patient)}</div>
    </div>
    """,
    unsafe_allow_html=True
)

st.info(f"Patient state: **{emotion_label(patient, st.session_state.patient_trust)}**")

# =========================================================
# PATIENT CARD
# =========================================================

patient_card = f"""
<div style="background-color:{theme['card']};padding:22px;border-radius:20px;border:1px solid {theme['secondary']};margin-bottom:20px;">
<h2 style="margin-bottom:5px;color:{theme['accent']};">{patient['avatar']} {patient['name']}</h2>
<p style="margin-bottom:4px;color:{theme['text']};"><b>Age:</b> {patient['age']}</p>
<p style="margin-bottom:4px;color:{theme['text']};"><b>Setting:</b> {patient['setting']}</p>
<p style="margin-bottom:4px;color:{theme['text']};"><b>Character:</b> {patient['personality']['style']}</p>
<p style="margin-top:15px;font-style:italic;color:{theme['text']};">“{patient['chief_complaint']}”</p>
</div>
"""

st.markdown(patient_card, unsafe_allow_html=True)

if st.button("🔄 Restart Consultation"):
    reset_consultation()
    st.rerun()

st.divider()

# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user", avatar="🩺"):
            st.write(message["content"])
    else:
        with st.chat_message("assistant", avatar=patient["avatar"]):
            st.write(message["content"])

# =========================================================
# CHAT
# =========================================================

if not st.session_state.consultation_finished:
    st.markdown('<span class="vp-section-pill">Step 1</span>', unsafe_allow_html=True)
    st.markdown("### 💬 Talk to the patient")
    st.caption("Write your question below. Your text will stay clearly visible while you type.")

    st.markdown(
        """
        <div class="vp-question-label">
            Ask your history question
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.form(key=f"history_form_{selected_case}", clear_on_submit=True):
        question = st.text_area(
            "History question",
            placeholder=f"Type here… for example: When did the pain start, {first_name}?",
            key=f"history_question_{selected_case}",
            height=88,
            label_visibility="collapsed"
        )
        ask_submitted = st.form_submit_button(
            "Ask patient  →",
            type="primary",
            use_container_width=True
        )

    if ask_submitted and question.strip():
        st.session_state.messages.append({"role": "user", "content": question})

        with st.chat_message("user", avatar="🩺"):
            st.write(question)

        q = question.lower().strip()
        update_patient_emotion(question)

        # Social conversation
        if contains_any(q, SOCIAL_GREETINGS):
            response = choose_response([
                f"Hi, I'm {first_name}.",
                "Hello.",
                "Hi... I'm not feeling great."
            ])

        elif contains_any(q, ["how are you", "how do you feel", "are you okay"]):
            response = choose_response([
                patient["chief_complaint"],
                "I've definitely felt better.",
                "I'm uncomfortable and a bit worried."
            ])

        elif contains_any(q, SOCIAL_REASSURE):
            response = choose_response([
                "Okay, thank you.",
                "Thanks, I appreciate that.",
                "That helps, thank you."
            ])

        elif contains_any(q, SOCIAL_THANKS):
            response = choose_response(["You're welcome.", "Of course.", "No problem."])

        else:
            matched = False

            # A few special-case intents
            for special_key, phrases in SPECIAL_KEYS.items():
                if contains_any(q, phrases) and special_key in patient.get("responses", {}):
                    response = choose_response(patient["responses"][special_key])
                    special_topic = {
                        "shoulder_tip": "Shoulder-tip pain",
                        "weakness_limb": "Limb weakness",
                        "jaw_claudication": "Jaw claudication",
                    }[special_key]
                    if special_topic in required_topics:
                        st.session_state.topics_asked.add(special_topic)
                    matched = True
                    break

            if not matched:
                smart_match = smart_intent_match(q)
                if smart_match:
                    key, topic = smart_match
                    response = choose_response(get_response_options(patient, key))
                    if topic in required_topics:
                        st.session_state.topics_asked.add(topic)
                    matched = True

            if not matched:
                response = choose_response([
                    "Sorry, I'm not quite sure what you mean.",
                    "Could you ask me that another way?",
                    "I'm not sure I understood that question."
                ])

        # Difficulty behavior
        if difficulty == "Easy":
            if random.random() < 0.20:
                response += " Is there anything else you'd like to know?"
        elif difficulty == "Hard":
            if random.random() < 0.16:
                vague_prefix = choose_response([
                    "I'm not completely sure, but ",
                    "It's hard to explain... ",
                    "I can't remember exactly, but ",
                    "Maybe... "
                ])
                response = vague_prefix + response[0].lower() + response[1:]

        response = humanize_response(
            patient,
            selected_case,
            response
        )

        if st.session_state.patient_trust >= 2 and random.random() < 0.18:
            response += " Thank you for explaining things clearly."
        elif st.session_state.patient_trust <= -2 and random.random() < 0.22:
            response = choose_response([
                "I'm not really comfortable with how this is going. ",
                "I'm feeling a bit uncomfortable. "
            ]) + response

        st.session_state.messages.append({"role": "assistant", "content": response})

        with st.chat_message("assistant", avatar=patient["avatar"]):
            st.write(response)


# =========================================================
# EXAMINATION / INVESTIGATIONS
# =========================================================

clinical_data = EXAM_DATA.get(selected_case, {})
test_catalog = TEST_CATALOG.get(selected_case, {})

if clinical_data and not st.session_state.consultation_finished:
    st.subheader("🩻 Clinical Assessment")

    st.caption(
        "Request examination findings and order investigations only when "
        "you think they are clinically relevant."
    )

    if st.button("❤️ Request Vitals", use_container_width=True):
        st.session_state.revealed_clinical_data.add("vitals")

    if "vitals" in st.session_state.revealed_clinical_data:
        with st.expander("❤️ Vital Signs", expanded=True):
            for finding in clinical_data.get("vitals", []):
                st.write(f"• {finding}")

    st.markdown("### 🩺 Focused Physical Examination")
    st.caption(
        "Choose what you actually want to examine. Findings stay hidden until "
        "you perform that part of the examination."
    )

    grouped_exam = classify_exam_findings(clinical_data.get("examination", []))
    exam_options = list(grouped_exam.keys())

    if exam_options:
        chosen_exam = st.selectbox(
            "Examination system",
            exam_options,
            key=f"exam_system_{selected_case}"
        )

        if st.button("Perform selected examination", use_container_width=True):
            st.session_state.revealed_clinical_data.add(f"exam:{chosen_exam}")

        examined_any = False
        for system in exam_options:
            if f"exam:{system}" in st.session_state.revealed_clinical_data:
                examined_any = True
                with st.expander(f"🩺 {system}", expanded=True):
                    for finding in grouped_exam[system]:
                        st.write(f"• {finding}")

        if not examined_any:
            st.info("No focused examination has been performed yet.")

    st.markdown('<span class="vp-section-pill">Step 3</span>', unsafe_allow_html=True)
    st.markdown("### 🧪 Order Investigations")

    if test_catalog:
        selected_tests = st.multiselect(
            "Choose investigations:",
            options=list(test_catalog.keys()),
            key=f"tests_{selected_case}"
        )

        if st.button("Order selected tests", use_container_width=True):
            for test_name in selected_tests:
                st.session_state.ordered_tests[test_name] = test_catalog[test_name]

        if st.session_state.ordered_tests:
            st.markdown("#### Results")

            for test_name, info in st.session_state.ordered_tests.items():
                st.markdown(f"**{test_name}**")
                st.write(info["result"])

                show_test_visual(
                    selected_case,
                    test_name,
                    difficulty
                )

                if difficulty == "Easy":
                    label = {
                        "essential": "⭐ High-yield / essential",
                        "useful": "✅ Reasonable",
                        "low_value": "⚠️ Low-value in this case"
                    }[info["value"]]
                    st.caption(label)

    st.divider()

# =========================================================
# END CONSULTATION
# =========================================================

st.divider()

if not st.session_state.consultation_finished:
    if st.button("🛑 End Consultation"):
        st.session_state.consultation_finished = True
        st.rerun()

# =========================================================
# RESULTS
# =========================================================

if st.session_state.consultation_finished:
    completed = st.session_state.topics_asked & required_topics
    missed = required_topics - completed

    score = round((len(completed) / len(required_topics)) * 100) if required_topics else 0

    st.header("📋 Consultation Results")
    st.metric("History-Taking Score", f"{score}%")

    test_catalog = TEST_CATALOG.get(selected_case, {})
    ordered_test_names = set(st.session_state.ordered_tests.keys())

    essential_tests = {
        name for name, info in test_catalog.items()
        if info["value"] == "essential"
    }

    useful_tests = {
        name for name, info in test_catalog.items()
        if info["value"] == "useful"
    }

    low_value_tests = {
        name for name, info in test_catalog.items()
        if info["value"] == "low_value"
    }

    essential_hit = ordered_test_names & essential_tests
    useful_hit = ordered_test_names & useful_tests
    low_value_hit = ordered_test_names & low_value_tests

    if essential_tests:
        investigation_score = round(
            (
                len(essential_hit) * 2
                + len(useful_hit)
                - len(low_value_hit)
            )
            / max((len(essential_tests) * 2 + len(useful_tests)), 1)
            * 100
        )
        investigation_score = max(0, min(100, investigation_score))
    else:
        investigation_score = 100

    st.metric("Investigation Score", f"{investigation_score}%")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Covered")
        if completed:
            for topic in sorted(completed):
                st.write(f"✅ {topic}")
        else:
            st.write("None yet.")

    with col2:
        st.subheader("Missed")
        if missed:
            for topic in sorted(missed):
                st.write(f"❌ {topic}")
        else:
            st.success("Everything covered!")


    st.subheader("🧪 Investigation Feedback")

    if essential_tests:
        missed_essential = essential_tests - ordered_test_names

        if essential_hit:
            st.write("**Essential investigations ordered:**")
            for name in sorted(essential_hit):
                st.write(f"✅ {name}")

        if missed_essential:
            st.write("**Essential investigations missed:**")
            for name in sorted(missed_essential):
                st.write(f"❌ {name}")

        if low_value_hit:
            st.write("**Low-value investigations ordered:**")
            for name in sorted(low_value_hit):
                st.write(f"⚠️ {name}")
    else:
        st.write("No essential investigation set was defined for this case.")

    st.divider()
    st.markdown('<span class="vp-section-pill">Step 4A</span>', unsafe_allow_html=True)
    st.subheader("🔀 Differential Diagnoses")
    st.caption(
        "Before committing to your final answer, enter up to three plausible alternatives. "
        "Think about dangerous mimics as well as common ones."
    )

    d1 = st.text_input("Differential 1", value=st.session_state.differentials[0], key=f"diff1_{selected_case}")
    d2 = st.text_input("Differential 2", value=st.session_state.differentials[1], key=f"diff2_{selected_case}")
    d3 = st.text_input("Differential 3", value=st.session_state.differentials[2], key=f"diff3_{selected_case}")

    if st.button("Submit Differentials"):
        st.session_state.differentials = [d1.strip(), d2.strip(), d3.strip()]
        st.session_state.differentials_submitted = True

    if st.session_state.differentials_submitted:
        entered = [x for x in st.session_state.differentials if x]
        reasonable = DIFFERENTIAL_CATALOG.get(selected_case, [])

        if entered:
            hits = []
            for user_diff in entered:
                normalized = user_diff.lower()
                matched_reasonable = next(
                    (item for item in reasonable
                     if normalized in item.lower() or item.lower() in normalized),
                    None
                )
                hits.append((user_diff, matched_reasonable))

            st.write("**Differential feedback:**")
            for user_diff, match in hits:
                if match:
                    st.write(f"✅ {user_diff} — reasonable alternative")
                else:
                    st.write(f"💭 {user_diff} — not in the preset list, but may still be defensible depending on your reasoning.")

            if difficulty == "Easy":
                st.caption("Other reasonable possibilities: " + ", ".join(reasonable[:3]))

    st.divider()
    st.markdown('<span class="vp-section-pill">Step 4B</span>', unsafe_allow_html=True)
    st.subheader("🧠 Your Final Diagnosis")

    diagnosis = st.text_input(
        "What is your most likely diagnosis?",
        value=st.session_state.final_diagnosis_text,
        key=f"final_dx_{selected_case}"
    )

    if st.button("Submit Diagnosis"):
        diagnosis_text = diagnosis.lower().strip()

        if diagnosis_text == "":
            st.warning("Please enter a diagnosis first.")
        else:
            st.session_state.final_diagnosis_text = diagnosis.strip()
            st.session_state.diagnosis_submitted = True
            st.session_state.diagnosis_correct = any(
                keyword in diagnosis_text
                for keyword in patient["diagnosis_keywords"]
            )

            if st.session_state.diagnosis_correct:
                st.success(f"✅ Correct — {patient['diagnosis_display']}")
            else:
                st.error("❌ Incorrect diagnosis.")
                st.write(f"**The intended diagnosis was {patient['diagnosis_display']}.**")

            st.write("**Key clinical clues:**")
            for clue in patient["diagnosis_explanation"]:
                st.write(f"- {clue}")


# =========================================================
# MANAGEMENT / TREATMENT
# =========================================================

if st.session_state.consultation_finished and st.session_state.diagnosis_submitted:
    st.divider()
    st.markdown('<span class="vp-section-pill">Step 5</span>', unsafe_allow_html=True)
    st.header("💊 Management Plan")

    management_catalog = MANAGEMENT_CATALOG.get(selected_case, {})

    st.write(
        "Select the actions you would include in your immediate or initial "
        "management plan for this simulated patient."
    )

    selected_management = st.multiselect(
        "Choose management actions:",
        options=list(management_catalog.keys()),
        default=st.session_state.selected_management,
        key=f"management_choices_{selected_case}"
    )

    if st.button("Submit Management Plan"):
        st.session_state.selected_management = selected_management
        st.session_state.management_submitted = True

    if st.session_state.management_submitted:
        selected = set(st.session_state.selected_management)

        essential = {
            name for name, info in management_catalog.items()
            if info["value"] == "essential"
        }

        useful = {
            name for name, info in management_catalog.items()
            if info["value"] == "useful"
        }

        harmful = {
            name for name, info in management_catalog.items()
            if info["value"] == "harmful"
        }

        essential_hit = selected & essential
        useful_hit = selected & useful
        harmful_hit = selected & harmful
        missed_essential = essential - selected

        possible_points = len(essential) * 2 + len(useful)

        earned_points = (
            len(essential_hit) * 2
            + len(useful_hit)
            - len(harmful_hit) * 2
        )

        management_score = round(
            max(0, min(1, earned_points / max(possible_points, 1))) * 100
        )
        st.session_state.management_score = management_score

        st.metric("Management Score", f"{management_score}%")

        if essential_hit:
            st.subheader("✅ Core actions you selected")
            for action in sorted(essential_hit):
                st.write(f"**{action}**")
                st.caption(management_catalog[action]["feedback"])

        if useful_hit:
            st.subheader("👍 Appropriate additional actions")
            for action in sorted(useful_hit):
                st.write(f"**{action}**")
                st.caption(management_catalog[action]["feedback"])

        if missed_essential:
            st.subheader("❌ Important actions you missed")
            for action in sorted(missed_essential):
                st.write(f"**{action}**")
                st.caption(management_catalog[action]["feedback"])

        if harmful_hit:
            st.subheader("⚠️ Actions to avoid")
            for action in sorted(harmful_hit):
                st.write(f"**{action}**")
                st.caption(management_catalog[action]["feedback"])

        history_score = score
        diagnosis_score = 100 if st.session_state.diagnosis_correct else 0

        overall_score = round(
            history_score * 0.30
            + investigation_score * 0.25
            + diagnosis_score * 0.20
            + management_score * 0.25
        )

        st.divider()
        st.subheader("🏁 Overall Case Score")

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric("History", f"{history_score}%")
        with c2:
            st.metric("Investigations", f"{investigation_score}%")
        with c3:
            st.metric("Diagnosis", f"{diagnosis_score}%")
        with c4:
            st.metric("Management", f"{management_score}%")

        st.metric("Overall", f"{overall_score}%")

        st.markdown(
            """
            <div class="vp-card" style="margin-top:16px;">
                <div class="vp-card-title">Your case performance</div>
                <div class="vp-card-copy">
                    Use the detailed review below to identify missed history points,
                    unnecessary tests, diagnostic gaps and management priorities.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if overall_score >= 85:
            st.success("Excellent overall clinical reasoning.")
        elif overall_score >= 70:
            st.success("Good performance with some areas to refine.")
        elif overall_score >= 50:
            st.warning("Reasonable start, but review the missed steps.")
        else:
            st.error("This case needs another attempt. Review the feedback and try again.")



# =========================================================
# END-OF-CASE REVIEW + CLINICAL NOTE
# =========================================================

if st.session_state.management_submitted:
    st.divider()
    st.markdown('<span class="vp-section-pill">Case complete</span>', unsafe_allow_html=True)
    st.header("✨ End-of-Case Review")

    review_tab, note_tab = st.tabs(["📚 Learning review", "📝 Clinical note"])

    with review_tab:
        completed_review = st.session_state.topics_asked & required_topics
        missed_review = required_topics - completed_review
        ordered_names_review = set(st.session_state.ordered_tests.keys())
        essential_review = {
            name for name, info in TEST_CATALOG.get(selected_case, {}).items()
            if info["value"] == "essential"
        }
        low_value_review = {
            name for name, info in TEST_CATALOG.get(selected_case, {}).items()
            if info["value"] == "low_value"
        }

        st.markdown("### What you did well")
        strengths = []
        if len(completed_review) >= max(1, int(len(required_topics) * 0.75)):
            strengths.append("You covered most of the important history domains.")
        if essential_review and essential_review.issubset(ordered_names_review):
            strengths.append("You ordered all of the predefined essential investigations.")
        if st.session_state.diagnosis_correct:
            strengths.append("You reached the intended diagnosis.")
        if st.session_state.management_score is not None and st.session_state.management_score >= 75:
            strengths.append("Your management plan included most of the important actions.")
        if st.session_state.patient_trust >= 1:
            strengths.append("Your communication style helped the patient feel more comfortable.")

        if strengths:
            for item in strengths:
                st.write(f"✅ {item}")
        else:
            st.write("This was a challenging attempt — use the sections below to target your next try.")

        st.markdown("### What to improve next time")
        improvements = []
        if missed_review:
            improvements.append(
                "History domains missed: " + ", ".join(sorted(missed_review)[:8])
            )
        missed_tests_review = essential_review - ordered_names_review
        if missed_tests_review:
            improvements.append(
                "Essential investigations missed: " + ", ".join(sorted(missed_tests_review))
            )
        unnecessary_review = ordered_names_review & low_value_review
        if unnecessary_review:
            improvements.append(
                "Consider avoiding low-value tests here: " + ", ".join(sorted(unnecessary_review))
            )
        if not st.session_state.diagnosis_correct:
            improvements.append(
                f"Revisit the key pattern that points toward {patient['diagnosis_display']}."
            )
        if st.session_state.patient_trust <= -1:
            improvements.append(
                "Use more neutral, empathic wording to keep the patient engaged."
            )

        if improvements:
            for item in improvements:
                st.write(f"→ {item}")
        else:
            st.success("No major predefined gaps were identified in this attempt.")

        st.markdown("### 🚨 Safety / red-flag takeaway")
        st.info(
            RED_FLAG_FEEDBACK.get(
                selected_case,
                "Always reassess for physiological deterioration, diagnostic uncertainty, "
                "and features that would require urgent senior review."
            )
        )

        st.markdown("### Differential-thinking prompt")
        st.write(
            "Useful alternatives for this presentation included: "
            + ", ".join(DIFFERENTIAL_CATALOG.get(selected_case, [])[:4])
            + "."
        )

        st.caption(
            "Feedback is deliberately simplified for undergraduate educational practice "
            "and should be checked against your local teaching and clinical guidelines."
        )

    with note_tab:
        note_text = make_clinical_note(
            patient=patient,
            selected_case=selected_case,
            discovered_topics=st.session_state.topics_asked,
            revealed_data=st.session_state.revealed_clinical_data,
            ordered_tests=st.session_state.ordered_tests,
            diagnosis_text=st.session_state.final_diagnosis_text,
            management=st.session_state.selected_management
        )

        st.text_area(
            "Generated clerking note",
            note_text,
            height=430,
            key=f"note_{selected_case}"
        )

        st.download_button(
            "⬇️ Download note as .txt",
            data=note_text,
            file_name=f"{selected_case.replace(' ', '_').replace('-', '')}_clinical_note.txt",
            mime="text/plain",
            use_container_width=True
        )

        st.caption(
            "This note is generated only from information you actually uncovered or submitted "
            "during the simulated consultation."
        )


# =========================================================
# FOOTER
# =========================================================

st.caption(
    "Educational simulator only. Cases are synthetic and are not a substitute "
    "for supervised clinical training or real-patient assessment."
)
