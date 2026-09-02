import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime
import os
import base64

ACCENTS = ["#B85C6B", "#C9A227", "#C1694F", "#B85C6B", "#C9A227", "#C1694F"]


def image_src(path_or_url):
    """Return a src usable in an <img> tag: pass URLs through, base64-encode local files."""
    if path_or_url.startswith("http"):
        return path_or_url
    with open(path_or_url, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return f"data:image/jpeg;base64,{data}"


# Passordene hentes fra Streamlit sine "Secrets" (App settings -> Secrets)
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
        "sted": "SNØ, Lørenskog",
        "type": "Sport & snø",
        "ta_med": "Varme klær og ski",
    },
    "Badstue og fjordbad": {
        "desc": "En av dine spesialiteter. Fjordbad — riktignok litt varmere enn isbadingen du elsker — men med noe godt i glasset og utsikt attpå.",
        "image": "badstue.jpg",
        "sted": "Sørenga sjøbad, Oslo havn",
        "type": "Avslapning",
        "ta_med": "Badetøy og håndkle",
    },
    "Joggetur og middag": {
        "desc": "Etter utallige maratonløp, halvmaratoner og sentrumsløp kan du endelig ta meg med, sette pace, og se hvor dårlig formen egentlig er på denne 28-åringen. Endorfiner først, god middag etterpå — thai hjemme hos meg?",
        "image": "https://images.unsplash.com/photo-1758520705254-1e9d913d78ea?fm=jpg&q=60&w=1200&auto=format&fit=crop",
        "sted": "Sentrum, avslutter hjemme hos meg",
        "type": "Trening & mat",
        "ta_med": "Løpesko og godt humør",
    },
    "En smak av 17. mai": {
        "desc": "Hva er bedre enn å gjenoppleve favorittdagen din — i september? Pølse i brød, eggerøre, rundstykker og bacon, kaker, is og bottomless mimosa. Espresso martini kan skaffes på forespørsel. Vi pynter koselig som på selveste dagen, og tester kunnskapene dine i en 17. mai-quiz. God stemning garantert.",
        "image": "17mai.jpg",
        "sted": "Hjemme hos meg",
        "type": "Feiring",
        "ta_med": "Sultent mage og quiz-hjerne",
    },
    "Munch og ramen": {
        "desc": "Litt kultur på Munchmuseet, etterfulgt av ramen hos Koie. Kirin Ichiban, sake, varm kraft og noen gode samtaler.",
        "image": "munch.jpg",
        "sted": "Munchmuseet + Koie, Bjørvika",
        "type": "Kultur & mat",
        "ta_med": "Nysgjerrighet og sulten mage",
    },
    "Buldring": {
        "desc": "Oslo Klatresenter, Grünerløkka eller Torshov — hva har de til felles? Bratte vegger, dårlige tak, slitne overarmer, men en arena som garanterer god stemning mellom oss to. Etterpå blir det økologisk IPA og vegetarpølse (eller noe tilsvarende) på en av Grünerløkkas barer.",
        "image": "buldring.jpg",
        "sted": "Oslo Klatresenter, Grünerløkka/Torshov",
        "type": "Klatring",
        "ta_med": "Treningsklær og en problemløsende hjerne (klatresko kan lånes)",
    },
}

