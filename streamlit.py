import streamlit as st
import sqlite3
import html
import re
import requests
from streamlit_extras.add_vertical_space import add_vertical_space

def get_place_details(gid, api_key):
    """
    Récupère le nom et l'adresse d'une place à partir de son gid en utilisant l'API Google Places.
    """
    try:
        url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={gid}&key={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "OK":
                result = data.get("result", {})
                name = result.get("name", "Unknown")
                address = result.get("formatted_address", "Unknown")
                return name, address
            else:
                st.error(f"Error from Google API: {data.get('status')}")
                return None, None
        else:
            st.error(f"HTTP Error: {response.status_code}")
            return None, None
    except Exception as e:
        st.error(f"Error fetching place details: {e}")
        return None, None
    
def extract_places(url):
    try:
        x: response = requests.get(url)
        txt = x.text.split(r")]}'\n")[2].split("]]\"],")[0] + "]]"
        txt = html.unescape(txt)

#        txt = response.text.split(r")]}'\n")[2].split("]]"]],")[0] + "]]"]
#        txt = html.unescape(txt)
        results = re.findall(r"\[null,null,[0-9]{1,2}\.[0-9]{4,16},[0-9]{1,2}\.[0-9]{4,16}]", txt)
        results2 = re.findall("Idem Paris", txt)
        print(results2)

        places = []
        index= 0
        for cord in results:
            curr = txt.split(cord)[1].split("\\\"]]")[0]
            curr = curr[curr.rindex("\\\"") + 2:]
            name = txt.split(cord)[1].split("\\\"]]")[0]
            name = name.split(",")[4]
            adresse = txt.split(cord)[0].split("\\\"]]")[0]
            adresse = adresse.split("[")[8].split("\\\"")[3]
            print("name: " + name)
            
            cords = str(cord).split(",")
            lat = cords[2]
            lon = cords[3][:-1]
            
            places.append((curr, lat, lon, name, adresse))
        return places
    except Exception as e:
        st.error(f"Error extracting places: {e}")
        return []

def save_to_db(places):
    """
    Enregistre les lieux dans la base de données, y compris le nom et l'adresse récupérés via l'API Google Places.
    """
    conn = sqlite3.connect("places.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS saved_places (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        gid TEXT,
        latitude TEXT,
        longitude TEXT,
        name TEXT,
        address TEXT
    )""")
    
   
    cursor.executemany(
        "INSERT INTO saved_places (gid, latitude, longitude, name, address) VALUES (?, ?, ?, ?, ?)",
        places
    )
    conn.commit()
    conn.close()

def load_places():
    """
    Charge les lieux enregistrés depuis la base de données.
    """
    conn = sqlite3.connect("places.db")
    cursor = conn.cursor()
    cursor.execute("SELECT gid, latitude, longitude, name, address FROM saved_places")
    data = cursor.fetchall()
    conn.close()
    return data

def delete_place(gid):
    """Supprime un lieu de la base de données par son nom."""
    conn = sqlite3.connect("places.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM saved_places WHERE gid = ?", (gid,))
    conn.commit()
    conn.close()

def main():
    st.set_page_config(page_title="Google Maps Saved Places Exporter", page_icon="🌍", layout="wide")
    st.title("🌍 Google Maps Saved Places Exporter")
    st.markdown("Easily extract and manage your saved places from Google Maps.")

    # Section: Input URL
    st.header("🔗 Extract Places")
    url = st.text_input("Enter Google Maps URL", placeholder="Paste your Google Maps URL here...")
    st.markdown("---")  # Add a horizontal separator

    # Button to extract and save places
    if st.button("Extract and Save Places", use_container_width=True):
        if url:
            places = extract_places(url)
            if places:
                save_to_db(places)
                st.success("✅ Places saved successfully!")
            else:
                st.error("⚠️ No places found in the provided URL.")
        else:
            st.error("⚠️ Please enter a valid URL.")

    # Add vertical space
    add_vertical_space(2)

    # Section: Show Saved Places
    st.header("📍 Saved Places")
    places = load_places()
    if places:
        st.write("### Your Saved Places")
        for place in places:
            gid, lat, lon, name, address = place
            col1, col2, col3, col4 = st.columns([3, 3, 2, 1])
            with col1:
                st.markdown(f"**{name}**")
                st.caption(address)
            with col2:
                st.markdown(f"🌐 **Coordinates:** ({lat}, {lon})")
            with col3:
                st.markdown(f"🆔 **GID:** {gid}")
            with col4:
                if st.button("🗑️ Delete", key=f"delete_{gid}"):
                    delete_place(gid)
                    st.rerun()  # Reload the app after deletion
    else:
        st.info("No places found in the database. Start by extracting places!")

if __name__ == "__main__":
    main()