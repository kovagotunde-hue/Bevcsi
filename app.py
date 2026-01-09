import streamlit as st

st.set_page_config(page_title="Bevcsi App", layout="centered")
st.title("💰 Bevcsi Pénzügyi Kezelő")

# --- INDULÓ EGYENLEG ---
nyito = st.number_input("Nyitó egyenleg (átvitel)", value=0, step=1000)
st.write("---")

# --- BEVÉTELEK (Egyedi nevekkel) ---
st.subheader("1. Bevételek")
osszes_bevetel = 0

# Itt írd át a neveket arra, amire szeretnéd (pl. "Fizetés", "Cafeteria", stb.)
forrasok = {
    "Genpact": 0,
    "Jogiroda": 0,
    "Béla": 0,
    "Tekla": 0,
    "Adomány": 0,
    "Egyéb": 0
}

cols_bev = st.columns(2)
i = 0
for nev in forrasok.keys():
    with cols_bev[i % 2]:
        bev = st.number_input(f"{nev} (Ft)", value=0, step=1000, key=f"b_{nev}")
        osszes_bevetel += bev
    i += 1

fokonyv = nyito + osszes_bevetel
st.metric("Aktuális keret összesen", f"{fokonyv} Ft")
st.write("---")

# --- UTALÁSOK (Azonnali részegyenleggel) ---
st.subheader("B Revolut")
szamla_a = st.number_input("'B Revolut, value=0, step=1000)
fokonyv -= szamla_a
st.warning(f"Egyenleg 'B Revolut' után: {fokonyv} Ft")

szamla_b = st.number_input("T Revolut", value=0, step=1000)
fokonyv -= szamla_b
st.info(f"RÉSZEGYENLEG utalások után: {fokonyv} Ft")
st.write("---")

# --- FIX ÉS EGYÉB ---
st.subheader("KK Singer")
fix = st.number_input("KK Singer (kézi)", value=0, step=100)
fokonyv -= fix
st.write(f"Egyenleg KK Singer után: **{fokonyv} Ft**")

for i in range(1, 4):
    egyeb = st.number_input(f"Egyéb kifizetés {i}", value=0, step=500, key=f"e_{i}")
    fokonyv -= egyeb
    if egyeb > 0:
        st.write(f"Egyenleg tétel után: **{fokonyv} Ft**")
st.write("---")

# --- Dnek ---
st.subheader("4. Dnek utalva (max 6)")
for j in range(1, 7):
    fiam = st.number_input(f"Fiam {j}. tétel", value=0, step=500, key=f"f_{j}")
    fokonyv -= fiam
    if fiam > 0:
        st.write(f"Aktuális egyenleg: **{fokonyv} Ft**")

# --- ZÁRÁS ---
st.divider()
st.success(f"## Havi záró/átvihető: {fokonyv} Ft")
