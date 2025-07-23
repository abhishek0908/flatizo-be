from abc import ABC, abstractmethod
from typing import BinaryIO

class StorageService(ABC):
    @abstractmethod
    def upload_file(self, file: BinaryIO, filename: str, content_type: str) -> str:
        pass
    
    @abstractmethod
    def delete_file(self, file_url: str) -> None:
       pass