from pymongo import MongoClient
import streamlit as st


class MongoManager:

    def __init__(self):
        self.client = MongoClient(st.secrets["mongo_uri"])
        self.db = self.client.thyssen_db

    def get_tours_dict(self):
        items = []
        tours = self.db.thyssen_tours.find()
        for tour in tours:
            tour_title = tour['tour_title']
            tour_size = tour['tour_size']
            tour_quote = tour['tour_quote']
            tour_image = tour['tour_image']

            tour_fields = dict(
                title=tour_title,
                quote=tour_quote,
                img=tour_image,
                size=tour_size
            )

            items.append(tour_fields)
        return items

    def get_tour(self, i):
        tours = self.db.thyssen_tours.find()
        return tours[i]

    def get_tours(self):
        tours = self.db.thyssen_tours.find()
        return tours

    def get_fees(self):
        fees = self.db.thyssen_fees.find()
        return fees

    def get_activities(self):
        activities = self.db.thyssen_activities.find()
        return activities

    def get_artist(self, name: str):
        artist = list(self.db.thyssen_artists.find({"artist_name": name}, {}))
        if not artist:
            return None
        else:
            return artist[0]

    def get_artwork_by_artist(self, artwork_name: str, artwork_artist_ref: str, artwork_artist_name: str):
        artwork = list(self.db.thyssen_artworks.find(
            {"artwork_name_title": artwork_name, "artwork_artist_ref": artwork_artist_ref}))

        if not artwork:
            artwork = list(self.db.thyssen_artworks.find(
                {"artwork_name_title": artwork_name, "artwork_artist_name": artwork_artist_name}))

        if artwork:
            return artwork[0]
        else:
            return None

    def get_artwork_by_ref(self, artwork_ref: str):
        artwork = list(self.db.thyssen_artworks.find(
            {"artwork_url_ref": artwork_ref}))

        if artwork:
            return artwork[0]
        else:
            return None

    def get_artist_by_ref(self, artist_ref: str):
        artist = list(self.db.thyssen_artists.find(
            {"artist_url_ref": artist_ref}))

        if artist:
            return artist[0]
        else:
            return None

    def get_artworks_list_by_artist(self, artist_ref: str):
        artworks = list(self.db.thyssen_artworks.find(
            {"artwork_artist_ref": artist_ref}))

        if artworks:
            return artworks
        else:
            return None

    def get_artwork_location_by_name(self, artwork_name: str):
        """
        Returns an artwork location list given the artwork name
        :param artwork_name: the name of the artwork to search
        :return: a list with the artwork name, artwork artist name, and artwork location
        """
        query = {"artwork_name_title": artwork_name}
        projection = {"_id": 0, "artwork_name_title": 1, "artwork_artist_name": 1, "artwork_location": 1}

        result = self.db.thyssen_artworks.find(query, projection)
        return list(result)

    def get_artwork_location_by_artist(self, artwork_artist: str):
        """
        Returns an artwork location list given the artwork artist
        :param artwork_artist: the name of the artist to search
        :return: a list with the artwork name, artwork artist name, and artwork location
        """
        query = {"artwork_artist_name": artwork_artist}
        projection = {"_id": 0, "artwork_name_title": 1, "artwork_artist_name": 1, "artwork_location": 1}

        result = self.db.thyssen_artworks.find(query, projection)
        return list(result)

    def get_artwork_location(self, artwork_name: str, artwork_artist: str):
        """
        Returns an artwork location list given the artwork artist and artwork_name
        :param artwork_name: the name of the artwork to search
        :param artwork_artist: the name of the artist to search
        :return: a list with the artwork name, artwork artist name, and artwork location
        """
        query = {"artwork_name_title": artwork_name, "artwork_artist_name": artwork_artist}
        projection = {"_id": 0, "artwork_name_title": 1, "artwork_artist_name": 1, "artwork_location": 1}

        result = self.db.thyssen_artworks.find(query, projection)
        return list(result)
