from pydantic import BaseModel

class Player(BaseModel):
    player_id: int
    balance: int
    farms: List[Farm]

    async def pay(user: Player, amount: int) -> bool:
        return False

    async def add(user: Player) -> bool:
        return False

    async def remove(user: Player) -> bool:
        return False