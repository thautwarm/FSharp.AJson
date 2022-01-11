from __future__ import annotations
from abc import abstractmethod
from typing import (TypeVar, List, Generic, Any)

_T = TypeVar("_T")

class Cons_1(Generic[_T]):
    @abstractmethod
    def Allocate(self, len: int) -> List[_T]:
        ...
    

def Helpers_allocateArrayFromCons(cons: Cons_1[_T], len_1: int) -> List[_T]:
    if cons is None:
        return (list)([None]*len_1)
    
    else: 
        return cons([0]*len_1)
    


def Helpers_fillImpl(array: List[_T], value: _T, start: int, count: int) -> List[_T]:
    for i in range(0, (count - 1) + 1, 1):
        array[i + start] = value
    return array


def Helpers_spliceImpl(array: List[_T], start: int, delete_count: int) -> List[_T]:
    for _ in range(1, delete_count + 1, 1):
        array.pop(start)
    return array


def Helpers_indexOfImpl(array: List[_T], item: _T, start: int) -> Any:
    try: 
        return array.index(item, start)
    
    except Exception as ex:
        return -1
    


