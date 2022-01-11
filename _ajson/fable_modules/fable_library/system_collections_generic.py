from __future__ import annotations
from typing import (TypeVar, Any, Generic, List)
from .array import (fill, copy_to, initialize)
from .reflection import (TypeInfo, class_type)
from .seq import (delay, enumerate_while, append, singleton, empty, to_array)
from .util import (compare, IComparer, equals, structural_hash, IEqualityComparer, get_enumerator, IEnumerable, IEnumerator, to_iterator, max, compare_primitives)

_T = TypeVar("_T")

def expr_10(gen0: TypeInfo) -> TypeInfo:
    return class_type("System.Collections.Generic.Comparer`1", [gen0], Comparer_1)


class Comparer_1(Generic[_T]):
    def Compare(self, x: _T, y: _T=None) -> int:
        return compare(x, y)
    

Comparer_1_reflection = expr_10

def Comparer_1__ctor() -> Comparer_1[Any]:
    return Comparer_1()


def Comparer_1_get_Default() -> IComparer[Any]:
    class ObjectExpr11(IComparer[_T]):
        def Compare(self, x: _T, y: _T=None) -> int:
            return compare(x, y)
        
    return ObjectExpr11()


def expr_12(gen0: TypeInfo) -> TypeInfo:
    return class_type("System.Collections.Generic.EqualityComparer`1", [gen0], EqualityComparer_1)


class EqualityComparer_1(Generic[_T]):
    def __eq__(self, x: _T, y: _T=None) -> bool:
        return equals(x, y)
    
    def GetHashCode(self, x: Any=None) -> int:
        return structural_hash(x)
    

EqualityComparer_1_reflection = expr_12

def EqualityComparer_1__ctor() -> EqualityComparer_1[Any]:
    return EqualityComparer_1()


def EqualityComparer_1_get_Default() -> IEqualityComparer[Any]:
    class ObjectExpr13(IEqualityComparer[Any]):
        def Equals(self, x: _T, y: _T=None) -> bool:
            return equals(x, y)
        
        def GetHashCode(self, x_1: Any=None) -> int:
            return structural_hash(x_1)
        
    return ObjectExpr13()


def expr_18(gen0: TypeInfo) -> TypeInfo:
    return class_type("System.Collections.Generic.Stack`1", [gen0], Stack_1)


class Stack_1(Generic[_T]):
    def __init__(self, initial_contents: List[_T], initial_count: int) -> None:
        self.contents = initial_contents
        self.count = initial_count or 0
    
    def GetEnumerator(self) -> IEnumerator[Any]:
        this : Stack_1[_T] = self
        def arrow_17(_unit: Any=None) -> IEnumerable[Any]:
            index : int = (this.count - 1) or 0
            def arrow_14(_unit: Any=None) -> bool:
                return index >= 0
            
            def arrow_16(_unit: Any=None) -> IEnumerable[Any]:
                def arrow_15(_unit: Any=None) -> IEnumerable[Any]:
                    nonlocal index
                    index = (index - 1) or 0
                    return empty()
                
                return append(singleton(this.contents[index]), delay(arrow_15))
            
            return enumerate_while(arrow_14, delay(arrow_16))
        
        return get_enumerator(delay(arrow_17))
    
    def __iter__(self) -> IEnumerator[Any]:
        return to_iterator(self.GetEnumerator())
    
    def System_Collections_IEnumerable_GetEnumerator(self) -> IEnumerator[Any]:
        this : Stack_1[_T] = self
        return get_enumerator(this)
    

Stack_1_reflection = expr_18

def Stack_1__ctor_Z2E171D71(initial_contents: List[_T], initial_count: int) -> Stack_1[_T]:
    return Stack_1(initial_contents, initial_count)


def Stack_1__ctor_Z524259A4(initial_capacity: int) -> Stack_1[Any]:
    return Stack_1__ctor_Z2E171D71(fill([0] * initial_capacity, 0, initial_capacity, None), 0)


def Stack_1__ctor() -> Stack_1[Any]:
    return Stack_1__ctor_Z524259A4(4)


def Stack_1__ctor_BB573A(xs: IEnumerable[_T]) -> Stack_1[_T]:
    arr : List[_T] = list(xs)
    return Stack_1__ctor_Z2E171D71(arr, len(arr))


