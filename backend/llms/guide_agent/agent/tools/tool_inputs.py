from pydantic import BaseModel, Field


class GetArtworkLocationByNameInput(BaseModel):
    artwork_name: str = Field(
        description="el nombre de la obra la cual se quiere saber la ubicación dentro del museo",
        default="",
    )


class GetArtworkLocationByArtistInput(BaseModel):
    artwork_artist: str = Field(
        description=(
            "El nombre del autor del que se quiere saber la ubicación de sus obras dentro del museo. "
            "Este debe estar entre: ['Caravaggio (Michelangelo Merisi)', 'Canaletto (Giovanni Antonio Canal)', "
            "'Alberto Durero', 'Duccio di Buoninsegna', 'Velázquez (Diego Rodríguez de Silva y Velázquez)', "
            "'Jan van Eyck', 'Harmensz. van Rijn Rembrandt', 'Édouard Manet', 'Joan Miró', 'Claude Monet', "
            "'Piet Mondrian', 'Salvador Dalí', 'Edgar Degas', 'Berthe Morisot', 'Paul Gauguin', 'Francisco de Goya', "
            "'El Greco (Doménikos Theotokópoulos)', 'Vincent van Gogh',  'Ernst Ludwig Kirchner', 'Georgia O'Keeffe', "
            "'Edward Hopper']"
        ),
        default="",
    )

