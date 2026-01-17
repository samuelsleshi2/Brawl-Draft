import streamlit as st
import requests

st.set_page_config(layout="wide")

st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #1e0b36 0%, #2a0f55 100%);
        color: white;
    }

    /* NEW: Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #1e0b36 !important;
        border-right: 2px solid #3e206d;
    }

    /* Headers */
    h1, h2, h3 {
        color: #ffce00 !important;
        text-transform: uppercase;
        font-family: 'Arial Black', sans-serif;
        text-shadow: 2px 2px 0 #000, -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000;
    }
    
    /* Dropdowns and Selectboxes */
    .stSelectbox label {
        color: #ffce00 !important;
        font-weight: bold;
    }
    
    /* Image and Logo Borders */
    img {
        border-radius: 15px;
        border: 2px solid #3e206d;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        transition: transform 0.2s;
    }
            
    .logo-style {
        border: 4px solid #ffce00 !important;
        border-radius: 15px;
        padding: 5px;
        background-color: #3e206d;
        box-shadow: 0 4px 8px rgba(0,0,0,0.5);
        display: block;
        margin-left: auto;
    }
            
    img:hover {
        transform: scale(1.05);
    }
    </style>
    """, unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])

with col1:
    st.title("Brawl Stars Ranked Draft Guide")

with col2:
    logo_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSAOStuzbNr0nIur8ENWACPTYsCzhne4WvS0-yGhuTYcQ&s"
    st.markdown(
        f'<img src="{logo_url}" class="logo-style" width="120">', 
        unsafe_allow_html=True
    )

@st.cache_data
def get_brawler_id_map():
    try:
        data = requests.get("https://api.brawlapi.com/v1/brawlers").json()
        return {b['name'].upper(): b['id'] for b in data['list']}
    except:
        return {}

id_map = get_brawler_id_map()

conn = st.connection("draft.db", type="sql", url="sqlite:///draft.db")

modes_query = conn.query("SELECT DISTINCT mode FROM Rankings")
modes_list = modes_query['mode'].tolist()
mode_choice = st.sidebar.selectbox("Select Mode", modes_list)

map_query = conn.query(f"SELECT DISTINCT map_name FROM Rankings WHERE mode = '{mode_choice}' ORDER BY map_name ASC")
map_list = map_query['map_name'].tolist()
map_choice = st.sidebar.selectbox("Select Map", map_list)

df_map_data = conn.query(f"SELECT * FROM Rankings WHERE map_name = '{map_choice}'")

def display_brawlers(df_filtered):
    if df_filtered.empty:
        st.warning("No brawlers found.")
        return

    def normalize(text):
        return "".join(filter(str.isalnum, text)).upper()

    clean_id_map = {normalize(name): b_id for name, b_id in id_map.items()}

    brawlers = df_filtered.to_dict('records')
    cols = st.columns(3)

    for i, brawler in enumerate(brawlers):
        with cols[i % 3]:
            raw_name = brawler['brawler_name']
            
            search_name = normalize(raw_name)
            
            b_id = clean_id_map.get(search_name)
            
            if b_id:
                img_url = f"https://cdn.brawlify.com/brawlers/borderless/{b_id}.png"
            else:
                clean_url = raw_name.lower().replace(".", "").replace(" ", "-")
                img_url = f"https://cdn.brawlify.com/brawler/{clean_url}.png"

            st.image(img_url, use_container_width=True)
            st.subheader(raw_name)
            
            if brawler['description']:
                st.write(brawler['description'])
            else:
                st.caption("Strategy loading...")

tab1, tab2, tab3, tab4 = st.tabs(["Instructions", "1st Pick", "6th Pick", "Other"])

with tab1:
    with st.expander("How to use 📃"):
        st.write('''
            1. Enter your mode
            2. Enter your map
            3. Click on your pick
            
            You will then be recommended 5-10 brawlers to play.
        ''')

with tab2:
    st.header("Best 1st Picks:")
    display_brawlers(df_map_data[df_map_data["pick"] == "1st"])

with tab3:
    st.header("Best 6th Picks:")
    display_brawlers(df_map_data[df_map_data["pick"] == "6th"])

with tab4:
    st.header("Other Good Picks:")
    display_brawlers(df_map_data[df_map_data["pick"] == "Other"])