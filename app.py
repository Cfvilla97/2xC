import streamlit as st
import pandas as pd
from datetime import datetime
import os
import base64

ACCENTS = ["#2E6F6E", "#E4A335", "#E2705A", "#2E6F6E", "#E4A335", "#E2705A"]


def image_src(path_or_url):
    """Return a src usable in an <img> tag: pass URLs through, base64-encode local files."""
    if path_or_url.startswith("http"):
        return path_or_url
    with open(path_or_url, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return f"data:image/jpeg;base64,{data}"


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
        "desc": "Ta med racerskiene — snø midt i byen venter. Jeg garanterer termos med kakao (og en aperol spritz i lommelerka), røde kinn, en god kveld, og trolig et par mislykkede jibbeforsøk fra undertegnede i parken.",
        "image": "ski.jpg",
    },
    "Badstue og fjordbad": {
        "desc": "En av dine spesialiteter. Fjordbad — riktignok litt varmere enn isbadingen du elsker — men med noe godt i glasset og utsikt attpå.",
        "image": "https://v.imgi.no/8dxk2bazcd",
    },
    "Joggetur og middag": {
        "desc": "Etter utallige maratonløp, halvmaratoner og sentrumsløp kan du endelig ta meg med, sette pace, og se hvor dårlig formen egentlig er på denne 28-åringen. Endorfiner først, god middag etterpå — thai hjemme hos meg?",
        "image": "https://images.unsplash.com/photo-1758520705254-1e9d913d78ea?fm=jpg&q=60&w=1200&auto=format&fit=crop",
    },
    "En smak av 17. mai": {
        "desc": "Hva er bedre enn å gjenoppleve favorittdagen din — i september? Pølse i brød, eggerøre, rundstykker og bacon, kaker, is og bottomless mimosa. Espresso martini kan skaffes på forespørsel. Vi pynter koselig som på selveste dagen, og tester kunnskapene dine i en 17. mai-quiz. God stemning garantert.",
        "image": "17mai.jpg",
    },
    "Munch og ramen": {
        "desc": "Litt kultur på Munchmuseet, etterfulgt av ramen hos Koie. Kirin Ichiban, sake, varm kraft og forhåpentligvis noen gode samtaler.",
        "image": "munch.jpg",
    },
    "Buldring": {
        "desc": "Oslo Klatresenter, Grünerløkka eller Torshov — hva har de til felles? Bratte vegger, dårlige tak, slitne overarmer, men garantert god stemning mellom oss to. Etterpå blir det økologisk IPA og vegetarpølse (eller noe tilsvarende) på en av Grünerløkkas barer.",
        "image": "buldring.jpg",
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
.activity-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 14px;
    margin-bottom: 18px;
}
.activity-box {
    background: #FFFFFF;
    border: 1.5px solid #DDD2BC;
    border-radius: 16px;
    padding: 18px 12px 16px;
    text-align: center;
}
.activity-box .bar {
    height: 4px;
    border-radius: 4px;
    margin: -18px -12px 14px;
}
.activity-box img {
    width: 84px;
    height: 84px;
    border-radius: 50%;
    object-fit: cover;
    margin-bottom: 10px;
}
.activity-box .title {
    font-weight: 600;
    font-size: 0.92rem;
    color: #26313C;
    margin-bottom: 4px;
}
.activity-box .desc {
    font-size: 0.78rem;
    color: #5B6672;
    line-height: 1.35;
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
st.markdown("EN INVITASJON TIL CHRISTINA")
st.markdown("# Skal vi finne på noe sammen?")
st.write("Jeg har seks ideer og noen ledige dager i september. Velg det som frister mest — resten fikser jeg.")

if "submitted" not in st.session_state:
    st.session_state.submitted = False

if not st.session_state.submitted:
    st.markdown("### 01 · Velg en opplevelse")

    grid_html = '<div class="activity-grid">'
    for i, (name, info) in enumerate(ACTIVITIES.items()):
        src = image_src(info["image"])
        color = ACCENTS[i % len(ACCENTS)]
        grid_html += f'''
        <div class="activity-box">
            <div class="bar" style="background:{color};"></div>
            <img src="{src}">
            <div class="title">{name}</div>
            <div class="desc">{info["desc"]}</div>
        </div>'''
    grid_html += '</div>'
    st.markdown(grid_html, unsafe_allow_html=True)

    activity_labels = [f"{name} — {info['desc']}" for name, info in ACTIVITIES.items()]
    choice = st.radio("Velg opplevelse", activity_labels, label_visibility="collapsed", index=None)
    chosen_activity = None
    if choice:
        chosen_activity = list(ACTIVITIES.keys())[activity_labels.index(choice)]

    st.markdown("### 02 · Hvilke dager passer?")
    chosen_dates = []
    for d in DATES:
        if st.checkbox(d, key=f"date_{d}"):
            chosen_dates.append(d)

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
