
from app.utils.mongo.pydantic_object import PyObjectId
from app.schemas.propeties_schema import PropertyDetailsBase, PropertyDetailsCreate, PropertyDetailsForm
from app.repositories.properties_repo import get_properties_repo,PropertiesRepository
from app.api.v1.auth import get_current_user
from app.models.user import User
from fastapi import APIRouter, status,Depends
from fastapi import HTTPException

router = APIRouter()

from fastapi import UploadFile, File
from typing import List
from app.services.s3_services import S3StorageService

@router.post("/add-property", status_code=status.HTTP_201_CREATED)
async def create_property(
    property_in: PropertyDetailsForm = Depends(),
    images: List[UploadFile] = File(None),
    repo: PropertiesRepository = Depends(get_properties_repo),
    current_user: User = Depends(get_current_user),
    storage_service: S3StorageService = Depends(S3StorageService)  # ✅ inject instance

):
    try:
        # Prepare property data, inject current user's MongoDB id
        property_data = property_in.__dict__
        property_data["user_id"] = PyObjectId(current_user.id)
        s3_image_urls = []
        if images:
            for img in images:
                url = storage_service.upload_file(img.file, img.filename, img.content_type)
                s3_image_urls.append(url)
        property_data["images"] = s3_image_urls
        # Validate and create the property
        new_property = await repo.add_property(PropertyDetailsCreate(**property_data))
        return new_property
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating property: {str(e)}")

@router.get("/all-properties", response_model=list[PropertyDetailsBase])
async def get_all_properties(repo: PropertiesRepository = Depends(get_properties_repo)):
    try:
        properties = await repo.list_properties()
        return properties
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching properties: {str(e)}")

from fastapi import Query

@router.get("/my-properties", response_model=list[PropertyDetailsBase])
async def get_my_properties(
    repo: PropertiesRepository = Depends(get_properties_repo),
    current_user: User = Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    try:
        properties = await repo.list_properties_by_user(current_user.id, skip=skip, limit=limit)
        return properties
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user properties: {str(e)}")