def Stack_1__Ensure_Z524259A4(this: Stack_1[Any], new_size: int) -> None:
    old_size : int = len(this.contents) or 0
    if new_size > old_size:
        old : List[_T] = this.contents
        def arrow_20(x: int, y: int, this: Stack_1[_T]=this, new_size: int=new_size) -> int:
            return compare_primitives(x, y)
        
        def arrow_21(x: int, y: int, this: Stack_1[_T]=this, new_size: int=new_size) -> int:
            return compare_primitives(x, y)
        
        this.contents = fill([0] * max(arrow_20, new_size, old_size * 2), 0, max(arrow_21, new_size, old_size * 2), None)
        copy_to(old, 0, this.contents, 0, this.count)
    


def Stack_1__get_Count(this: Stack_1[Any]) -> int:
    return this.count


def Stack_1__Pop(this: Stack_1[_T]) -> _T:
    this.count = (this.count - 1) or 0
    return this.contents[this.count]


def Stack_1__Peek(this: Stack_1[_T]) -> _T:
    return this.contents[this.count - 1]


def Stack_1__Contains_2B595(this: Stack_1[_T], x: _T=None) -> bool:
    found : bool = False
    i : int = 0
    while not found if (i < this.count) else (False):
        if equals(x, this.contents[i]):
            found = True
        
        else: 
            i = (i + 1) or 0
        
    return found


def Stack_1__TryPeek_1F3DB691(this: Stack_1[_T], result: Any) -> bool:
    if this.count > 0:
        result.contents = Stack_1__Peek(this)
        return True
    
    else: 
        return False
    


def Stack_1__TryPop_1F3DB691(this: Stack_1[_T], result: Any) -> bool:
    if this.count > 0:
        result.contents = Stack_1__Pop(this)
        return True
    
    else: 
        return False
    


def Stack_1__Push_2B595(this: Stack_1[_T], x: _T=None) -> None:
    Stack_1__Ensure_Z524259A4(this, this.count + 1)
    this.contents[this.count] = x
    this.count = (this.count + 1) or 0


def Stack_1__Clear(this: Stack_1[Any]) -> None:
    this.count = 0
    fill(this.contents, 0, len(this.contents), None)


def Stack_1__TrimExcess(this: Stack_1[Any]) -> None:
    if (this.count / len(this.contents)) > 0.9:
        Stack_1__Ensure_Z524259A4(this, this.count)
    


def Stack_1__ToArray(this: Stack_1[_T]) -> List[_T]:
    def arrow_22(i: int, this: Stack_1[_T]=this) -> Any:
        return this.contents[(this.count - 1) - i]
    
    return initialize(this.count, arrow_22, None)


def expr_23(gen0: TypeInfo) -> TypeInfo:
    return class_type("System.Collections.Generic.Queue`1", [gen0], Queue_1)


class Queue_1(Generic[_T]):
    def __init__(self, initial_contents: List[_T], initial_count: int) -> None:
        self.contents = initial_contents
        self.count = initial_count or 0
        self.head = 0
        self.tail = initial_count or 0
    
    def GetEnumerator(self) -> IEnumerator[Any]:
        this : Queue_1[_T] = self
        return get_enumerator(Queue_1__toSeq(this))
    
    def __iter__(self) -> IEnumerator[Any]:
        return to_iterator(self.GetEnumerator())
    
    def System_Collections_IEnumerable_GetEnumerator(self) -> IEnumerator[Any]:
        this : Queue_1[_T] = self
        return get_enumerator(this)
    

Queue_1_reflection = expr_23

def Queue_1__ctor_Z2E171D71(initial_contents: List[_T], initial_count: int) -> Queue_1[_T]:
    return Queue_1(initial_contents, initial_count)


def Queue_1__ctor_Z524259A4(initial_capacity: int) -> Queue_1[Any]:
    if initial_capacity < 0:
        raise Exception("capacity is less than 0")
    
    return Queue_1__ctor_Z2E171D71(fill([0] * initial_capacity, 0, initial_capacity, None), 0)


def Queue_1__ctor() -> Queue_1[Any]:
    return Queue_1__ctor_Z524259A4(4)


def Queue_1__ctor_BB573A(xs: IEnumerable[_T]) -> Queue_1[_T]:
    arr : List[_T] = list(xs)
    return Queue_1__ctor_Z2E171D71(arr, len(arr))


