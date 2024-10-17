from typing import Union, List, Dict
from pydantic import BaseModel


class FormatResponseSchema(BaseModel):
    data: Union[str, List[Dict], Dict]
    message: str
