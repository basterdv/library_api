from pydantic import BaseModel, Field, ConfigDict


class SUserID(BaseModel):
    id: int = Field(description="ID пользователя")
    model_config = ConfigDict(from_attributes=True)


class SUserRole(BaseModel):
    is_admin: bool = Field(description="Идентификатор администратора")
    model_config = ConfigDict(from_attributes=True)
