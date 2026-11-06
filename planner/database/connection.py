from beanie import init_beanie, PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Any, List, Optional
from pydantic_settings import BaseSettings
from pydantic import BaseModel
from models.events import Event
from models.users import User


class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = "mongodb://localhost:27017/planner"

    class Config:
        env_file = ".env"


settings = Settings()


async def initialize_database():
    client = AsyncIOMotorClient(settings.DATABASE_URL)
    await init_beanie(
        database=client.get_default_database(),
        document_models=[Event, User]
    )


class Database:
    def __init__(self, model):
        self.model = model

    async def save(self, document) -> None:
        await document.create()
        return

    async def get(self, id: PydanticObjectId) -> Any:
        doc = await self.model.get(id)
        if doc:
            return doc
        return False

    async def get_all(self) -> List[Any]:
        docs = await self.model.find_all().to_list()
        return docs

    async def update(self, id: PydanticObjectId, body: BaseModel) -> Any:
        doc_id = id
        des_body = body.model_dump(exclude_unset=True) if hasattr(body, "model_dump") else body.dict(exclude_unset=True)
        des_body = {k: v for k, v in des_body.items() if v is not None}
        
        doc = await self.get(doc_id)
        if not doc:
            return False
            
        update_query = {"$set": des_body}
        await doc.update(update_query)
        return doc

    async def delete(self, id: PydanticObjectId) -> bool:
        doc = await self.get(id)
        if not doc:
            return False
        await doc.delete()
        return True