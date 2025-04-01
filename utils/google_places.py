import requests
import html
import re
import streamlit as st

def get_place_details(gid, api_key):
    """
    Récupère le nom et l'adresse d'une place à partir de son GID en utilisant l'API Google Places.
    :param gid: Identifiant unique du lieu (GID)
    :param api_key: Clé API Google Places
    :return: Tuple (name, address) ou (None, None) en cas d'erreur
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
    """
    Extrait les lieux à partir d'une URL Google Maps.
    :param url: URL Google Maps contenant les lieux sauvegardés
    :return: Liste de tuples (gid, latitude, longitude, name, address)
    """
    try:
        response = requests.get(url)
        if response.status_code != 200:
            st.error(f"HTTP Error: {response.status_code}")
            return []

        # Extraction des données brutes
        txt = response.text.split(r")]}'\n")[2].split("]]\"],")[0] + "]]"
        txt = html.unescape(txt)

        # Recherche des coordonnées et des informations associées
        results = re.findall(r"\[null,null,[0-9]{1,2}\.[0-9]{4,16},[0-9]{1,2}\.[0-9]{4,16}]", txt)
        places = []

        for cord in results:
            curr = txt.split(cord)[1].split("\\\"]]")[0]
            curr = curr[curr.rindex("\\\"") + 2:]
            name = txt.split(cord)[1].split("\\\"]]")[0].split(",")[4]
            address = txt.split(cord)[0].split("\\\"]]")[0].split("[")[8].split("\\\"")[3]

            cords = str(cord).split(",")
            lat = cords[2]
            lon = cords[3][:-1]

            places.append((curr, lat, lon, name, address))
        return places
    except Exception as e:
        st.error(f"Error extracting places: {e}")
        return []