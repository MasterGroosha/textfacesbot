from typing import Optional

from pydantic import BaseSettings, SecretStr, FilePath


class Settings(BaseSettings):
    bot_token: SecretStr
    drop_pending_updates: bool = False
    custom_faces_path: Optional[FilePath]
    webhook_domain: Optional[str]
    webhook_path: Optional[str]
    app_host: Optional[str] = "0.0.0.0"
    app_port: Optional[int] = 9000
    custom_bot_api: Optional[str]
    default_faces_filename = "faces_original.txt"

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'


config = Settings()
