from pydantic import BaseModel
from pydantic import Field

class MM1(BaseModel):
    miu: float = Field(...)
    lamb: float = Field(...)

class MMs(MM1):
    number_servers: int = Field(...)

class Costos(MMs):
    wait_cost: float = Field(...)
    service_cost: float = Field(...)

class MM1K(MM1):
    #número de clientes que pueden estar en la cola
    k: int = Field(...)


# class Ambulance(BaseModel):
#     placa: str = Field(...)
#     id_provee: int = Field(...)
#     id_para: int = Field(...)
#     latitud: Optional[str] = Field(default=None)
#     longitud: Optional[str] = Field(default=None)
#     estado: Optional[str] = Field(default="Disponible")