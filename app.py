import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Bevcsi App", layout="centered")

# --- IDŐKEZELÉS ---
st.title("💰 Bevcsi Pénzügyi Kezelő")
ma = datetime.now()
valasztott_ev = st.sidebar.selectbox("Év", [ma.year, ma.year + 1], index=0)
valasztott_honap = st.sidebar.selectbox("Hónap", ["Január", "Február", "Március", "Április", "Május", "Június", "Július", "Augusztus", "Szeptember", "Október", "November", "December"], index=ma.month - 1)

st.header(f"📅 {valasztott_ev} - {valasztott_honap}")

# --- INDULÓ EGYENLEG ---
nyito = st.number_input("Nyitó egyenleg (átvitel)", value=0, step=1000, key=f"nyito_{valasztott_honap}")
st.write("---")

# --- 1. BEVÉTELEK ---
st.subheader("1. Bevételek")
osszes_bevetel = 0
forrasok = ["Genpact", "Jogiroda", "Béla", "Tekla", "Adomány", "Egyéb"]
cols_bev = st.columns(2)

for i, nev in enumerate(forrasok):
    with cols_bev[i % 2]:
        bev = st.number_input(f"{nev} (Ft)", value=0, step=1000, key=f"b_{nev}_{valasztott_honap}")
        osszes_bevetel += bev

fokonyv = nyito + osszes_bevetel
st.metric("Kiinduló keret", f"{fokonyv} Ft")
st.write("---")

# --- 2. REVOLUT UTALÁSOK ---
st.subheader("2. Revolut utalások")

# B Revolut (3 slot)
st.write("**B Revolut utalások (max 3)**")
osszes_b_rev = 0
cols_b = st.columns(3)
for i in range(1, 4):
    with cols_b[i-1]:
        b_ut = st.number_input(f"B {i}. (Ft)", value=0, step=1000, key=f"b_rev_{i}_{valasztott_honap}")
        osszes_b_rev += b_ut

# T Revolut (6 slot)
st.write("**T Revolut utalások (max 6)**")
osszes_t_rev = 0
cols_t = st.columns(3)
for i in range(1, 7):
    with cols_t[(i-1) % 3]:
        t_ut = st.number_input(f"T {i}. (Ft)", value=0, step=1000, key=f"t_rev_{i}_{valasztott_honap}")
        osszes_t_rev += t_ut

# Közös részegyenleg a két Revolut után
fokonyv -= (osszes_b_rev + osszes_t_rev)
st.info(f"RÉSZEGYENLEG (B és T Revolut után): **{fokonyv} Ft**")
st.write("---")

# --- 3. FIX ÉS EGYÉB ---
st.subheader("3. KK Singer és Egyéb")
fix = st.number_input("KK Singer (kézi)", value=0, step=100, key=f"fix_{valasztott_honap}")
fokonyv -= fix

st.write("**Egyéb kifizetések (max 3)**")
egyeb_osszeg = 0
cols_e = st.columns(3)
for i in range(1, 4):
    with cols_e[i-1]:
        e_ut = st.number_input(f"Egyéb {i}.", value=0, step=500, key=f"e_{i}_{valasztott_honap}")
        egyeb_osszeg += e_ut
fokonyv -= egyeb_osszeg
st.write(f"Egyenleg egyéb után: **{fokonyv} Ft**")
st.write("---")

# --- 4. D-NEK UTALVA ---
st.subheader("4. D-nek utalva (max 6)")
d_osszesen = 0
cols_d = st.columns(3)
for i in range(1, 7):
    with cols_d[(i-1) % 3]:
        d_ut = st.number_input(f"D {i}. tétel", value=0, step=500, key=f"d_{i}_{valasztott_honap}")
        d_osszesen += d_ut
        
fokonyv -= d_osszesen

# --- ZÁRÁS ---
st.divider()
st.success(f"## {valasztott_honap}i záró/átvihető: {fokonyv} Ft")

# Segítség a mentéshez
if st.button("Hónap lezárása (Képernyőkép készítése)"):
    st.balloons()
    st.info("Kérlek, készíts egy képernyőfotót vagy jegyezd fel a záróösszeget a következő hónap indításához!")