st.set_page_config(page_title="Innlogging", page_icon="🔒", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,500;1,500&family=Work+Sans:wght@400;500;600&display=swap');

html, body, [class*="css"]  {
    font-family: 'Work Sans', sans-serif;
}
html {
    scroll-behavior: smooth;
}
h1, h2, h3 {
    font-family: 'Fraunces', serif !important;
    font-weight: 500 !important;
}
.stApp {
    background-color: #FBEFE9;
}
.block-container {
    max-width: 620px;
    padding-top: 0rem;
    padding-bottom: 3rem;
}
div[data-testid="stForm"] {
    background: transparent;
    border: none;
}
.stCheckbox {
    background: #FFFDF9;
    border: 1.5px solid #EAD4CE;
    border-radius: 16px;
    padding: 14px 16px;
    margin-bottom: 10px;
    transition: border-color 0.15s ease, transform 0.08s ease;
}
.stCheckbox:active {
    transform: scale(0.98);
}
.stCheckbox label p {
    font-size: 0.95rem !important;
}
.stRadio {
    background: #FFFDF9;
    border: 1.5px solid #EAD4CE;
    border-radius: 16px;
    padding: 10px 16px;
    margin-bottom: 8px;
}
.stButton button {
    background-color: #B85C6B;
    color: white;
    border-radius: 12px;
    border: none;
    padding: 12px 20px;
    font-weight: 600;
    width: 100%;
    min-height: 46px;
    transition: transform 0.08s ease, background 0.15s ease;
}
.stButton button:hover {
    background-color: #9C4A57;
    color: white;
}
.stButton button:active {
    transform: scale(0.97);
}
.stTextInput input, .stTextArea textarea {
    border-radius: 12px !important;
    border: 1.5px solid #EAD4CE !important;
}
[data-testid="stImage"] img {
    border-radius: 16px;
}
.activity-card-inner img {
    width: 88px;
    height: 88px;
    border-radius: 50%;
    object-fit: cover;
    display: block;
    margin: 0 auto 12px;
}
.activity-card-inner .type-tag {
    display: inline-block;
    font-size: 0.66rem;
    font-weight: 600;
    letter-spacing: 0.03em;
    padding: 3px 11px;
    border-radius: 999px;
    background: #F3E3DE;
    margin-bottom: 8px;
}
.activity-card-inner .title {
    font-family: 'Fraunces', serif;
    font-style: italic;
    font-weight: 500;
    font-size: 1.1rem;
    color: #4A2E30;
    margin-bottom: 6px;
}
.activity-card-inner .desc {
    font-size: 0.85rem;
    color: #6B4F4A;
    line-height: 1.45;
    text-align: left;
}
.activity-card-inner .meta-row {
    text-align: left;
    font-size: 0.76rem;
    color: #8A6A64;
    margin-top: 10px;
    padding-top: 8px;
    border-top: 1px dashed #EAD4CE;
    line-height: 1.6;
}
.activity-card-inner .meta-row .label {
    font-weight: 600;
    color: #4A2E30;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    text-align: center;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.card-selected) {
    border-color: #B85C6B !important;
    box-shadow: 0 0 0 2px rgba(184, 92, 107, 0.25);
    background: #FDF4F1;
}

/* --- scroll-reveal hero + sections --- */
.hero-block {
    min-height: 92vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    opacity: 1;
    transition: opacity 0.5s ease, transform 0.5s ease;
}
.hero-block h1 {
    font-size: 3rem;
    line-height: 1.1;
    margin: 0 0 10px;
    color: #4A2E30;
}
.hero-block p {
    color: #8A6A64;
    font-size: 1rem;
}
.hero-block .hint {
    margin-top: 40px;
    font-size: 0.85rem;
    color: #B85C6B;
    animation: bounce 2s infinite;
}
.hero-block.faded {
    opacity: 0;
    transform: translateY(-30px);
}
@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(8px); }
}
.reveal-section {
    opacity: 0;
    transform: translateY(24px);
    transition: opacity 0.6s ease, transform 0.6s ease;
}
.reveal-section.visible {
    opacity: 1;
    transform: translateY(0);
}

/* respect people who've asked for reduced motion */
@media (prefers-reduced-motion: reduce) {
    html { scroll-behavior: auto; }
    .hero-block, .reveal-section, .hint, .heart-pop {
        transition: none !important;
        animation: none !important;
        opacity: 1 !important;
        transform: none !important;
    }
}

