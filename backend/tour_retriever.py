from backend.mongo_manager import MongoManager
import backend.utils as u


class TourRetriever:

    def __init__(self):
        self.mongo_manager = MongoManager()
        self.n_tour = 0
        self.tour = None
        self.artworks = None
        self.n_artwork = 0

    def set_tour(self, i):
        self.n_tour = i
        self.tour = self.mongo_manager.get_tour(i)
        self.artworks = self.tour['tour_artworks']

    def get_tour_title(self):
        return self.tour['tour_title']

    def get_tour_welcome(self):
        messages = []
        tour_title = self.tour['tour_title']
        tour_description = self.tour['long_tour_description']

        messages.append(f"""
        ¡Perfecto! Buena elección. Comenzaremos entonces con el tour "{tour_title}" 
        """)
        messages = u.split_string_to_list(tour_description, messages)

        return messages

    def get_tour_artwork_messages(self):
        messages = []
        if self.n_artwork >= len(self.artworks):
            return None

        artwork = self.artworks[self.n_artwork]
        self.n_artwork += 1

        messages.append(f"""
        La siguiente obra del recorrido se titula "{artwork["artwork_name"]}", del autor {artwork["artwork_author"]}.        
       """)

        if artwork['artwork_location'] == "No expuesta":
            messages.append(f"""
            La siguiente obra del recorrido no se encuentra expuesta actualmente. Para poder disfrutarla le
            mostraré una imagen.
            """)
            messages.append(0)
            messages.append(artwork['artwork_img'])

        else:
            messages.append(f"""
            Para continuar con el recorrido dirígase a la {artwork['artwork_location'].lower()}. 
            Cuando se encuentre en la sala pulse "Pulsa el botón para continuar".
            """)
            messages.append(1)
            messages.append("DUMMY")

        messages = u.split_string_to_list(artwork['artwork_description'], messages)

        return messages


