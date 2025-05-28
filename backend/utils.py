from langchain_core.documents import Document

from backend.mongo_manager import MongoManager


def split_string_to_list(input_string, message_list):
    parts = input_string.split('\n')
    for part in parts:
        message_list.append(part)
    return message_list


def tools_parser(tools: list):
    tools_str = ""
    for tool in tools:
        tool_str = "\n"

        tool_str += f"function: {tool.name}\n"
        tool_str += f"description: {tool.description}\n"

        args_schema = tool.args_schema
        tool_str += "input: "
        if args_schema.__fields__.items():
            tool_str += "{{"
            fields = []
            for name, input in args_schema.__fields__.items():
                default_value = f'"{input.default}"' if type(input) == str and input.default else f"{input.default}"
                field_str = f'"{name}": {{{{"type": "{type(input)}", "description": "{input.description}", "default_value": {default_value}}}}}'
                fields.append(field_str)
            tool_str += ", ".join(fields)
            tool_str += "}}\n"
        else:
            tool_str += "None\n"

        tools_str += tool_str
        tools_str += "---------"
    return tools_str


def parser_artwork_location_info(mongo_manager: MongoManager, related_artworks: list):
    artworks_prompt_info = "----\n"
    artwork_description = "Desconocida"

    for artwork in related_artworks:

        if isinstance(artwork, Document):
            artwork_description = artwork.page_content
            artwork = artwork.metadata
            artwork_artist = artwork.get('artwork-artist')
            artwork_name = artwork.get('artwork-name')
            artwork_location = mongo_manager.get_artwork_location(artwork_name, artwork_artist)
            artwork_location = artwork_location[0].get('artwork_location')
        else:
            artwork_artist = artwork.get('artwork_artist_name')
            artwork_name = artwork.get('artwork_name_title')
            artwork_location = artwork.get('artwork_location')

        artwork_info = f"Nombre de la obra: {artwork_name}\n"
        artwork_info += f"Nombre del artista: {artwork_artist}\n"
        artwork_info += f"Localización: {artwork_location}\n"
        artwork_info += f"Descripción: {artwork_description}\n"
        artwork_info += "----\n"
        artworks_prompt_info += artwork_info

    return artworks_prompt_info
