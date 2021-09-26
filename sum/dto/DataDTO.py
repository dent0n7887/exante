from pydantic import BaseModel, StrictInt, StrictStr, StrictBool, StrictFloat
from typing import Union, Dict, List


class DataDTO(BaseModel):
    js: Union[StrictInt, StrictFloat, StrictBool, StrictStr, Dict, List]