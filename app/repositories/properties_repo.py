
from typing import List, Optional
from uuid import UUID
from app.models.properties_model import PropertyDetails
from app.schemas.propeties_schema import PropertyDetailsCreate, PropertyDetailsUpdate

class PropertiesRepository:
    async def add_property(self, data: PropertyDetailsCreate) -> PropertyDetails:
        property(data,"flatizo")
        obj = PropertyDetails(**data.dict())
        await obj.insert()
        return obj

    async def get_property(self, property_uuid: UUID) -> Optional[PropertyDetails]:
        return await PropertyDetails.find_one(PropertyDetails.property_uuid == property_uuid)

    async def list_properties(self) -> List[PropertyDetails]:
        return await PropertyDetails.find_all().to_list()

    async def list_properties_by_user(self, user_id, skip: int = 0, limit: int = 10) -> List[PropertyDetails]:
        return await PropertyDetails.find(PropertyDetails.user_id == user_id).skip(skip).limit(limit).to_list()

    async def update_property(self, property_uuid: UUID, data: PropertyDetailsUpdate) -> Optional[PropertyDetails]:
        obj = await self.get_property(property_uuid)
        if not obj:
            return None
        for field, value in data.dict(exclude_unset=True).items():
            setattr(obj, field, value)
        await obj.save()
        return obj

    async def delete_property(self, property_uuid: UUID) -> bool:
        obj = await self.get_property(property_uuid)
        if not obj:
            return False
        await obj.delete()
        return True

properties_repo = PropertiesRepository()

def get_properties_repo():
    return properties_repo
