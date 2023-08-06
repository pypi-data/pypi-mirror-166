from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class Insight(BaseModel):
    id: int
    resource_key: str = Field(alias='resourceKey')
    name: Optional[str]
    dw_operation_set_id: int = Field(alias='dwOperationSetId')
    operation_set_resource_key: str = Field(alias='operationSetResourceKey')
    transform_id: int = Field(alias='transformId')
    transform_arguments: Optional[Dict[str, Any]] = Field(alias='transformArguments')
    dw_table_id: int = Field(alias='dwTableId')
    fqtn: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
