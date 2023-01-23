from typing import List

from pydantic import BaseModel

from Genesis.objects.farms import Farm


class Player(BaseModel):
    user_id: int
    balance: int
    farm_id: int
    farm_size: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

    async def pay(self, user, amount: int) -> bool:
        pass

    async def add(self, user) -> bool:
        pass

    async def remove(self, user) -> bool:
        pass

