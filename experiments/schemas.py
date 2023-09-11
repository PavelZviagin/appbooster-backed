from pydantic import BaseModel


class ExperimentsSchema(BaseModel):
    button_color: str
    price: float
