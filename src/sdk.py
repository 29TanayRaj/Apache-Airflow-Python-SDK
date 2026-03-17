from typing import Optional

from src.core.client import APIClient
from src.services.dags import DagsAPI, DagRunsAPI, TasksAPI, TaskInstancesAPI, DagSourcesAPI, DagStatsAPI, DagVersionsAPI, DagWarningsAPI
from src.services.admin import ConfigAPI, ConnectionsAPI, EventLogsAPI, ImportErrorsAPI, JobsAPI, PluginsAPI, PoolsAPI, ProvidersAPI, VariablesAPI
from src.services.assets import AssetsAPI
from src.services.backfills import BackfillsAPI

class AirflowSDK:
    """
    Main Facade class for the synchronous Airflow Python SDK.
    
    Usage:
        from src import AirflowSDK
        client = AirflowSDK("http://localhost:8080", "admin", "admin")
        dags = client.dags.list()
    """
    def __init__(self, 
                base_url: str, 
                username: Optional[str] = None, 
                password: Optional[str] = None, 
                retries: int = 3):
        
        self.client = APIClient(base_url=base_url, 
                                username=username, 
                                password=password, 
                                retries=retries)
        
        # DAG Management
        self.dags = DagsAPI(self.client)
        self.dag_runs = DagRunsAPI(self.client)
        self.dag_sources = DagSourcesAPI(self.client)
        self.dag_stats = DagStatsAPI(self.client)
        self.dag_versions = DagVersionsAPI(self.client)
        self.dag_warnings = DagWarningsAPI(self.client)
        self.tasks = TasksAPI(self.client)
        self.task_instances = TaskInstancesAPI(self.client)
        
        # Admin & Config
        self.config = ConfigAPI(self.client)
        self.connections = ConnectionsAPI(self.client)
        self.event_logs = EventLogsAPI(self.client)
        self.import_errors = ImportErrorsAPI(self.client)
        self.jobs = JobsAPI(self.client)
        self.plugins = PluginsAPI(self.client)
        self.pools = PoolsAPI(self.client)
        self.providers = ProvidersAPI(self.client)
        self.variables = VariablesAPI(self.client)
        
        # Other
        self.assets = AssetsAPI(self.client)
        self.backfills = BackfillsAPI(self.client)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.client.close()
