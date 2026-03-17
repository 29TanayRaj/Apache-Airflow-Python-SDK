from typing import List, Optional, Any, Dict
from pydantic import BaseModel

# --- DAG Models ---

class DagModel(BaseModel):
    dag_id: str
    is_paused: Optional[bool] = None
    is_active: Optional[bool] = None
    is_subdag: Optional[bool] = None
    description: Optional[str] = None
    fileloc: str
    file_token: str
    owners: List[str] = []
    tags: List[Dict[str, str]] = []

class DagCollection(BaseModel):
    dags: List[DagModel]
    total_entries: int

# --- DagRun Models ---

class DagRunModel(BaseModel):
    dag_run_id: str
    dag_id: str
    logical_date: Optional[str] = None
    execution_date: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    data_interval_start: Optional[str] = None
    data_interval_end: Optional[str] = None
    last_scheduling_decision: Optional[str] = None
    run_type: str
    state: str
    external_trigger: bool
    conf: Dict[str, Any] = {}

class DagRunCollection(BaseModel):
    dag_runs: List[DagRunModel]
    total_entries: int

# --- Task Models ---

class TaskModel(BaseModel):
    class_ref: Optional[Dict[str, str]] = None
    task_id: str
    owner_name: Optional[str] = None
    depends_on_past: bool = False
    wait_for_downstream: bool = False
    retries: float = 0
    queue: Optional[str] = None
    pool: Optional[str] = None
    pool_slots: float = 1.0
    execution_timeout: Optional[Dict[str, Any]] = None
    retry_delay: Optional[Dict[str, Any]] = None
    retry_exponential_backoff: bool = False
    priority_weight: float = 1.0
    weight_rule: str = "downstream"
    ui_color: str = "#fff"
    ui_fgcolor: str = "#000"
    template_fields: List[str] = []
    subdag: bool = False
    downstream_task_ids: List[str] = []

class TaskCollection(BaseModel):
    tasks: List[TaskModel]
    total_entries: int

# --- TaskInstance Models ---

class TaskInstanceModel(BaseModel):
    task_id: str
    dag_id: str
    dag_run_id: str
    execution_date: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    duration: Optional[float] = None
    state: Optional[str] = None
    try_number: int = 0
    map_index: int = -1
    max_tries: int = 0
    hostname: Optional[str] = None
    unixname: Optional[str] = None
    pool: str
    pool_slots: int
    queue: Optional[str] = None
    priority_weight: Optional[int] = None
    operator: Optional[str] = None
    queued_when: Optional[str] = None
    pid: Optional[int] = None

class TaskInstanceCollection(BaseModel):
    task_instances: List[TaskInstanceModel]
    total_entries: int

# --- DAG Source Models ---

class DagSourceModel(BaseModel):
    content: str

# --- DAG Stats Models ---

class DagStatsStateModel(BaseModel):
    state: str
    count: int

class DagStatsModel(BaseModel):
    dag_id: str
    stats: List[DagStatsStateModel]

class DagStatsCollection(BaseModel):
    dag_stats: List[DagStatsModel]
    total_entries: int

# --- DAG Version Models ---

class DagVersionModel(BaseModel):
    version_number: int
    dag_id: str
    bundle_name: str
    bundle_version: Optional[str] = None
    created_at: str

class DagVersionCollection(BaseModel):
    dag_versions: List[DagVersionModel]
    total_entries: int

# --- DAG Warning Models ---

class DagWarningModel(BaseModel):
    dag_id: str
    warning_type: str
    message: str
    timestamp: str

class DagWarningCollection(BaseModel):
    dag_warnings: List[DagWarningModel]
    total_entries: int
