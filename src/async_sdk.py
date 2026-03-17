from typing import Optional

from src.core.async_client import AsyncAPIClient
from src.services.dags import AsyncDagsAPI, AsyncDagRunsAPI, AsyncTasksAPI, AsyncTaskInstancesAPI, AsyncDagSourcesAPI, AsyncDagStatsAPI, AsyncDagVersionsAPI, AsyncDagWarningsAPI
from src.services.admin import AsyncConfigAPI, AsyncConnectionsAPI, AsyncEventLogsAPI, AsyncImportErrorsAPI, AsyncJobsAPI, AsyncPluginsAPI, AsyncPoolsAPI, AsyncProvidersAPI, AsyncVariablesAPI
from src.services.assets import AsyncAssetsAPI
from src.services.backfills import AsyncBackfillsAPI

class AsyncAirflowSDK:
    """
    Main Facade class for the asynchronous Airflow Python SDK.
    
    Usage:
        from src import AsyncAirflowSDK
        async with AsyncAirflowSDK("http://localhost:8080", "admin", "admin") as client:
            dags = await client.dags.list()
    """
    def __init__(self, base_url: str,
                       username: Optional[str] = None, 
                       password: Optional[str] = None, 
                       retries: int = 3):
        """
        Initialize the AsyncAirflowSDK.
        
        Args:
            base_url: The base URL of the Airflow API.
            username: The username for authentication.
            password: The password for authentication.
            retries: The number of retries for failed requests.
        """
        self.client = AsyncAPIClient(base_url=base_url, 
                                     username=username, 
                                     password=password, 
                                     retries=retries)
        
        # DAG Management
        self.dags = AsyncDagsAPI(self.client)
        self.dag_runs = AsyncDagRunsAPI(self.client)
        self.dag_sources = AsyncDagSourcesAPI(self.client)
        self.dag_stats = AsyncDagStatsAPI(self.client)
        self.dag_versions = AsyncDagVersionsAPI(self.client)
        self.dag_warnings = AsyncDagWarningsAPI(self.client)
        self.tasks = AsyncTasksAPI(self.client)
        self.task_instances = AsyncTaskInstancesAPI(self.client)
        
        # Admin & Config
        self.config = AsyncConfigAPI(self.client)
        self.connections = AsyncConnectionsAPI(self.client)
        self.event_logs = AsyncEventLogsAPI(self.client)
        self.import_errors = AsyncImportErrorsAPI(self.client)
        self.jobs = AsyncJobsAPI(self.client)
        self.plugins = AsyncPluginsAPI(self.client)
        self.pools = AsyncPoolsAPI(self.client)
        self.providers = AsyncProvidersAPI(self.client)
        self.variables = AsyncVariablesAPI(self.client)
        
        # Other
        self.assets = AsyncAssetsAPI(self.client)
        self.backfills = AsyncBackfillsAPI(self.client)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        await self.client.close()
