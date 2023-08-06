from typing import Optional

from pydantic import BaseModel, Field

from vdb_schema.gender import GenderModel


class CustomerModel(BaseModel):
    customer_created_on: Optional[str] = Field(alias="customer_created_on")
    customer_modified_on: Optional[str] = Field(alias="customer_modified_on")
    customer_id: str = Field(alias="customer_id")
    birthday: Optional[str] = Field(alias="birthday")
    gender: Optional[GenderModel] = Field(alias="gender")
    new_created: Optional[bool] = Field(alias="new_created", default=False)
    new_updated: Optional[bool] = Field(alias="new_updated", default=False)
    UserDetail_UDKey: int = Field(alias="UserDetail_UDKey")
