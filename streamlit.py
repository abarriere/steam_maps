import streamlit as st
import sqlite3
import html
import re
import requests

def extract_places(url):
    try:
        x: response = requests.get(url)
        txt = x.text.split(r")]}'\n")[2].split("]]\"],")[0] + "]]"
        txt = html.unescape(txt)

#        txt = response.text.split(r")]}'\n")[2].split("]]"]],")[0] + "]]"]
#        txt = html.unescape(txt)
        results = re.findall(r"\[null,null,[0-9]{1,2}\.[0-9]{4,15},[0-9]{1,2}\.[0-9]{4,15}]", txt)
        
        places = []
        for cord in results:
            curr = txt.split(cord)[1].split("\\\"]]")[0]
            curr = curr[curr.rindex("\\\"") + 2:]
            cords = str(cord).split(",")
            lat = cords[2]
            lon = cords[3][:-1]
            places.append((curr, lat, lon))
        return places
    except Exception as e:
        st.error(f"Error extracting places: {e}")
        return []

def save_to_db(places):
    conn = sqlite3.connect("places.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS saved_places (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        latitude TEXT,
        longitude TEXT
    )""")
    cursor.executemany("INSERT INTO saved_places (name, latitude, longitude) VALUES (?, ?, ?)", places)
    conn.commit()
    conn.close()

def load_places():
    conn = sqlite3.connect("places.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, latitude, longitude FROM saved_places")
    data = cursor.fetchall()
    conn.close()
    return data

def main():
    st.title("Google Maps Saved Places Exporter")
    url = st.text_input("Enter Google Maps URL")
    if st.button("Extract and Save Places"):
        if url:
            places = extract_places(url)
            if places:
                save_to_db(places)
                st.success("Places saved successfully!")
        else:
            st.error("Please enter a valid URL.")
    
    if st.button("Show Saved Places"):
        places = load_places()
        if places:
            st.write("### Saved Places")
            for place in places:
                st.write(f"**{place[0]}** - ({place[1]}, {place[2]})")
        else:
            st.write("No places found in the database.")

if __name__ == "__main__":
    main()