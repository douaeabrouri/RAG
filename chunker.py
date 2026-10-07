from pydantic import BaseModel

class Chunk(BaseModel) :
    id    : int
    text   : str
    first_char_index : int
    last_char_index  : int 
    text_path  : str 

