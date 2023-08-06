from enum import Enum


class DataType(Enum):
    SMALLINT = 'smallint'
    BIGINT = 'bigint'
    INT = 'int'
    INTEGER = 'integer'
    TINYINT = 'tinyint'
    BYTEINT = 'byteint'
    FLOAT = 'float'
    FLOAT4 = 'float4'
    FLOAT8 = 'float8'
    FLOAT64 = 'float64'
    DECIMAL = 'decimal'
    NUMERIC = 'numeric'
    NUMBER = 'number'
    REAL = 'real'
    DOUBLE = 'double'
    STRING = 'string'
    TEXT = 'text'
    VARCHAR = 'varchar'
    CHAR = 'char'
    CHARACTER = 'character'
    DATE = 'date'
    DATETIME = 'datetime'
    TIME = 'time'
    TIMESTAMP = 'timestamp'
    TIMESTAMP_LTZ = 'timestamp_ltz'
    TIMESTAMP_NTZ = 'timestamp_ntz'
    TIMESTAMP_TZ = 'timestamp_tz'
    BINARY = 'binary'
    VARBINARY = 'varbinary'
    BOOLEAN = 'boolean'
    BOOL = 'bool'
    VARIANT = 'variant'
    OBJECT = 'object'
    ARRAY = 'array'


class OperationSetAsyncTaskType(str, Enum):
    FORK = "FORK"
    REVALIDATE = "REVALIDATE"
    UPDATE = "UPDATE"
    ACCELERATE = "ACCELERATE"


class DataWarehouseType(Enum):
    """
    Supported Data Warehouses
    """

    BIGQUERY = "bigquery"
    SNOWFLAKE = "snowflake"
