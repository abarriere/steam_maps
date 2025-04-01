import streamlit as st
from utils.google_places import extract_places, save_to_db, load_places, delete_place

st.set_page_config(page_title="Export Places", page_icon="📍", layout="wide")

st.title("📍 Export Your Google Places")
st.markdown("Easily extract and manage your saved places from Google Maps.")

# Input URL
url = st.text_input("Enter Google Maps URL", placeholder="Paste your Google Maps URL here...")
if st.button("Extract and Save Places"):
    if url:
        places = extract_places(url)
        if places:
            save_to_db(places)
            st.success("✅ Places saved successfully!")
        else:
            st.error("⚠️ No places found in the provided URL.")
    else:
        st.error("⚠️ Please enter a valid URL.")

# Display saved places
places = load_places()
if places:
    st.write("### Your Saved Places")
    for place in places:
        gid, lat, lon, name, address = place
        st.write(f"**{name}** - {address} ({lat}, {lon}) [GID: {gid}]")
        if st.button("🗑️ Delete", key=f"delete_{gid}"):
            delete_place(gid)
            st.experimental_rerun()
else:
    st.info("No places found in the database.")