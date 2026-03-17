from src.services.base import BaseService
from typing import Dict, Any
from src.services.admin.admin_models import ConfigModel

class ConfigRequestBuilder(BaseService):
    def get_config_request(self):
        return self._construct_request("GET", "config")

    def get_config_value_request(self, section: str, option: str):
        return self._construct_request("GET", f"config/section/{section}/option/{option}")

    def get_version_request(self):
        return self._construct_request("GET", "version")

    def get_health_request(self):
        return self._construct_request("GET", "monitor/health")

class ConfigAPI(ConfigRequestBuilder):
    def __init__(self, client):
        self.client = client

    def get_config(self) -> ConfigModel:
        raw_response = self.client.request(**self.get_config_request())
        return ConfigModel(**raw_response)

    def get_config_value(self, section: str, option: str) -> Dict[str, Any]:
        return self.client.request(**self.get_config_value_request(section, option))

    def get_version(self) -> Dict[str, Any]:
        return self.client.request(**self.get_version_request())

    def get_health(self) -> Dict[str, Any]:
        return self.client.request(**self.get_health_request())

class AsyncConfigAPI(ConfigRequestBuilder):
    def __init__(self, client):
        self.client = client

    async def get_config(self) -> ConfigModel:
        raw_response = await self.client.request(**self.get_config_request())
        return ConfigModel(**raw_response)

    async def get_config_value(self, section: str, option: str) -> Dict[str, Any]:
        return await self.client.request(**self.get_config_value_request(section, option))

    async def get_version(self) -> Dict[str, Any]:
        return await self.client.request(**self.get_version_request())

    async def get_health(self) -> Dict[str, Any]:
        return await self.client.request(**self.get_health_request())
