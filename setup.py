from setuptools import setup, find_packages

setup(
    name="AirflowSDK",
    version="0.1.0",
    description="A lightweight and easy-to-use Python SDK for interacting with the Apache Airflow Stable REST API.",
    author="AirflowSDK Contributors",
    packages=find_packages(),
    install_requires=[
        "httpx>=0.24.0",
        "pydantic>=2.0.0",
        "anyio>=3.0.0"
    ],
    python_requires=">=3.8",
)
