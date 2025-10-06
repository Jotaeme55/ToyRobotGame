from abc import ABC, abstractmethod
from typing import Optional, TypeVar, Generic

T = TypeVar('T')


class IRepository(ABC, Generic[T]):
    """Interfaz base genérica para repositorios de persistencia"""
    
    @abstractmethod
    def save(self, entity: T) -> None:
        """Persiste la entidad"""
        pass
    
    @abstractmethod
    def load(self) -> Optional[T]:
        """Carga la entidad desde la persistencia"""
        pass
    
    @abstractmethod
    def delete(self) -> None:
        """Elimina la entidad persistida"""
        pass
    
    @abstractmethod
    def exists(self) -> bool:
        """Verifica si existe la entidad persistida"""
        pass