def Queue_1__get_Count(_: Queue_1[Any]) -> int:
    return _.count


def Queue_1__Enqueue_2B595(_: Queue_1[_T], value: _T=None) -> None:
    if _.count == Queue_1__size(_):
        Queue_1__ensure_Z524259A4(_, _.count + 1)
    
    _.contents[_.tail] = value
    _.tail = ((_.tail + 1) % Queue_1__size(_)) or 0
    _.count = (_.count + 1) or 0


def Queue_1__Dequeue(_: Queue_1[_T]) -> _T:
    if _.count == 0:
        raise Exception("Queue is empty")
    
    value : _T = _.contents[_.head]
    _.head = ((_.head + 1) % Queue_1__size(_)) or 0
    _.count = (_.count - 1) or 0
    return value


def Queue_1__Peek(_: Queue_1[_T]) -> _T:
    if _.count == 0:
        raise Exception("Queue is empty")
    
    return _.contents[_.head]


def Queue_1__TryDequeue_1F3DB691(this: Queue_1[_T], result: Any) -> bool:
    if this.count == 0:
        return False
    
    else: 
        result.contents = Queue_1__Dequeue(this)
        return True
    


def Queue_1__TryPeek_1F3DB691(this: Queue_1[_T], result: Any) -> bool:
    if this.count == 0:
        return False
    
    else: 
        result.contents = Queue_1__Peek(this)
        return True
    


def Queue_1__Contains_2B595(this: Queue_1[_T], x: _T=None) -> bool:
    found : bool = False
    i : int = 0
    while not found if (i < this.count) else (False):
        if equals(x, this.contents[Queue_1__toIndex_Z524259A4(this, i)]):
            found = True
        
        else: 
            i = (i + 1) or 0
        
    return found


def Queue_1__Clear(this: Queue_1[Any]) -> None:
    this.count = 0
    this.head = 0
    this.tail = 0
    fill(this.contents, 0, Queue_1__size(this), None)


def Queue_1__TrimExcess(this: Queue_1[Any]) -> None:
    if (this.count / len(this.contents)) > 0.9:
        Queue_1__ensure_Z524259A4(this, this.count)
    


def Queue_1__ToArray(this: Queue_1[_T]) -> List[_T]:
    return to_array(Queue_1__toSeq(this))


def Queue_1__CopyTo_Z2E171D71(this: Queue_1[_T], target: List[_T], start: int) -> None:
    i : int = start or 0
    with get_enumerator(Queue_1__toSeq(this)) as enumerator:
        while enumerator.System_Collections_IEnumerator_MoveNext():
            item : _T = enumerator.System_Collections_Generic_IEnumerator_00601_get_Current()
            target[i] = item
            i = (i + 1) or 0


def Queue_1__size(this: Queue_1[Any]) -> int:
    return len(this.contents)


def Queue_1__toIndex_Z524259A4(this: Queue_1[Any], i: int) -> int:
    return (this.head + i) % Queue_1__size(this)


def Queue_1__ensure_Z524259A4(this: Queue_1[Any], required_size: int) -> None:
    new_buffer : List[_T] = fill([0] * required_size, 0, required_size, None)
    if this.head < this.tail:
        copy_to(this.contents, this.head, new_buffer, 0, this.count)
    
    else: 
        copy_to(this.contents, this.head, new_buffer, 0, Queue_1__size(this) - this.head)
        copy_to(this.contents, 0, new_buffer, Queue_1__size(this) - this.head, this.tail)
    
    this.head = 0
    this.tail = this.count or 0
    this.contents = new_buffer


def Queue_1__toSeq(this: Queue_1[_T]) -> IEnumerable[_T]:
    def arrow_27(this: Queue_1[_T]=this) -> IEnumerable[Any]:
        i : int = 0
        def arrow_24(_unit: Any=None) -> bool:
            return i < this.count
        
        def arrow_26(_unit: Any=None) -> IEnumerable[Any]:
            def arrow_25(_unit: Any=None) -> IEnumerable[Any]:
                nonlocal i
                i = (i + 1) or 0
                return empty()
            
            return append(singleton(this.contents[Queue_1__toIndex_Z524259A4(this, i)]), delay(arrow_25))
        
        return enumerate_while(arrow_24, delay(arrow_26))
    
    return delay(arrow_27)


