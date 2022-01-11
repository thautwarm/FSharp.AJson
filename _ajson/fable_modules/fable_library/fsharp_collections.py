from typing import (TypeVar, Callable, Any)
from .util import (IEqualityComparer, structural_hash, equals, physical_hash, IComparer, compare)

_T = TypeVar("_T")

def HashIdentity_FromFunctions(hash_1: Callable[[_T], int], eq: Callable[[_T, _T], bool]) -> IEqualityComparer[Any]:
    class ObjectExpr0(IEqualityComparer[Any]):
        def Equals(self, x: _T, y: _T=None, hash_1: Callable[[_T], int]=hash_1, eq: Callable[[_T, _T], bool]=eq) -> bool:
            return eq(x, y)
        
        def GetHashCode(self, x_1: Any=None, hash_1: Callable[[_T], int]=hash_1, eq: Callable[[_T, _T], bool]=eq) -> int:
            return hash_1(x_1)
        
    return ObjectExpr0()


def HashIdentity_Structural() -> IEqualityComparer[Any]:
    def arrow_1(obj: Any=None) -> int:
        return structural_hash(obj)
    
    def arrow_2(e1: _T, e2: _T=None) -> bool:
        return equals(e1, e2)
    
    return HashIdentity_FromFunctions(arrow_1, arrow_2)


def HashIdentity_Reference() -> IEqualityComparer[Any]:
    def arrow_3(obj: Any=None) -> int:
        return physical_hash(obj)
    
    def arrow_4(e1: _T, e2: _T=None) -> bool:
        return e1 is e2
    
    return HashIdentity_FromFunctions(arrow_3, arrow_4)


def ComparisonIdentity_FromFunction(comparer: Callable[[_T, _T], int]) -> IComparer[_T]:
    class ObjectExpr5(IComparer[_T]):
        def Compare(self, x: _T, y: _T=None, comparer: Callable[[_T, _T], int]=comparer) -> int:
            return comparer(x, y)
        
    return ObjectExpr5()


def ComparisonIdentity_Structural() -> IComparer[Any]:
    def arrow_6(e1: _T, e2: _T=None) -> int:
        return compare(e1, e2)
    
    return ComparisonIdentity_FromFunction(arrow_6)


