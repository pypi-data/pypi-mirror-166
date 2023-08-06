"""
API Contracts for Data Warehouse Operations
"""
from typing import Dict, List, Optional, Any

from pydantic import BaseModel, Field

from pyrasgo.schemas import dw_table as dw_table_schemas


class OperationCreate(BaseModel):
    """
    Contract to create an Operation on set
    """

    operation_name: str = Field(alias='operationName')
    transform_id: Optional[int] = Field(alias='transformId')
    operation_args: Dict = Field(alias='operationArgs')
    sql_alias: Optional[str] = Field(alias="sqlAlias")

    # Prepare for deprecation
    table_dependency_names: Optional[List[str]] = Field(alias="tableDependencyNames")  # DW Table names
    table_dependency_ids: Optional[List[int]] = Field(alias="tableDependencyIds")  # DW Table ids
    table_name: Optional[str] = Field(alias="tableName")

    def __eq__(self: 'OperationCreate', other: Any) -> bool:
        """
        Comparison to determine if an OperationCreate is same as another

        Returns True if Equals; False Otherwise
        """
        # If the other class isn't a OperationCreate return comparison error
        if not isinstance(other, OperationCreate):
            return False
        return (
            self.operation_name == other.operation_name
            and self.operation_args == self.operation_args
            and self.transform_id == other.transform_id
            and self.table_dependency_names == other.table_dependency_names
            and self.table_dependency_ids == other.table_dependency_ids
            and self.table_name == other.table_name
            and self.sql_alias == other.sql_alias
        )

    class Config:
        allow_population_by_field_name = True


class OperationUpdate(BaseModel):
    """
    Contract to update an Operation on set
    """

    operation_name: Optional[str] = Field(alias='operationName')
    transform_id: Optional[int] = Field(alias='transformId')
    operation_args: Optional[Dict] = Field(alias='operationArgs')
    sql_alias: Optional[str] = Field(alias="sqlAlias")

    # Prepare for deprecation
    table_dependency_names: Optional[List[str]] = Field(alias="tableDependencyNames")  # DW Table names
    table_dependency_ids: Optional[List[int]] = Field(alias="tableDependencyIds")  # DW Table ids
    dw_operation_set_id: Optional[int] = Field(alias='dwOperationSetId')

    class Config:
        allow_population_by_field_name = True


class Operation(BaseModel):
    """
    Contract representing a Operation
    """

    id: int
    resource_key: str = Field(alias='resourceKey')
    operation_name: str = Field(alias='operationName')
    operation_args: Any = Field(alias='operationArgs')
    operation_sql: str = Field(alias='operationSQL')
    sql_alias: Optional[str] = Field(alias="sqlAlias")
    transform_id: int = Field(alias='transformId')
    dw_operation_set_id: int = Field(alias='dwOperationSetId')
    dependencies: Optional[Any]

    # Prepare for deprecation
    dw_table_id: int = Field(alias='dwTableId')
    dw_table: Optional[dw_table_schemas.DataTableWithColumns] = Field(alias='dataTable')
    table_dependencies: Optional[List[int]] = Field(alias="tableDependencies")  # DW Table ids

    class Config:
        allow_population_by_field_name = True
