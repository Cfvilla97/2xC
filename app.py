import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Passordene hentes fra Streamlit sine "Secrets" (App settings → Secrets)
GUEST_PASSWORD = st.secrets.get("guest_password", "Christina_12345")
ADMIN_PASSWORD = st.secrets.get("admin_password", "Carl_12345")

RESPONSES_FILE = "svar.csv"

DATES = [
    "Torsdag 3. september",
    "Fredag 4. september",
    "Søndag 5. september",
    "Mandag 7. september",
    "Tirsdag 8. september",
    "Onsdag 9. september",
]

ACTIVITIES = {
    "Innendørs ski": {
        "desc": "Snø midt i byen — vi tar en runde i bakken.",
        "image": "images/ski.jpg",
    },
    "Badstue og fjordbad": {
        "desc": "Varm opp, hopp i — badstue etterfulgt av et kaldt dukkert i fjorden.",
        "image": "https://v.imgi.no/8dxk2bazcd",
    },
    "Joggetur og middag": {
        "desc": "En løpetur for å få opp pulsen, så middag etterpå.",
        "image": "https://images.unsplash.com/photo-1758520705254-1e9d913d78ea?fm=jpg&q=60&w=1200&auto=format&fit=crop",
    },
    "En smak av 17. mai": {
        "desc": "Champagnefrokost til middag: pølser, kake og en liten quiz med leker.",
        "image": "images/17mai.jpg",
    },
    "Munch og ramen": {
        "desc": "Innom Munchmuseet, så en skål varm ramen på Koie etterpå.",
        "image": "images/munch.jpg",
    },
    "Buldring": {
        "desc": "Klatring uten tau — bare oss, en vegg og litt konkurranseinstinkt.",
        "image": "images/buldring.jpg",
    },
}

st.set_page_config(page_title="Innlogging", page_icon="🔒", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,500;1,500&family=Work+Sans:wght@400;500;600&display=swap');

html, body, [class*="css"]  {
    font-family: 'Work Sans', sans-serif;
}
h1, h2, h3 {
    font-family: 'Fraunces', serif !important;
    font-weight: 500 !important;
}
.stApp {
    background-color: #FBF6EC;
}
.block-container {
    max-width: 620px;
    padding-top: 3rem;
}
div[data-testid="stForm"] {
    background: transparent;
    border: none;
}
.stCheckbox, .stRadio {
    background: #FFFFFF;
    border: 1.5px solid #DDD2BC;
    border-radius: 16px;
    padding: 10px 16px;
    margin-bottom: 8px;
}
.stButton button {
    background-color: #26313C;
    color: white;
    border-radius: 12px;
    border: none;
    padding: 10px 20px;
    font-weight: 600;
    width: 100%;
}
.stButton button:hover {
    background-color: #2E6F6E;
    color: white;
}
.stTextInput input, .stTextArea textarea {
    border-radius: 12px !important;
    border: 1.5px solid #DDD2BC !important;
}
[data-testid="stImage"] img {
    border-radius: 16px;
}
</style>
""", unsafe_allow_html=True)


def load_responses():
    if os.path.exists(RESPONSES_FILE):
        return pd.read_csv(RESPONSES_FILE)
    return pd.DataFrame(columns=["tidspunkt", "navn", "dager", "opplevelse", "melding"])


def save_response(navn, dager, opplevelse, melding):
    df = load_responses()
    new_row = {
        "tidspunkt": datetime.now().isoformat(timespec="seconds"),
        "navn": navn,
        "dager": ", ".join(dager),
        "opplevelse": opplevelse,
        "melding": melding,
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(RESPONSES_FILE, index=False)


# ---------- PASSWORD GATE ----------
if "unlocked" not in st.session_state:
    st.session_state.unlocked = False

if not st.session_state.unlocked:
    st.markdown("### Innlogging")
    st.write("Skriv inn kodeordet for å fortsette.")
    pw = st.text_input("Kodeord", type="password", label_visibility="collapsed", placeholder="Kodeord")
    if st.button("Fortsett"):
        if pw.strip().lower() == GUEST_PASSWORD.lower():
            st.session_state.unlocked = True
            st.rerun()
        else:
            st.error("Feil kodeord, prøv igjen.")
    st.stop()

# ---------- MAIN CONTENT ----------
st.markdown("EN INVITASJON")
st.markdown("# Skal vi finne på noe sammen?")
st.write("Jeg har seks ideer og noen ledige dager i september. Velg det som frister — resten fikser jeg.")

if "submitted" not in st.session_state:
    st.session_state.submitted = False

if not st.session_state.submitted:
    st.markdown("### 01 · Hvilke dager passer?")
    chosen_dates = []
    for d in DATES:
        if st.checkbox(d, key=f"date_{d}"):
            chosen_dates.append(d)

    st.markdown("### 02 · Velg en opplevelse")
    for name, info in ACTIVITIES.items():
        col_img, col_text = st.columns([1, 1.4])
        with col_img:
            st.image(info["image"], use_container_width=True)
        with col_text:
            st.markdown(f"**{name}**")
            st.caption(info["desc"])
        st.write("")

    activity_labels = [f"{name} — {info['desc']}" for name, info in ACTIVITIES.items()]
    choice = st.radio("Velg opplevelse", activity_labels, label_visibility="collapsed", index=None)
    chosen_activity = None
    if choice:
        chosen_activity = list(ACTIVITIES.keys())[activity_labels.index(choice)]

    st.markdown("### 03 · Send det til meg")
    navn = st.text_input("Navnet ditt")
    melding = st.text_area("Melding (valgfritt)", height=80)

    if st.button("Send svar"):
        if not navn.strip():
            st.error("Skriv navnet ditt.")
        elif not chosen_dates:
            st.error("Velg minst én dag som passer.")
        elif not chosen_activity:
            st.error("Velg en opplevelse.")
        else:
            save_response(navn.strip(), chosen_dates, chosen_activity, melding.strip())
            st.session_state.submitted = True
            st.rerun()
else:
    st.success("Sendt! 🙂 Jeg tar kontakt for å bestemme detaljene.")

st.markdown("---")
st.markdown("_Gleder meg — CF_")

# ---------- ADMIN VIEW ----------
with st.expander("Arrangør"):
    admin_pw = st.text_input("Kodeord for arrangør", type="password", key="admin_pw")
    if admin_pw:
        if admin_pw.lower() == ADMIN_PASSWORD.lower():
            df = load_responses()
            if df.empty:
                st.write("Ingen svar ennå.")
            else:
                st.dataframe(df, use_container_width=True)
        else:
            st.error("Feil kodeord.")
