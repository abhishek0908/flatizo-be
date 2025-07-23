from bson import ObjectId

class PyObjectId(ObjectId):
    """
    Pydantic-compatible ObjectId type for MongoDB fields.
    Use this as the type for any ObjectId field in your Pydantic models.
    Handles validation, OpenAPI schema, and JSON serialization as string.
    
    Usage:
        from app.utils.mongo.pydantic_object import PyObjectId
        class MyModel(BaseModel):
            id: PyObjectId
            model_config = {"arbitrary_types_allowed": True}
    """
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core import core_schema
        return core_schema.json_or_python_schema(
            python_schema=core_schema.with_info_plain_validator_function(cls.validate),
            json_schema=core_schema.with_info_plain_validator_function(cls.validate),
            serialization=core_schema.plain_serializer_function_ser_schema(lambda v: str(v)),
        )

    @classmethod
    def validate(cls, v, info=None):
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str) and ObjectId.is_valid(v):
            return ObjectId(v)
        raise ValueError("Invalid ObjectId")

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        return {"type": "string"}

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        return {"type": "string"}

        return {"type": "string"}