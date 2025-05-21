import streamlit as st
import hmac
import hashlib
import random

st.title("Prédicteur de Bombes - Stake Mines")
st.markdown("Entrez les informations ci-dessous pour révéler les positions des bombes :")

server_seed = st.text_input("Server Seed (révélé)")
client_seed = st.text_input("Client Seed", value="default")
nonce = st.number_input("Nonce (n° de partie)", min_value=0, step=1)
number_of_bombs = st.slider("Nombre de bombes", 1, 24, 3)

def generate_hmac(server_seed, client_seed, nonce):
    message = f"{client_seed}:{nonce}"
    hmac_hash = hmac.new(
        key=server_seed.encode('utf-8'),
        msg=message.encode('utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest()
    return hmac_hash

def get_mines_positions(hmac_hash, number_of_bombs):
    rng = random.Random(hmac_hash)
    positions = list(range(25))
    rng.shuffle(positions)
    return sorted(positions[:number_of_bombs])

if server_seed:
    hmac_hash = generate_hmac(server_seed, client_seed, nonce)
    bomb_positions = get_mines_positions(hmac_hash, number_of_bombs)
    st.success(f"Positions des bombes : {bomb_positions}")
    # Affichage en grille
    grid = ""
    for i in range(25):
        if i % 5 == 0:
            grid += "\n"
        if i in bomb_positions:
            grid += "[X] "
        else:
            grid += "[ ] "
    st.text(grid)