/* success screen: small heart pop */
.heart-pop {
    text-align: center;
    font-size: 2.4rem;
    margin: 10px 0 0;
    animation: pop 0.5s ease;
}
@keyframes pop {
    0% { transform: scale(0); opacity: 0; }
    60% { transform: scale(1.15); opacity: 1; }
    100% { transform: scale(1); }
}
</style>
""", unsafe_allow_html=True)


def load_responses():
    if os.path.exists(RESPONSES_FILE):
        return pd.read_csv(RESPONSES_FILE)
    return pd.DataFrame(columns=["tidspunkt", "dager", "opplevelse"])


def save_response(dager, opplevelse):
    df = load_responses()
    new_row = {
        "tidspunkt": datetime.now().isoformat(timespec="seconds"),
        "dager": ", ".join(dager),
        "opplevelse": opplevelse,
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

if "submitted" not in st.session_state:
    st.session_state.submitted = False

# ---------- HERO ----------
st.markdown(
    '''
    <div class="hero-block" id="hero-block">
        <p style="text-transform:uppercase;letter-spacing:0.05em;font-size:0.8rem;color:#B85C6B;">
            En invitasjon til Christina
        </p>
        <h1>Invitasjon til date?</h1>
        <p>Bla ned for å velge.</p>
        <div class="hint">↓ scroll ned</div>
    </div>
    ''',
    unsafe_allow_html=True,
)

if not st.session_state.submitted:

    # ---------- ACTIVITIES ----------
    st.markdown('<div class="reveal-section" id="sec-activities">', unsafe_allow_html=True)
    st.markdown("### Velg en opplevelse")

    if "chosen_activity" not in st.session_state:
        st.session_state.chosen_activity = None

    activity_items = list(ACTIVITIES.items())
    for row_start in range(0, len(activity_items), 3):
        row = activity_items[row_start:row_start + 3]
        cols = st.columns(len(row))
        for col, (name, info) in zip(cols, row):
            i = activity_items.index((name, info))
            color = ACCENTS[i % len(ACCENTS)]
            src = image_src(info["image"])
            is_selected = st.session_state.chosen_activity == name
            with col:
                with st.container(border=True):
                    if is_selected:
                        st.markdown('<span class="card-selected" style="display:none;"></span>', unsafe_allow_html=True)
                    card_html = f'''
                    <div class="activity-card-inner">
                        <div style="height:4px;border-radius:4px;background:{color};margin:-17px -17px 14px;"></div>
                        <img src="{src}">
                        <div class="type-tag" style="color:{color};">{info["type"]}</div>
                        <div class="title">{name}</div>
                        <div class="desc">{info["desc"]}</div>
                        <div class="meta-row">
                            <span class="label">Sted:</span> {info["sted"]}<br>
                            <span class="label">Ta med:</span> {info["ta_med"]}
                        </div>
                    </div>
                    '''
                    st.markdown(card_html, unsafe_allow_html=True)
                    st.write("")
                    button_label = "✓ Valgt" if is_selected else "Velg denne"
                    if st.button(button_label, key=f"pick_{i}", use_container_width=True):
                        st.session_state.chosen_activity = name
                        st.rerun()

    chosen_activity = st.session_state.chosen_activity
    st.markdown('</div>', unsafe_allow_html=True)

    # ---------- DATES ----------
    st.markdown('<div class="reveal-section" id="sec-dates">', unsafe_allow_html=True)
    st.markdown("### Hvilke dager passer?")
    chosen_dates = []
    for d in DATES:
        if st.checkbox(d, key=f"date_{d}"):
            chosen_dates.append(d)
    st.markdown('</div>', unsafe_allow_html=True)

    # ---------- SEND ----------
    st.markdown('<div class="reveal-section" id="sec-send">', unsafe_allow_html=True)
    st.write("")
    if st.button("Send svar"):
        if not chosen_dates:
            st.error("Velg minst én dag som passer.")
        elif not chosen_activity:
            st.error("Velg en opplevelse.")
        else:
            save_response(chosen_dates, chosen_activity)
            st.session_state.submitted = True
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown('<div class="heart-pop">♡</div>', unsafe_allow_html=True)
    st.success("Sendt! 🙂 Jeg tar kontakt for å bestemme detaljene.")

st.markdown('<p style="text-align:center;color:#B85C6B;font-size:1.1rem;margin:24px 0 8px;">♡</p>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center;font-family:Fraunces,serif;font-style:italic;color:#4A2E30;'>Gleder meg — CF</p>", unsafe_allow_html=True)

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
                if st.button("Slett alle svar"):
                    if os.path.exists(RESPONSES_FILE):
                        os.remove(RESPONSES_FILE)
                    st.rerun()
        else:
            st.error("Feil kodeord.")

# ---------- SCROLL-REVEAL SCRIPT ----------
# Injects an IntersectionObserver into the parent Streamlit page (this component
# itself is invisible, height=0) so the hero fades out and each section fades in
# as it scrolls into view.
components.html(
    """
    <script>
    function setupReveal() {
        const doc = window.parent.document;
        const hero = doc.getElementById('hero-block');
        const sections = doc.querySelectorAll('.reveal-section');
        if (!hero && sections.length === 0) return;

        if (hero && !hero.dataset.observed) {
            hero.dataset.observed = "1";
            const heroObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.intersectionRatio < 0.35) {
                        hero.classList.add('faded');
                    } else {
                        hero.classList.remove('faded');
                    }
                });
            }, { threshold: [0, 0.35, 1], root: null });
            heroObserver.observe(hero);
        }

        sections.forEach(sec => {
            if (sec.dataset.observed) return;
            sec.dataset.observed = "1";
            const obs = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        sec.classList.add('visible');
                    }
                });
            }, { threshold: 0.15, root: null });
            obs.observe(sec);
        });
    }
    setupReveal();
    setTimeout(setupReveal, 400);
    setTimeout(setupReveal, 1200);
    </script>
    """,
    height=0,
)
