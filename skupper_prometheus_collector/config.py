from pydantic import (
    AnyHttpUrl,
    BaseSettings,
)


class Settings(BaseSettings):
    service_controller: AnyHttpUrl = AnyHttpUrl(
        url="http://skupper-service-controller:8888/DATA", scheme="http"
    )
    service_controller_timeout: int = 5
    port: int = 8000
    log_level: str = "INFO"

    class Config:
        env_prefix = "spc_"


settings = Settings()
