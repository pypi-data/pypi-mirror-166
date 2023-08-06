from typing import Optional
from pydantic import BaseModel
from enum import Enum


class LockType(Enum):
    CanNotDelete = "CanNotDelete"
    ReadOnly = "ReadOnly"


class ResourceLock(BaseModel):
    lock_type: Optional[LockType]
    """The type of lock"""

    name: str
    """The name of the lock"""

    resource: str
    """The name of the locked resource"""

    resource_group: str
    """The name of the resource group holding the locked resource"""
