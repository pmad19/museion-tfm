
class StoreExistingPineconeArtworkException(Exception):
    def __init__(self, message):
        message = "La obra que intentas introducir ya se encuentra registrada en la base de datos."
        super().__init__(message)


class FindMongoArtworkException(Exception):
    def __init__(self, message):
        message = "No se ha encontrado el artista."
        super().__init__(message)


class FindMongoArtistException(Exception):
    def __init__(self, message):
        message = "No se ha encontrado la obra."
        super().__init__(message)
