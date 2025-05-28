from langchain_core.tools import StructuredTool

from backend.llms.guide_agent.agent.tools.tool_inputs import GetArtworkLocationByArtistInput, GetArtworkLocationByNameInput
from backend.mongo_manager import MongoManager
from backend.utils import tools_parser


class GuideTools:

    def __init__(self):
        self.mongo_manager = MongoManager()

    def get_artwork_location_by_name_tool(self):
        tool = StructuredTool.from_function(
            func=self.mongo_manager.get_artwork_location_by_name,
            name="get-artwork-location-by-name",
            description="Útil para encontrar la ubicación de una obra en el museo dado el título de la obra.",
            args_schema=GetArtworkLocationByNameInput,
            return_direct=False,
        )
        return tool

    def get_artwork_location_by_artist_tool(self):
        tool = StructuredTool.from_function(
            func=self.mongo_manager.get_artwork_location_by_artist,
            name="get-artwork-location-by-artist",
            description="Útil para encontrar la ubicación de las obras de un artista en el museo dado el nombre del "
                        "artista.",
            args_schema=GetArtworkLocationByArtistInput,
            return_direct=False
        )
        return tool

    def get_tools(self):
        return [self.get_artwork_location_by_artist_tool(), self.get_artwork_location_by_name_tool()]

    def get_str_tools(self):
        return tools_parser(self.get_tools())

