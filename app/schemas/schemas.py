from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class TableBase(BaseModel):
    name: str
    seats: int
    location: Optional[str]


class TableCreate(TableBase):
    pass


class TableOut(TableBase):
    id: int

    model_config = {
        "from_attributes": True
    }


class ReservationBase(BaseModel):
    customer_name: str
    table_id: int
    reservation_time: datetime
    duration_minutes: int = Field(gt=0)


class ReservationCreate(ReservationBase):
    pass


class ReservationOut(ReservationBase):
    id: int

    model_config = {
        "from_attributes": True
    }
