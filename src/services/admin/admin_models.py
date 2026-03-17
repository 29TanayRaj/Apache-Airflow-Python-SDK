from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field

# --- Pool Models ---

class PoolModel(BaseModel):
    name: str
    slots: int
    occupied_slots: int
    running_slots: int
    queued_slots: int
    open_slots: int
    description: Optional[str] = None

class PoolCollection(BaseModel):
    pools: List[PoolModel]
    total_entries: int

class PoolCreateRequest(BaseModel):
    name: str
    slots: int
    description: Optional[str] = None

# --- Variable Models ---

class VariableModel(BaseModel):
    key: str
    value: Optional[str] = None
    description: Optional[str] = None

class VariableCollection(BaseModel):
    variables: List[VariableModel]
    total_entries: int

class VariableCreateRequest(BaseModel):
    key: str
    value: str
    description: Optional[str] = None

# --- Connection Models ---

class ConnectionModel(BaseModel):
    connection_id: str
    conn_type: str
    description: Optional[str] = None
    host: Optional[str] = None
    login: Optional[str] = None
    schema_: Optional[str] = Field(None, alias='schema')
    port: Optional[int] = None
    extra: Optional[str] = None

class ConnectionCollection(BaseModel):
    connections: List[ConnectionModel]
    total_entries: int

class ConnectionCreateRequest(BaseModel):
    connection_id: str
    conn_type: str
    description: Optional[str] = None
    host: Optional[str] = None
    login: Optional[str] = None
    schema_: Optional[str] = Field(None, alias='schema')
    port: Optional[int] = None
    password: Optional[str] = None
    extra: Optional[str] = None

# --- Config Models ---

class ConfigOptionModel(BaseModel):
    key: str
    value: str

class ConfigSectionModel(BaseModel):
    name: str
    options: List[ConfigOptionModel]

class ConfigModel(BaseModel):
    sections: List[ConfigSectionModel]

# --- Provider Models ---

class ProviderModel(BaseModel):
    package_name: str
    description: str
    version: str

class ProviderCollection(BaseModel):
    providers: List[ProviderModel]
    total_entries: int

# --- Plugin Models ---

class PluginModel(BaseModel):
    name: Optional[str] = None
    constants: List[Any] = []
    exclude_from_webui: bool = False
    flask_blueprints: List[Any] = []
    fastapi_apps: List[Any] = []
    global_operator_extra_links: List[Any] = []
    macros: List[Any] = []
    operator_extra_links: List[Any] = []
    source: Optional[str] = None

class PluginCollection(BaseModel):
    plugins: List[PluginModel]
    total_entries: int
