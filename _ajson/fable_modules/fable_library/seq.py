from __future__ import annotations
from typing import (Any, TypeVar, Callable, Generic, Tuple, List)
from .array import (singleton as singleton_1, try_find_back as try_find_back_1, try_find_index_back as try_find_index_back_1, fold_back as fold_back_1, fold_back2 as fold_back2_1, try_head as try_head_1, try_item as try_item_1, map_fold as map_fold_1, map_fold_back as map_fold_back_1, reduce_back as reduce_back_1, reverse as reverse_1, scan_back as scan_back_1, pairwise as pairwise_1, map as map_1, split_into as split_into_1, windowed as windowed_1, transpose as transpose_1, permute as permute_1, chunk_by_size as chunk_by_size_1)
from .fsharp_core import (Operators_NullArg, Operators_Lock)
from .global_ import (IGenericAdder_1, IGenericAverager_1, SR_indexOutOfBounds)
from .list import (FSharpList, to_array as to_array_1, of_array as of_array_1, of_seq as of_seq_1, try_head as try_head_2, is_empty as is_empty_1, try_item as try_item_2, length as length_1)
from .option import (Option, value as value_1, some)
from .reflection import (TypeInfo, class_type)
from .types import to_string
from .util import (get_enumerator, IEnumerator, to_iterator, IDisposable, is_disposable, dispose as dispose_2, IEnumerable, is_array_like, IEqualityComparer, equals, ignore, clear, IComparer)

_T = TypeVar("_T")

_U = TypeVar("_U")

_STATE = TypeVar("_STATE")

__A = TypeVar("__A")

__B = TypeVar("__B")

_T1 = TypeVar("_T1")

_T2 = TypeVar("_T2")

_T3 = TypeVar("_T3")

_RESULT = TypeVar("_RESULT")

SR_enumerationAlreadyFinished : str = "Enumeration already finished."

SR_enumerationNotStarted : str = "Enumeration has not started. Call MoveNext."

SR_inputSequenceEmpty : str = "The input sequence was empty."

SR_inputSequenceTooLong : str = "The input sequence contains more than one element."

SR_keyNotFoundAlt : str = "An index satisfying the predicate was not found in the collection."

SR_notEnoughElements : str = "The input sequence has an insufficient number of elements."

SR_resetNotSupported : str = "Reset is not supported on this enumerator."

def Enumerator_noReset() -> Any:
    raise Exception(SR_resetNotSupported)


def Enumerator_notStarted() -> Any:
    raise Exception(SR_enumerationNotStarted)


def Enumerator_alreadyFinished() -> Any:
    raise Exception(SR_enumerationAlreadyFinished)


def expr_147(gen0: TypeInfo) -> TypeInfo:
    return class_type("SeqModule.Enumerator.Seq", [gen0], Enumerator_Seq)


class Enumerator_Seq(Generic[_T]):
    def __init__(self, f: Callable[[], IEnumerator[_T]]) -> None:
        self.f = f
    
    def __str__(self) -> str:
        xs : Enumerator_Seq[_T] = self
        max_count : int = 4
        i : int = 0
        str_1 : str = "seq ["
        with get_enumerator(xs) as e:
            while e.System_Collections_IEnumerator_MoveNext() if (i < max_count) else (False):
                if i > 0:
                    str_1 = str_1 + "; "
                
                str_1 = str_1 + to_string(e.System_Collections_Generic_IEnumerator_00601_get_Current())
                i = (i + 1) or 0
            if i == max_count:
                str_1 = str_1 + "; ..."
            
            return str_1 + "]"
    
    def GetEnumerator(self) -> IEnumerator[Any]:
        x : Enumerator_Seq[_T] = self
        return x.f()
    
    def __iter__(self) -> IEnumerator[Any]:
        return to_iterator(self.GetEnumerator())
    
    def System_Collections_IEnumerable_GetEnumerator(self) -> IEnumerator[Any]:
        x : Enumerator_Seq[_T] = self
        return x.f()
    

Enumerator_Seq_reflection = expr_147

def Enumerator_Seq__ctor_673A07F2(f: Callable[[], IEnumerator[_T]]) -> Enumerator_Seq[_T]:
    return Enumerator_Seq(f)


def expr_148(gen0: TypeInfo) -> TypeInfo:
    return class_type("SeqModule.Enumerator.FromFunctions`1", [gen0], Enumerator_FromFunctions_1)


class Enumerator_FromFunctions_1(IDisposable, Generic[_T]):
    def __init__(self, current: Callable[[], _T], next_1: Callable[[], bool], dispose: Callable[[], None]) -> None:
        self.current = current
        self.next = next_1
        self.dispose = dispose
    
    def System_Collections_Generic_IEnumerator_00601_get_Current(self) -> Any:
        __ : Enumerator_FromFunctions_1[_T] = self
        return __.current()
    
    def System_Collections_IEnumerator_get_Current(self) -> Any:
        __ : Enumerator_FromFunctions_1[_T] = self
        return __.current()
    
    def System_Collections_IEnumerator_MoveNext(self) -> bool:
        __ : Enumerator_FromFunctions_1[_T] = self
        return __.next()
    
    def System_Collections_IEnumerator_Reset(self) -> None:
        Enumerator_noReset()
    
    def Dispose(self) -> None:
        __ : Enumerator_FromFunctions_1[_T] = self
        __.dispose()
    

Enumerator_FromFunctions_1_reflection = expr_148

def Enumerator_FromFunctions_1__ctor_58C54629(current: Callable[[], _T], next_1: Callable[[], bool], dispose: Callable[[], None]) -> Enumerator_FromFunctions_1[_T]:
    return Enumerator_FromFunctions_1(current, next_1, dispose)


def Enumerator_cast(e: IEnumerator[Any]) -> IEnumerator[Any]:
    def current(e: IEnumerator[Any]=e) -> Any:
        return e.System_Collections_IEnumerator_get_Current()
    
    def next_1(e: IEnumerator[Any]=e) -> bool:
        return e.System_Collections_IEnumerator_MoveNext()
    
    def dispose(e: IEnumerator[Any]=e) -> None:
        if is_disposable(e):
            dispose_2(e)
        
    
    return Enumerator_FromFunctions_1__ctor_58C54629(current, next_1, dispose)


def Enumerator_concat(sources: IEnumerable[Any]) -> IEnumerator[Any]:
    outer_opt : Option[IEnumerator[_U]] = None
    inner_opt : Option[IEnumerator[_T]] = None
    started : bool = False
    finished : bool = False
    curr : Option[_T] = None
    def finish(sources: IEnumerable[_U]=sources) -> None:
        nonlocal finished, inner_opt, outer_opt
        finished = True
        if inner_opt is not None:
            inner : IEnumerator[_T] = inner_opt
            try: 
                dispose_2(inner)
            
            finally: 
                inner_opt = None
            
        
        if outer_opt is not None:
            outer : IEnumerator[_U] = outer_opt
            try: 
                dispose_2(outer)
            
            finally: 
                outer_opt = None
            
        
    
    def current(sources: IEnumerable[_U]=sources) -> Any:
        if not started:
            Enumerator_notStarted()
        
        elif finished:
            Enumerator_alreadyFinished()
        
        if curr is not None:
            return value_1(curr)
        
        else: 
            return Enumerator_alreadyFinished()
        
    
    def next_1(sources: IEnumerable[_U]=sources) -> bool:
        nonlocal started
        if not started:
            started = True
        
        if finished:
            return False
        
        else: 
            res : Option[bool] = None
            while res is None:
                nonlocal curr, inner_opt, outer_opt
                match_value : Tuple[Option[IEnumerator[_U]], Option[IEnumerator[_T]]] = (outer_opt, inner_opt)
                if match_value[0] is not None:
                    if match_value[1] is not None:
                        inner_1 : IEnumerator[_T] = match_value[1]
                        if inner_1.System_Collections_IEnumerator_MoveNext():
                            curr = some(inner_1.System_Collections_Generic_IEnumerator_00601_get_Current())
                            res = True
                        
                        else: 
                            try: 
                                dispose_2(inner_1)
                            
                            finally: 
                                inner_opt = None
                            
                        
                    
                    else: 
                        outer_1 : IEnumerator[_U] = match_value[0]
                        if outer_1.System_Collections_IEnumerator_MoveNext():
                            ie : _U = outer_1.System_Collections_Generic_IEnumerator_00601_get_Current()
                            def arrow_149(_unit: Any=None) -> IEnumerator[Any]:
                                copy_of_struct : _U = ie
                                return get_enumerator(copy_of_struct)
                            
                            inner_opt = arrow_149()
                        
                        else: 
                            finish()
                            res = False
                        
                    
                
                else: 
                    outer_opt = get_enumerator(sources)
                
            return value_1(res)
        
    
    def dispose(sources: IEnumerable[_U]=sources) -> None:
        if not finished:
            finish()
        
    
    return Enumerator_FromFunctions_1__ctor_58C54629(current, next_1, dispose)


def Enumerator_enumerateThenFinally(f: Callable[[], None], e: IEnumerator[_T]) -> IEnumerator[_T]:
    def current(f: Callable[[], None]=f, e: IEnumerator[_T]=e) -> Any:
        return e.System_Collections_Generic_IEnumerator_00601_get_Current()
    
    def next_1(f: Callable[[], None]=f, e: IEnumerator[_T]=e) -> bool:
        return e.System_Collections_IEnumerator_MoveNext()
    
    def dispose(f: Callable[[], None]=f, e: IEnumerator[_T]=e) -> None:
        try: 
            dispose_2(e)
        
        finally: 
            f()
        
    
    return Enumerator_FromFunctions_1__ctor_58C54629(current, next_1, dispose)


def Enumerator_generateWhileSome(openf: Callable[[], _T], compute: Callable[[_T], Option[_U]], closef: Callable[[_T], None]) -> IEnumerator[_U]:
    started : bool = False
    curr : Option[_U] = None
    state : Option[_T] = some(openf())
    def dispose(openf: Callable[[], _T]=openf, compute: Callable[[_T], Option[_U]]=compute, closef: Callable[[_T], None]=closef) -> None:
        nonlocal state
        if state is not None:
            x_1 : _T = value_1(state)
            try: 
                closef(x_1)
            
            finally: 
                state = None
            
        
    
    def finish(openf: Callable[[], _T]=openf, compute: Callable[[_T], Option[_U]]=compute, closef: Callable[[_T], None]=closef) -> None:
        nonlocal curr
        try: 
            dispose()
        
        finally: 
            curr = None
        
    
    def current(openf: Callable[[], _T]=openf, compute: Callable[[_T], Option[_U]]=compute, closef: Callable[[_T], None]=closef) -> Any:
        if not started:
            Enumerator_notStarted()
        
        if curr is not None:
            return value_1(curr)
        
        else: 
            return Enumerator_alreadyFinished()
        
    
    def next_1(openf: Callable[[], _T]=openf, compute: Callable[[_T], Option[_U]]=compute, closef: Callable[[_T], None]=closef) -> bool:
        nonlocal started, curr
        if not started:
            started = True
        
        if state is not None:
            s : _T = value_1(state)
            match_value_1 : Option[_U]
            try: 
                match_value_1 = compute(s)
            
            except Exception as match_value:
                finish()
                raise match_value
            
            if match_value_1 is not None:
                curr = match_value_1
                return True
            
            else: 
                finish()
                return False
            
        
        else: 
            return False
        
    
    return Enumerator_FromFunctions_1__ctor_58C54629(current, next_1, dispose)


def Enumerator_unfold(f: Callable[[_STATE], Option[Tuple[_T, _STATE]]], state: _STATE=None) -> IEnumerator[_T]:
    curr : Option[Tuple[_T, _STATE]] = None
    acc : _STATE = state
    def current(f: Callable[[_STATE], Option[Tuple[_T, _STATE]]]=f, state: _STATE=state) -> Any:
        if curr is not None:
            x : _T = curr[0]
            st : _STATE = curr[1]
            return x
        
        else: 
            return Enumerator_notStarted()
        
    
    def next_1(f: Callable[[_STATE], Option[Tuple[_T, _STATE]]]=f, state: _STATE=state) -> bool:
        nonlocal curr, acc
        curr = f(acc)
        if curr is not None:
            x_1 : _T = curr[0]
            st_1 : _STATE = curr[1]
            acc = st_1
            return True
        
        else: 
            return False
        
    
    def dispose(f: Callable[[_STATE], Option[Tuple[_T, _STATE]]]=f, state: _STATE=state) -> None:
        pass
    
    return Enumerator_FromFunctions_1__ctor_58C54629(current, next_1, dispose)


def index_not_found() -> Any:
    raise Exception(SR_keyNotFoundAlt)


def check_non_null(arg_name: str, arg: Any=None) -> None:
    if arg is None:
        Operators_NullArg(arg_name)
    


def mk_seq(f: Callable[[], IEnumerator[_T]]) -> IEnumerable[_T]:
    return Enumerator_Seq__ctor_673A07F2(f)


def of_seq(xs: IEnumerable[_T]) -> IEnumerator[_T]:
    check_non_null("source", xs)
    return get_enumerator(xs)


def delay(generator: Callable[[], IEnumerable[_T]]) -> IEnumerable[_T]:
    def arrow_150(generator: Callable[[], IEnumerable[_T]]=generator) -> IEnumerator[Any]:
        return get_enumerator(generator())
    
    return mk_seq(arrow_150)


def concat(sources: IEnumerable[Any]) -> IEnumerable[Any]:
    def arrow_151(sources: IEnumerable[__A]=sources) -> IEnumerator[Any]:
        return Enumerator_concat(sources)
    
    return mk_seq(arrow_151)


def unfold(generator: Callable[[_STATE], Option[Tuple[_T, _STATE]]], state: _STATE=None) -> IEnumerable[_T]:
    def arrow_152(generator: Callable[[_STATE], Option[Tuple[_T, _STATE]]]=generator, state: _STATE=state) -> IEnumerator[Any]:
        return Enumerator_unfold(generator, state)
    
    return mk_seq(arrow_152)


def empty() -> IEnumerable[Any]:
    def arrow_153(_unit: Any=None) -> IEnumerable[Any]:
        return []
    
    return delay(arrow_153)


def singleton(x: _T=None) -> IEnumerable[_T]:
    def arrow_154(x: _T=x) -> IEnumerable[Any]:
        return singleton_1(x, None)
    
    return delay(arrow_154)


def of_array(arr: List[_T]) -> IEnumerable[_T]:
    return arr


def to_array(xs: IEnumerable[_T]) -> List[_T]:
    if isinstance(xs, FSharpList):
        return to_array_1(xs)
    
    else: 
        return list(xs)
    


def of_list(xs: FSharpList[_T]) -> IEnumerable[_T]:
    return xs


def to_list(xs: IEnumerable[_T]) -> IEnumerable[_T]:
    if is_array_like(xs):
        return of_array_1(xs)
    
    elif isinstance(xs, FSharpList):
        return xs
    
    else: 
        return of_seq_1(xs)
    


def generate(create: Callable[[], __A], compute: Callable[[__A], Option[__B]], dispose: Callable[[__A], None]) -> IEnumerable[__B]:
    def arrow_155(create: Callable[[], __A]=create, compute: Callable[[__A], Option[__B]]=compute, dispose: Callable[[__A], None]=dispose) -> IEnumerator[Any]:
        return Enumerator_generateWhileSome(create, compute, dispose)
    
    return mk_seq(arrow_155)


def generate_indexed(create: Callable[[], __A], compute: Callable[[int, __A], Option[__B]], dispose: Callable[[__A], None]) -> IEnumerable[__B]:
    def arrow_157(create: Callable[[], __A]=create, compute: Callable[[int, __A], Option[__B]]=compute, dispose: Callable[[__A], None]=dispose) -> IEnumerator[Any]:
        i : int = -1
        def arrow_156(x: Any=None) -> Option[Any]:
            nonlocal i
            i = (i + 1) or 0
            return compute(i, x)
        
        return Enumerator_generateWhileSome(create, arrow_156, dispose)
    
    return mk_seq(arrow_157)


def append(xs: IEnumerable[_T], ys: IEnumerable[_T]) -> IEnumerable[_T]:
    return concat([xs, ys])


def cast(xs: IEnumerable[Any]) -> IEnumerable[Any]:
    def arrow_158(xs: IEnumerable[Any]=xs) -> IEnumerator[Any]:
        check_non_null("source", xs)
        return Enumerator_cast(get_enumerator(xs))
    
    return mk_seq(arrow_158)


def choose(chooser: Callable[[_T], Option[_U]], xs: IEnumerable[_T]) -> IEnumerable[_U]:
    def arrow_159(chooser: Callable[[_T], Option[_U]]=chooser, xs: IEnumerable[_T]=xs) -> IEnumerator[Any]:
        return of_seq(xs)
    
    def arrow_160(e: IEnumerator[Any], chooser: Callable[[_T], Option[_U]]=chooser, xs: IEnumerable[_T]=xs) -> Option[Any]:
        curr : Option[_U] = None
        while e.System_Collections_IEnumerator_MoveNext() if (curr is None) else (False):
            curr = chooser(e.System_Collections_Generic_IEnumerator_00601_get_Current())
        return curr
    
    def arrow_161(e_1: IEnumerator[Any], chooser: Callable[[_T], Option[_U]]=chooser, xs: IEnumerable[_T]=xs) -> None:
        dispose_2(e_1)
    
    return generate(arrow_159, arrow_160, arrow_161)


def compare_with(comparer: Callable[[_T, _T], int], xs: IEnumerable[_T], ys: IEnumerable[_T]) -> int:
    with of_seq(xs) as e1:
        with of_seq(ys) as e2:
            c : int = 0
            b1 : bool = e1.System_Collections_IEnumerator_MoveNext()
            b2 : bool = e2.System_Collections_IEnumerator_MoveNext()
            while b2 if (b1 if (c == 0) else (False)) else (False):
                c = comparer(e1.System_Collections_Generic_IEnumerator_00601_get_Current(), e2.System_Collections_Generic_IEnumerator_00601_get_Current()) or 0
                if c == 0:
                    b1 = e1.System_Collections_IEnumerator_MoveNext()
                    b2 = e2.System_Collections_IEnumerator_MoveNext()
                
            if c != 0:
                return c
            
            elif b1:
                return 1
            
            elif b2:
                return -1
            
            else: 
                return 0
            


def contains(value: _T, xs: IEnumerable[_T], comparer: IEqualityComparer[Any]) -> bool:
    with of_seq(xs) as e:
        found : bool = False
        while e.System_Collections_IEnumerator_MoveNext() if (not found) else (False):
            found = comparer.Equals(value, e.System_Collections_Generic_IEnumerator_00601_get_Current())
        return found


def enumerate_from_functions(create: Callable[[], __A], move_next: Callable[[__A], bool], current: Callable[[__A], __B]) -> IEnumerable[__B]:
    def arrow_162(x: Any=None, create: Callable[[], __A]=create, move_next: Callable[[__A], bool]=move_next, current: Callable[[__A], __B]=current) -> Option[Any]:
        return some(current(x)) if (move_next(x)) else (None)
    
    def arrow_163(x_1: Any=None, create: Callable[[], __A]=create, move_next: Callable[[__A], bool]=move_next, current: Callable[[__A], __B]=current) -> None:
        match_value : Any = x_1
        if is_disposable(match_value):
            dispose_2(match_value)
        
    
    return generate(create, arrow_162, arrow_163)


def enumerate_then_finally(source: IEnumerable[_T], compensation: Callable[[], None]) -> IEnumerable[_T]:
    compensation_1 : Callable[[], None] = compensation
    def arrow_164(source: IEnumerable[_T]=source, compensation: Callable[[], None]=compensation) -> IEnumerator[Any]:
        try: 
            return Enumerator_enumerateThenFinally(compensation_1, of_seq(source))
        
        except Exception as match_value:
            compensation_1()
            raise match_value
        
    
    return mk_seq(arrow_164)


def enumerate_using(resource: _T, source: Callable[[_T], __A]) -> IEnumerable[Any]:
    def compensation(resource: _T=resource, source: Callable[[_T], __A]=source) -> None:
        if equals(resource, None):
            pass
        
        else: 
            copy_of_struct : _T = resource
            dispose_2(copy_of_struct)
        
    
    def arrow_166(resource: _T=resource, source: Callable[[_T], __A]=source) -> IEnumerator[Any]:
        try: 
            def arrow_165(xs: IEnumerable[_T]) -> IEnumerator[_T]:
                return of_seq(xs)
            
            return Enumerator_enumerateThenFinally(compensation, arrow_165(source(resource)))
        
        except Exception as match_value_1:
            compensation()
            raise match_value_1
        
    
    return mk_seq(arrow_166)


def enumerate_while(guard: Callable[[], bool], xs: IEnumerable[_T]) -> IEnumerable[_T]:
    def arrow_167(i: int, guard: Callable[[], bool]=guard, xs: IEnumerable[_T]=xs) -> Option[Tuple[IEnumerable[_T], int]]:
        return (xs, i + 1) if (guard()) else (None)
    
    return concat(unfold(arrow_167, 0))


def filter(f: Callable[[_T], bool], xs: IEnumerable[_T]) -> IEnumerable[_T]:
    def chooser(x: _T=None, f: Callable[[_T], bool]=f, xs: IEnumerable[_T]=xs) -> Option[_T]:
        if f(x):
            return some(x)
        
        else: 
            return None
        
    
    return choose(chooser, xs)


def exists(predicate: Callable[[_T], bool], xs: IEnumerable[_T]) -> bool:
    with of_seq(xs) as e:
        found : bool = False
        while e.System_Collections_IEnumerator_MoveNext() if (not found) else (False):
            found = predicate(e.System_Collections_Generic_IEnumerator_00601_get_Current())
        return found


def exists2(predicate: Callable[[_T1, _T2], bool], xs: IEnumerable[_T1], ys: IEnumerable[_T2]) -> bool:
    with of_seq(xs) as e1:
        with of_seq(ys) as e2:
            found : bool = False
            while e2.System_Collections_IEnumerator_MoveNext() if (e1.System_Collections_IEnumerator_MoveNext() if (not found) else (False)) else (False):
                found = predicate(e1.System_Collections_Generic_IEnumerator_00601_get_Current(), e2.System_Collections_Generic_IEnumerator_00601_get_Current())
            return found


def exactly_one(xs: IEnumerable[_T]) -> _T:
    with of_seq(xs) as e:
        if e.System_Collections_IEnumerator_MoveNext():
            v : _T = e.System_Collections_Generic_IEnumerator_00601_get_Current()
            if e.System_Collections_IEnumerator_MoveNext():
                raise Exception((SR_inputSequenceTooLong + "\\nParameter name: ") + "source")
            
            else: 
                return v
            
        
        else: 
            raise Exception((SR_inputSequenceEmpty + "\\nParameter name: ") + "source")
        


def try_exactly_one(xs: IEnumerable[_T]) -> Option[_T]:
    with of_seq(xs) as e:
        if e.System_Collections_IEnumerator_MoveNext():
            v : _T = e.System_Collections_Generic_IEnumerator_00601_get_Current()
            if e.System_Collections_IEnumerator_MoveNext():
                return None
            
            else: 
                return some(v)
            
        
        else: 
            return None
        


def try_find(predicate: Callable[[_T], bool], xs: IEnumerable[_T]) -> Option[_T]:
    with of_seq(xs) as e:
        res : Option[_T] = None
        while e.System_Collections_IEnumerator_MoveNext() if (res is None) else (False):
            c : _T = e.System_Collections_Generic_IEnumerator_00601_get_Current()
            if predicate(c):
                res = some(c)
            
        return res


def find(predicate: Callable[[_T], bool], xs: IEnumerable[_T]) -> _T:
    match_value : Option[_T] = try_find(predicate, xs)
    if match_value is None:
        return index_not_found()
    
    else: 
        return value_1(match_value)
    


def try_find_back(predicate: Callable[[_T], bool], xs: IEnumerable[_T]) -> Option[_T]:
    return try_find_back_1(predicate, to_array(xs))


def find_back(predicate: Callable[[_T], bool], xs: IEnumerable[_T]) -> _T:
    match_value : Option[_T] = try_find_back(predicate, xs)
    if match_value is None:
        return index_not_found()
    
    else: 
        return value_1(match_value)
    


def try_find_index(predicate: Callable[[_T], bool], xs: IEnumerable[_T]) -> Option[int]:
    with of_seq(xs) as e:
        def loop(i_mut: int, predicate: Callable[[_T], bool]=predicate, xs: IEnumerable[_T]=xs) -> Option[int]:
            while True:
                (i,) = (i_mut,)
                if e.System_Collections_IEnumerator_MoveNext():
                    if predicate(e.System_Collections_Generic_IEnumerator_00601_get_Current()):
                        return i
                    
                    else: 
                        i_mut = i + 1
                        continue
                    
                
                else: 
                    return None
                
                break
        
        loop : Callable[[int], Option[int]] = loop
        return loop(0)


def find_index(predicate: Callable[[_T], bool], xs: IEnumerable[_T]) -> int:
    match_value : Option[int] = try_find_index(predicate, xs)
    if match_value is None:
        return index_not_found()
    
    else: 
        return match_value
    


def try_find_index_back(predicate: Callable[[_T], bool], xs: IEnumerable[_T]) -> Option[int]:
    return try_find_index_back_1(predicate, to_array(xs))


def find_index_back(predicate: Callable[[_T], bool], xs: IEnumerable[_T]) -> int:
    match_value : Option[int] = try_find_index_back(predicate, xs)
    if match_value is None:
        return index_not_found()
    
    else: 
        return match_value
    


def fold(folder: Callable[[_STATE, _T], _STATE], state: _STATE, xs: IEnumerable[_T]) -> _STATE:
    with of_seq(xs) as e:
        acc : _STATE = state
        while e.System_Collections_IEnumerator_MoveNext():
            acc = folder(acc, e.System_Collections_Generic_IEnumerator_00601_get_Current())
        return acc


def fold_back(folder: Callable[[_T, __A], __A], xs: IEnumerable[_T], state: __A=None) -> __A:
    return fold_back_1(folder, to_array(xs), state)


def fold2(folder: Callable[[_STATE, _T1, _T2], _STATE], state: _STATE, xs: IEnumerable[_T1], ys: IEnumerable[_T2]) -> _STATE:
    with of_seq(xs) as e1:
        with of_seq(ys) as e2:
            acc : _STATE = state
            while e2.System_Collections_IEnumerator_MoveNext() if (e1.System_Collections_IEnumerator_MoveNext()) else (False):
                acc = folder(acc, e1.System_Collections_Generic_IEnumerator_00601_get_Current(), e2.System_Collections_Generic_IEnumerator_00601_get_Current())
            return acc


def fold_back2(folder: Callable[[_T1, _T2, _STATE], _STATE], xs: IEnumerable[_T1], ys: IEnumerable[_T2], state: _STATE=None) -> _STATE:
    return fold_back2_1(folder, to_array(xs), to_array(ys), state)


def for_all(predicate: Callable[[__A], bool], xs: IEnumerable[__A]) -> bool:
    def arrow_168(x: Any=None, predicate: Callable[[__A], bool]=predicate, xs: IEnumerable[__A]=xs) -> bool:
        return not predicate(x)
    
    return not exists(arrow_168, xs)


def for_all2(predicate: Callable[[__A, __B], bool], xs: IEnumerable[__A], ys: IEnumerable[__B]) -> bool:
    def arrow_169(x: Any, y: Any=None, predicate: Callable[[__A, __B], bool]=predicate, xs: IEnumerable[__A]=xs, ys: IEnumerable[__B]=ys) -> bool:
        return not predicate(x, y)
    
    return not exists2(arrow_169, xs, ys)


def try_head(xs: IEnumerable[_T]) -> Option[_T]:
    if is_array_like(xs):
        return try_head_1(xs)
    
    elif isinstance(xs, FSharpList):
        return try_head_2(xs)
    
    else: 
        with of_seq(xs) as e:
            if e.System_Collections_IEnumerator_MoveNext():
                return some(e.System_Collections_Generic_IEnumerator_00601_get_Current())
            
            else: 
                return None
            
    


def head(xs: IEnumerable[_T]) -> _T:
    match_value : Option[_T] = try_head(xs)
    if match_value is None:
        raise Exception((SR_inputSequenceEmpty + "\\nParameter name: ") + "source")
    
    else: 
        return value_1(match_value)
    


def initialize(count: int, f: Callable[[int], __A]) -> IEnumerable[__A]:
    def arrow_170(i: int, count: int=count, f: Callable[[int], __A]=f) -> Option[Tuple[__A, int]]:
        return (f(i), i + 1) if (i < count) else (None)
    
    return unfold(arrow_170, 0)


def initialize_infinite(f: Callable[[int], __A]) -> IEnumerable[__A]:
    return initialize(2147483647, f)


def is_empty(xs: IEnumerable[Any]) -> bool:
    if is_array_like(xs):
        return len(xs) == 0
    
    elif isinstance(xs, FSharpList):
        return is_empty_1(xs)
    
    else: 
        with of_seq(xs) as e:
            return not e.System_Collections_IEnumerator_MoveNext()
    


def try_item(index: int, xs: IEnumerable[_T]) -> Option[_T]:
    if is_array_like(xs):
        return try_item_1(index, xs)
    
    elif isinstance(xs, FSharpList):
        return try_item_2(index, xs)
    
    else: 
        with of_seq(xs) as e:
            def loop(index_1_mut: int, index: int=index, xs: IEnumerable[_T]=xs) -> Option[Any]:
                while True:
                    (index_1,) = (index_1_mut,)
                    if not e.System_Collections_IEnumerator_MoveNext():
                        return None
                    
                    elif index_1 == 0:
                        return some(e.System_Collections_Generic_IEnumerator_00601_get_Current())
                    
                    else: 
                        index_1_mut = index_1 - 1
                        continue
                    
                    break
            
            loop : Callable[[int], Option[_T]] = loop
            return loop(index)
    


def item(index: int, xs: IEnumerable[_T]) -> _T:
    match_value : Option[_T] = try_item(index, xs)
    if match_value is None:
        raise Exception((SR_notEnoughElements + "\\nParameter name: ") + "index")
    
    else: 
        return value_1(match_value)
    


def iterate(action: Callable[[__A], None], xs: IEnumerable[__A]) -> None:
    def arrow_171(unit_var0: None, x: Any=None, action: Callable[[__A], None]=action, xs: IEnumerable[__A]=xs) -> None:
        action(x)
    
    fold(arrow_171, None, xs)


def iterate2(action: Callable[[__A, __B], None], xs: IEnumerable[__A], ys: IEnumerable[__B]) -> None:
    def arrow_172(unit_var0: None, x: Any, y: Any=None, action: Callable[[__A, __B], None]=action, xs: IEnumerable[__A]=xs, ys: IEnumerable[__B]=ys) -> None:
        action(x, y)
    
    fold2(arrow_172, None, xs, ys)


def iterate_indexed(action: Callable[[int, __A], None], xs: IEnumerable[__A]) -> None:
    def arrow_173(i: int, x: Any=None, action: Callable[[int, __A], None]=action, xs: IEnumerable[__A]=xs) -> int:
        action(i, x)
        return i + 1
    
    ignore(fold(arrow_173, 0, xs))


def iterate_indexed2(action: Callable[[int, __A, __B], None], xs: IEnumerable[__A], ys: IEnumerable[__B]) -> None:
    def arrow_174(i: int, x: Any, y: Any=None, action: Callable[[int, __A, __B], None]=action, xs: IEnumerable[__A]=xs, ys: IEnumerable[__B]=ys) -> int:
        action(i, x, y)
        return i + 1
    
    ignore(fold2(arrow_174, 0, xs, ys))


def try_last(xs: IEnumerable[_T]) -> Option[_T]:
    with of_seq(xs) as e:
        def loop(acc_mut: _T=None, xs: IEnumerable[_T]=xs) -> _T:
            while True:
                (acc,) = (acc_mut,)
                if not e.System_Collections_IEnumerator_MoveNext():
                    return acc
                
                else: 
                    acc_mut = e.System_Collections_Generic_IEnumerator_00601_get_Current()
                    continue
                
                break
        
        loop : Callable[[_T], _T] = loop
        if e.System_Collections_IEnumerator_MoveNext():
            return some(loop(e.System_Collections_Generic_IEnumerator_00601_get_Current()))
        
        else: 
            return None
        


def last(xs: IEnumerable[_T]) -> _T:
    match_value : Option[_T] = try_last(xs)
    if match_value is None:
        raise Exception((SR_notEnoughElements + "\\nParameter name: ") + "source")
    
    else: 
        return value_1(match_value)
    


def length(xs: IEnumerable[Any]) -> int:
    if is_array_like(xs):
        return len(xs)
    
    elif isinstance(xs, FSharpList):
        return length_1(xs)
    
    else: 
        with of_seq(xs) as e:
            count : int = 0
            while e.System_Collections_IEnumerator_MoveNext():
                count = (count + 1) or 0
            return count
    


def map(mapping: Callable[[_T], _U], xs: IEnumerable[_T]) -> IEnumerable[_U]:
    def arrow_175(mapping: Callable[[_T], _U]=mapping, xs: IEnumerable[_T]=xs) -> IEnumerator[Any]:
        return of_seq(xs)
    
    def arrow_176(e: IEnumerator[Any], mapping: Callable[[_T], _U]=mapping, xs: IEnumerable[_T]=xs) -> Option[Any]:
        return some(mapping(e.System_Collections_Generic_IEnumerator_00601_get_Current())) if (e.System_Collections_IEnumerator_MoveNext()) else (None)
    
    def arrow_177(e_1: IEnumerator[Any], mapping: Callable[[_T], _U]=mapping, xs: IEnumerable[_T]=xs) -> None:
        dispose_2(e_1)
    
    return generate(arrow_175, arrow_176, arrow_177)


def map_indexed(mapping: Callable[[int, _T], _U], xs: IEnumerable[_T]) -> IEnumerable[_U]:
    def arrow_178(mapping: Callable[[int, _T], _U]=mapping, xs: IEnumerable[_T]=xs) -> IEnumerator[Any]:
        return of_seq(xs)
    
    def arrow_179(i: int, e: IEnumerator[Any], mapping: Callable[[int, _T], _U]=mapping, xs: IEnumerable[_T]=xs) -> Option[Any]:
        return some(mapping(i, e.System_Collections_Generic_IEnumerator_00601_get_Current())) if (e.System_Collections_IEnumerator_MoveNext()) else (None)
    
    def arrow_180(e_1: IEnumerator[Any], mapping: Callable[[int, _T], _U]=mapping, xs: IEnumerable[_T]=xs) -> None:
        dispose_2(e_1)
    
    return generate_indexed(arrow_178, arrow_179, arrow_180)


def indexed(xs: IEnumerable[_T]) -> IEnumerable[Tuple[int, _T]]:
    def mapping(i: int, x: _T=None, xs: IEnumerable[_T]=xs) -> Tuple[int, _T]:
        return (i, x)
    
    return map_indexed(mapping, xs)


def map2(mapping: Callable[[_T1, _T2], _U], xs: IEnumerable[_T1], ys: IEnumerable[_T2]) -> IEnumerable[_U]:
    def arrow_181(mapping: Callable[[_T1, _T2], _U]=mapping, xs: IEnumerable[_T1]=xs, ys: IEnumerable[_T2]=ys) -> Tuple[IEnumerator[_T1], IEnumerator[_T2]]:
        return (of_seq(xs), of_seq(ys))
    
    def arrow_182(tupled_arg: Tuple[IEnumerator[_T1], IEnumerator[_T2]], mapping: Callable[[_T1, _T2], _U]=mapping, xs: IEnumerable[_T1]=xs, ys: IEnumerable[_T2]=ys) -> Option[Any]:
        e1 : IEnumerator[_T1] = tupled_arg[0]
        e2 : IEnumerator[_T2] = tupled_arg[1]
        return some(mapping(e1.System_Collections_Generic_IEnumerator_00601_get_Current(), e2.System_Collections_Generic_IEnumerator_00601_get_Current())) if (e2.System_Collections_IEnumerator_MoveNext() if (e1.System_Collections_IEnumerator_MoveNext()) else (False)) else (None)
    
    def arrow_183(tupled_arg_1: Tuple[IEnumerator[_T1], IEnumerator[_T2]], mapping: Callable[[_T1, _T2], _U]=mapping, xs: IEnumerable[_T1]=xs, ys: IEnumerable[_T2]=ys) -> None:
        try: 
            dispose_2(tupled_arg_1[0])
        
        finally: 
            dispose_2(tupled_arg_1[1])
        
    
    return generate(arrow_181, arrow_182, arrow_183)


def map_indexed2(mapping: Callable[[int, _T1, _T2], _U], xs: IEnumerable[_T1], ys: IEnumerable[_T2]) -> IEnumerable[_U]:
    def arrow_184(mapping: Callable[[int, _T1, _T2], _U]=mapping, xs: IEnumerable[_T1]=xs, ys: IEnumerable[_T2]=ys) -> Tuple[IEnumerator[_T1], IEnumerator[_T2]]:
        return (of_seq(xs), of_seq(ys))
    
    def arrow_185(i: int, tupled_arg: Tuple[IEnumerator[_T1], IEnumerator[_T2]], mapping: Callable[[int, _T1, _T2], _U]=mapping, xs: IEnumerable[_T1]=xs, ys: IEnumerable[_T2]=ys) -> Option[Any]:
        e1 : IEnumerator[_T1] = tupled_arg[0]
        e2 : IEnumerator[_T2] = tupled_arg[1]
        return some(mapping(i, e1.System_Collections_Generic_IEnumerator_00601_get_Current(), e2.System_Collections_Generic_IEnumerator_00601_get_Current())) if (e2.System_Collections_IEnumerator_MoveNext() if (e1.System_Collections_IEnumerator_MoveNext()) else (False)) else (None)
    
    def arrow_186(tupled_arg_1: Tuple[IEnumerator[_T1], IEnumerator[_T2]], mapping: Callable[[int, _T1, _T2], _U]=mapping, xs: IEnumerable[_T1]=xs, ys: IEnumerable[_T2]=ys) -> None:
        try: 
            dispose_2(tupled_arg_1[0])
        
        finally: 
            dispose_2(tupled_arg_1[1])
        
    
    return generate_indexed(arrow_184, arrow_185, arrow_186)


def map3(mapping: Callable[[_T1, _T2, _T3], _U], xs: IEnumerable[_T1], ys: IEnumerable[_T2], zs: IEnumerable[_T3]) -> IEnumerable[_U]:
    def arrow_187(mapping: Callable[[_T1, _T2, _T3], _U]=mapping, xs: IEnumerable[_T1]=xs, ys: IEnumerable[_T2]=ys, zs: IEnumerable[_T3]=zs) -> Tuple[IEnumerator[_T1], IEnumerator[_T2], IEnumerator[_T3]]:
        return (of_seq(xs), of_seq(ys), of_seq(zs))
    
    def arrow_188(tupled_arg: Tuple[IEnumerator[_T1], IEnumerator[_T2], IEnumerator[_T3]], mapping: Callable[[_T1, _T2, _T3], _U]=mapping, xs: IEnumerable[_T1]=xs, ys: IEnumerable[_T2]=ys, zs: IEnumerable[_T3]=zs) -> Option[Any]:
        e1 : IEnumerator[_T1] = tupled_arg[0]
        e2 : IEnumerator[_T2] = tupled_arg[1]
        e3 : IEnumerator[_T3] = tupled_arg[2]
        return some(mapping(e1.System_Collections_Generic_IEnumerator_00601_get_Current(), e2.System_Collections_Generic_IEnumerator_00601_get_Current(), e3.System_Collections_Generic_IEnumerator_00601_get_Current())) if (e3.System_Collections_IEnumerator_MoveNext() if (e2.System_Collections_IEnumerator_MoveNext() if (e1.System_Collections_IEnumerator_MoveNext()) else (False)) else (False)) else (None)
    
    def arrow_189(tupled_arg_1: Tuple[IEnumerator[_T1], IEnumerator[_T2], IEnumerator[_T3]], mapping: Callable[[_T1, _T2, _T3], _U]=mapping, xs: IEnumerable[_T1]=xs, ys: IEnumerable[_T2]=ys, zs: IEnumerable[_T3]=zs) -> None:
        try: 
            dispose_2(tupled_arg_1[0])
        
        finally: 
            try: 
                dispose_2(tupled_arg_1[1])
            
            finally: 
                dispose_2(tupled_arg_1[2])
            
        
    
    return generate(arrow_187, arrow_188, arrow_189)


def read_only(xs: IEnumerable[_T]) -> IEnumerable[_T]:
    check_non_null("source", xs)
    def arrow_190(x: _T=None, xs: IEnumerable[_T]=xs) -> _T:
        return x
    
    return map(arrow_190, xs)


def expr_191(gen0: TypeInfo) -> TypeInfo:
    return class_type("SeqModule.CachedSeq`1", [gen0], CachedSeq_1)


class CachedSeq_1(IDisposable, Generic[_T]):
    def __init__(self, cleanup: Callable[[], None], res: IEnumerable[Any]) -> None:
        self.cleanup = cleanup
        self.res = res
    
    def Dispose(self) -> None:
        _ : CachedSeq_1[_T] = self
        _.cleanup()
    
    def GetEnumerator(self) -> IEnumerator[Any]:
        _ : CachedSeq_1[_T] = self
        return get_enumerator(_.res)
    
    def __iter__(self) -> IEnumerator[Any]:
        return to_iterator(self.GetEnumerator())
    
    def System_Collections_IEnumerable_GetEnumerator(self) -> IEnumerator[Any]:
        _ : CachedSeq_1[_T] = self
        return get_enumerator(_.res)
    

CachedSeq_1_reflection = expr_191

def CachedSeq_1__ctor_Z7A8347D4(cleanup: Callable[[], None], res: IEnumerable[Any]) -> CachedSeq_1[_T]:
    return CachedSeq_1(cleanup, res)


def CachedSeq_1__Clear(_: CachedSeq_1[Any]) -> None:
    _.cleanup()


def cache(source: IEnumerable[_T]) -> IEnumerable[_T]:
    check_non_null("source", source)
    prefix : List[_T] = []
    enumerator_r : Option[Option[IEnumerator[_T]]] = None
    def cleanup(source: IEnumerable[_T]=source) -> None:
        def arrow_192(_unit: Any=None) -> None:
            nonlocal enumerator_r
            clear(prefix)
            (pattern_matching_result, e) = (None, None)
            if enumerator_r is not None:
                if value_1(enumerator_r) is not None:
                    pattern_matching_result = 0
                    e = value_1(enumerator_r)
                
                else: 
                    pattern_matching_result = 1
                
            
            else: 
                pattern_matching_result = 1
            
            if pattern_matching_result == 0:
                dispose_2(e)
            
            enumerator_r = None
        
        Operators_Lock(prefix, arrow_192)
    
    def arrow_194(i_1: int, source: IEnumerable[_T]=source) -> Option[Tuple[_T, int]]:
        def arrow_193(_unit: Any=None) -> Option[Tuple[_T, int]]:
            nonlocal enumerator_r
            if i_1 < len(prefix):
                return (prefix[i_1], i_1 + 1)
            
            else: 
                if i_1 >= len(prefix):
                    opt_enumerator_2 : Option[IEnumerator[_T]]
                    if enumerator_r is not None:
                        opt_enumerator_2 = value_1(enumerator_r)
                    
                    else: 
                        opt_enumerator : Option[IEnumerator[_T]] = get_enumerator(source)
                        enumerator_r = some(opt_enumerator)
                        opt_enumerator_2 = opt_enumerator
                    
                    if opt_enumerator_2 is None:
                        pass
                    
                    else: 
                        enumerator : IEnumerator[_T] = opt_enumerator_2
                        if enumerator.System_Collections_IEnumerator_MoveNext():
                            (prefix.append(enumerator.System_Collections_Generic_IEnumerator_00601_get_Current()))
                        
                        else: 
                            dispose_2(enumerator)
                            enumerator_r = some(None)
                        
                    
                
                return (prefix[i_1], i_1 + 1) if (i_1 < len(prefix)) else (None)
            
        
        return Operators_Lock(prefix, arrow_193)
    
    return CachedSeq_1__ctor_Z7A8347D4(cleanup, unfold(arrow_194, 0))


def all_pairs(xs: IEnumerable[_T1], ys: IEnumerable[_T2]) -> IEnumerable[Tuple[_T1, _T2]]:
    ys_cache : IEnumerable[_T2] = cache(ys)
    def arrow_195(xs: IEnumerable[_T1]=xs, ys: IEnumerable[_T2]=ys) -> IEnumerable[Tuple[_T1, _T2]]:
        def mapping_1(x: __A=None) -> IEnumerable[Tuple[__A, _T2]]:
            def mapping(y: _T2=None, x: __A=x) -> Tuple[__A, _T2]:
                return (x, y)
            
            return map(mapping, ys_cache)
        
        return concat(map(mapping_1, xs))
    
    return delay(arrow_195)


def map_fold(mapping: Callable[[_STATE, _T], Tuple[_RESULT, _STATE]], state: _STATE, xs: IEnumerable[_T]) -> Tuple[IEnumerable[_RESULT], _STATE]:
    pattern_input : Tuple[List[_RESULT], _STATE] = map_fold_1(mapping, state, to_array(xs), None)
    return (read_only(pattern_input[0]), pattern_input[1])


def map_fold_back(mapping: Callable[[_T, _STATE], Tuple[_RESULT, _STATE]], xs: IEnumerable[_T], state: _STATE=None) -> Tuple[IEnumerable[_RESULT], _STATE]:
    pattern_input : Tuple[List[_RESULT], _STATE] = map_fold_back_1(mapping, to_array(xs), state, None)
    return (read_only(pattern_input[0]), pattern_input[1])


def try_pick(chooser: Callable[[_T], Option[__A]], xs: IEnumerable[_T]) -> Option[__A]:
    with of_seq(xs) as e:
        res : Option[__A] = None
        while e.System_Collections_IEnumerator_MoveNext() if (res is None) else (False):
            res = chooser(e.System_Collections_Generic_IEnumerator_00601_get_Current())
        return res


def pick(chooser: Callable[[_T], Option[__A]], xs: IEnumerable[_T]) -> __A:
    match_value : Option[__A] = try_pick(chooser, xs)
    if match_value is None:
        return index_not_found()
    
    else: 
        return value_1(match_value)
    


def reduce(folder: Callable[[_T, _T], _T], xs: IEnumerable[_T]) -> _T:
    with of_seq(xs) as e:
        def loop(acc_mut: _T=None, folder: Callable[[_T, _T], _T]=folder, xs: IEnumerable[_T]=xs) -> _T:
            while True:
                (acc,) = (acc_mut,)
                if e.System_Collections_IEnumerator_MoveNext():
                    acc_mut = folder(acc, e.System_Collections_Generic_IEnumerator_00601_get_Current())
                    continue
                
                else: 
                    return acc
                
                break
        
        loop : Callable[[_T], _T] = loop
        if e.System_Collections_IEnumerator_MoveNext():
            return loop(e.System_Collections_Generic_IEnumerator_00601_get_Current())
        
        else: 
            raise Exception(SR_inputSequenceEmpty)
        


def reduce_back(folder: Callable[[_T, _T], _T], xs: IEnumerable[_T]) -> _T:
    arr : List[_T] = to_array(xs)
    if len(arr) > 0:
        return reduce_back_1(folder, arr)
    
    else: 
        raise Exception(SR_inputSequenceEmpty)
    


def replicate(n: int, x: __A=None) -> IEnumerable[__A]:
    def arrow_196(_arg1: int, n: int=n, x: __A=x) -> Any:
        return x
    
    return initialize(n, arrow_196)


def reverse(xs: IEnumerable[_T]) -> IEnumerable[_T]:
    def arrow_197(xs: IEnumerable[_T]=xs) -> IEnumerable[Any]:
        return of_array(reverse_1(to_array(xs)))
    
    return delay(arrow_197)


def scan(folder: Callable[[_STATE, _T], _STATE], state: _STATE, xs: IEnumerable[_T]) -> IEnumerable[_STATE]:
    def arrow_198(folder: Callable[[_STATE, _T], _STATE]=folder, state: _STATE=state, xs: IEnumerable[_T]=xs) -> IEnumerable[Any]:
        acc : _STATE = state
        def mapping(x: Any=None) -> Any:
            nonlocal acc
            acc = folder(acc, x)
            return acc
        
        return concat([singleton(state), map(mapping, xs)])
    
    return delay(arrow_198)


def scan_back(folder: Callable[[_T, _STATE], _STATE], xs: IEnumerable[_T], state: _STATE=None) -> IEnumerable[_STATE]:
    def arrow_199(folder: Callable[[_T, _STATE], _STATE]=folder, xs: IEnumerable[_T]=xs, state: _STATE=state) -> IEnumerable[Any]:
        return of_array(scan_back_1(folder, to_array(xs), state, None))
    
    return delay(arrow_199)


def skip(count: int, source: IEnumerable[_T]) -> IEnumerable[_T]:
    def arrow_200(count: int=count, source: IEnumerable[_T]=source) -> IEnumerator[Any]:
        e : IEnumerator[_T] = of_seq(source)
        try: 
            for _ in range(1, count + 1, 1):
                if not e.System_Collections_IEnumerator_MoveNext():
                    raise Exception((SR_notEnoughElements + "\\nParameter name: ") + "source")
                
            def compensation(_unit: Any=None) -> None:
                pass
            
            return Enumerator_enumerateThenFinally(compensation, e)
        
        except Exception as match_value:
            dispose_2(e)
            raise match_value
        
    
    return mk_seq(arrow_200)


def skip_while(predicate: Callable[[_T], bool], xs: IEnumerable[_T]) -> IEnumerable[_T]:
    def arrow_201(predicate: Callable[[_T], bool]=predicate, xs: IEnumerable[_T]=xs) -> IEnumerable[Any]:
        skipped : bool = True
        def f(x: Any=None) -> bool:
            nonlocal skipped
            if skipped:
                skipped = predicate(x)
            
            return not skipped
        
        return filter(f, xs)
    
    return delay(arrow_201)


def tail(xs: IEnumerable[_T]) -> IEnumerable[_T]:
    return skip(1, xs)


def take(count: int, xs: IEnumerable[_T]) -> IEnumerable[_T]:
    def arrow_202(count: int=count, xs: IEnumerable[_T]=xs) -> IEnumerator[Any]:
        return of_seq(xs)
    
    def arrow_203(i: int, e: IEnumerator[_T], count: int=count, xs: IEnumerable[_T]=xs) -> Option[_T]:
        if i < count:
            if e.System_Collections_IEnumerator_MoveNext():
                return some(e.System_Collections_Generic_IEnumerator_00601_get_Current())
            
            else: 
                raise Exception((SR_notEnoughElements + "\\nParameter name: ") + "source")
            
        
        else: 
            return None
        
    
    def arrow_204(e_1: IEnumerator[Any], count: int=count, xs: IEnumerable[_T]=xs) -> None:
        dispose_2(e_1)
    
    return generate_indexed(arrow_202, arrow_203, arrow_204)


def take_while(predicate: Callable[[_T], bool], xs: IEnumerable[_T]) -> IEnumerable[_T]:
    def arrow_205(predicate: Callable[[_T], bool]=predicate, xs: IEnumerable[_T]=xs) -> IEnumerator[Any]:
        return of_seq(xs)
    
    def arrow_206(e: IEnumerator[_T], predicate: Callable[[_T], bool]=predicate, xs: IEnumerable[_T]=xs) -> Option[_T]:
        return some(e.System_Collections_Generic_IEnumerator_00601_get_Current()) if (predicate(e.System_Collections_Generic_IEnumerator_00601_get_Current()) if (e.System_Collections_IEnumerator_MoveNext()) else (False)) else (None)
    
    def arrow_207(e_1: IEnumerator[Any], predicate: Callable[[_T], bool]=predicate, xs: IEnumerable[_T]=xs) -> None:
        dispose_2(e_1)
    
    return generate(arrow_205, arrow_206, arrow_207)


def truncate(count: int, xs: IEnumerable[_T]) -> IEnumerable[_T]:
    def arrow_208(count: int=count, xs: IEnumerable[_T]=xs) -> IEnumerator[Any]:
        return of_seq(xs)
    
    def arrow_209(i: int, e: IEnumerator[_T], count: int=count, xs: IEnumerable[_T]=xs) -> Option[_T]:
        return some(e.System_Collections_Generic_IEnumerator_00601_get_Current()) if (e.System_Collections_IEnumerator_MoveNext() if (i < count) else (False)) else (None)
    
    def arrow_210(e_1: IEnumerator[Any], count: int=count, xs: IEnumerable[_T]=xs) -> None:
        dispose_2(e_1)
    
    return generate_indexed(arrow_208, arrow_209, arrow_210)


def zip(xs: IEnumerable[_T1], ys: IEnumerable[_T2]) -> IEnumerable[Tuple[_T1, _T2]]:
    def arrow_211(x: _T1, y: _T2=None, xs: IEnumerable[_T1]=xs, ys: IEnumerable[_T2]=ys) -> Tuple[_T1, _T2]:
        return (x, y)
    
    return map2(arrow_211, xs, ys)


def zip3(xs: IEnumerable[_T1], ys: IEnumerable[_T2], zs: IEnumerable[_T3]) -> IEnumerable[Tuple[_T1, _T2, _T3]]:
    def arrow_212(x: _T1, y: _T2, z: _T3=None, xs: IEnumerable[_T1]=xs, ys: IEnumerable[_T2]=ys, zs: IEnumerable[_T3]=zs) -> Tuple[_T1, _T2, _T3]:
        return (x, y, z)
    
    return map3(arrow_212, xs, ys, zs)


def collect(mapping: Callable[[_T], IEnumerable[_U]], xs: IEnumerable[_T]) -> IEnumerable[_U]:
    def arrow_213(mapping: Callable[[_T], IEnumerable[_U]]=mapping, xs: IEnumerable[_T]=xs) -> IEnumerable[Any]:
        return concat(map(mapping, xs))
    
    return delay(arrow_213)


def where(predicate: Callable[[_T], bool], xs: IEnumerable[_T]) -> IEnumerable[_T]:
    return filter(predicate, xs)


def pairwise(xs: IEnumerable[_T]) -> IEnumerable[Tuple[_T, _T]]:
    def arrow_214(xs: IEnumerable[_T]=xs) -> IEnumerable[Tuple[_T, _T]]:
        return of_array(pairwise_1(to_array(xs)))
    
    return delay(arrow_214)


def split_into(chunks: int, xs: IEnumerable[_T]) -> IEnumerable[IEnumerable[_T]]:
    def arrow_215(chunks: int=chunks, xs: IEnumerable[_T]=xs) -> IEnumerable[IEnumerable[Any]]:
        def mapping(arr: List[_T]) -> IEnumerable[_T]:
            return of_array(arr)
        
        return of_array(map_1(mapping, split_into_1(chunks, to_array(xs)), None))
    
    return delay(arrow_215)


def windowed(window_size: int, xs: IEnumerable[_T]) -> IEnumerable[IEnumerable[_T]]:
    def arrow_216(window_size: int=window_size, xs: IEnumerable[_T]=xs) -> IEnumerable[IEnumerable[Any]]:
        def mapping(arr: List[_T]) -> IEnumerable[_T]:
            return of_array(arr)
        
        return of_array(map_1(mapping, windowed_1(window_size, to_array(xs)), None))
    
    return delay(arrow_216)


def transpose(xss: IEnumerable[Any]) -> IEnumerable[IEnumerable[Any]]:
    def arrow_217(xss: IEnumerable[__A]=xss) -> IEnumerable[IEnumerable[Any]]:
        def mapping_1(arr: List[_T]) -> IEnumerable[_T]:
            return of_array(arr)
        
        def mapping(xs_1: Any=None) -> List[_T]:
            return to_array(xs_1)
        
        return of_array(map_1(mapping_1, transpose_1(map_1(mapping, to_array(xss), None), None), None))
    
    return delay(arrow_217)


def sort_with(comparer: Callable[[_T, _T], int], xs: IEnumerable[_T]) -> IEnumerable[_T]:
    def arrow_218(comparer: Callable[[_T, _T], int]=comparer, xs: IEnumerable[_T]=xs) -> IEnumerable[Any]:
        arr : List[_T] = to_array(xs)
        arr.sort()
        return of_array(arr)
    
    return delay(arrow_218)


def sort(xs: IEnumerable[_T], comparer: IComparer[_T]) -> IEnumerable[_T]:
    def arrow_219(x: _T, y: _T=None, xs: IEnumerable[_T]=xs, comparer: IComparer[_T]=comparer) -> int:
        return comparer.Compare(x, y)
    
    return sort_with(arrow_219, xs)


def sort_by(projection: Callable[[_T], _U], xs: IEnumerable[_T], comparer: IComparer[_U]) -> IEnumerable[_T]:
    def arrow_220(x: _T, y: _T=None, projection: Callable[[_T], _U]=projection, xs: IEnumerable[_T]=xs, comparer: IComparer[_U]=comparer) -> int:
        return comparer.Compare(projection(x), projection(y))
    
    return sort_with(arrow_220, xs)


def sort_descending(xs: IEnumerable[_T], comparer: IComparer[_T]) -> IEnumerable[_T]:
    def arrow_221(x: _T, y: _T=None, xs: IEnumerable[_T]=xs, comparer: IComparer[_T]=comparer) -> int:
        return comparer.Compare(x, y) * -1
    
    return sort_with(arrow_221, xs)


def sort_by_descending(projection: Callable[[_T], _U], xs: IEnumerable[_T], comparer: IComparer[_U]) -> IEnumerable[_T]:
    def arrow_222(x: _T, y: _T=None, projection: Callable[[_T], _U]=projection, xs: IEnumerable[_T]=xs, comparer: IComparer[_U]=comparer) -> int:
        return comparer.Compare(projection(x), projection(y)) * -1
    
    return sort_with(arrow_222, xs)


def sum(xs: IEnumerable[_T], adder: IGenericAdder_1[_T]) -> _T:
    def arrow_223(acc: _T, x: _T=None, xs: IEnumerable[_T]=xs, adder: IGenericAdder_1[_T]=adder) -> _T:
        return adder.Add(acc, x)
    
    return fold(arrow_223, adder.GetZero(), xs)


def sum_by(f: Callable[[_T], _U], xs: IEnumerable[_T], adder: IGenericAdder_1[_U]) -> _U:
    def arrow_224(acc: _U, x: Any=None, f: Callable[[_T], _U]=f, xs: IEnumerable[_T]=xs, adder: IGenericAdder_1[_U]=adder) -> _U:
        return adder.Add(acc, f(x))
    
    return fold(arrow_224, adder.GetZero(), xs)


def max_by(projection: Callable[[_T], _U], xs: IEnumerable[_T], comparer: IComparer[_U]) -> _T:
    def arrow_225(x: _T, y: _T=None, projection: Callable[[_T], _U]=projection, xs: IEnumerable[_T]=xs, comparer: IComparer[_U]=comparer) -> _T:
        return y if (comparer.Compare(projection(y), projection(x)) > 0) else (x)
    
    return reduce(arrow_225, xs)


def max(xs: IEnumerable[_T], comparer: IComparer[_T]) -> _T:
    def arrow_226(x: _T, y: _T=None, xs: IEnumerable[_T]=xs, comparer: IComparer[_T]=comparer) -> _T:
        return y if (comparer.Compare(y, x) > 0) else (x)
    
    return reduce(arrow_226, xs)


def min_by(projection: Callable[[_T], _U], xs: IEnumerable[_T], comparer: IComparer[_U]) -> _T:
    def arrow_227(x: _T, y: _T=None, projection: Callable[[_T], _U]=projection, xs: IEnumerable[_T]=xs, comparer: IComparer[_U]=comparer) -> _T:
        return x if (comparer.Compare(projection(y), projection(x)) > 0) else (y)
    
    return reduce(arrow_227, xs)


def min(xs: IEnumerable[_T], comparer: IComparer[_T]) -> _T:
    def arrow_228(x: _T, y: _T=None, xs: IEnumerable[_T]=xs, comparer: IComparer[_T]=comparer) -> _T:
        return x if (comparer.Compare(y, x) > 0) else (y)
    
    return reduce(arrow_228, xs)


def average(xs: IEnumerable[_T], averager: IGenericAverager_1[_T]) -> _T:
    count : int = 0
    def folder(acc: _T, x: _T=None, xs: IEnumerable[_T]=xs, averager: IGenericAverager_1[_T]=averager) -> _T:
        nonlocal count
        count = (count + 1) or 0
        return averager.Add(acc, x)
    
    total : _T = fold(folder, averager.GetZero(), xs)
    if count == 0:
        raise Exception((SR_inputSequenceEmpty + "\\nParameter name: ") + "source")
    
    else: 
        return averager.DivideByInt(total, count)
    


def average_by(f: Callable[[_T], _U], xs: IEnumerable[_T], averager: IGenericAverager_1[_U]) -> _U:
    count : int = 0
    def arrow_229(acc: _U, x: Any=None, f: Callable[[_T], _U]=f, xs: IEnumerable[_T]=xs, averager: IGenericAverager_1[_U]=averager) -> _U:
        nonlocal count
        count = (count + 1) or 0
        return averager.Add(acc, f(x))
    
    total : _U = fold(arrow_229, averager.GetZero(), xs)
    if count == 0:
        raise Exception((SR_inputSequenceEmpty + "\\nParameter name: ") + "source")
    
    else: 
        return averager.DivideByInt(total, count)
    


def permute(f: Callable[[int], int], xs: IEnumerable[_T]) -> IEnumerable[_T]:
    def arrow_230(f: Callable[[int], int]=f, xs: IEnumerable[_T]=xs) -> IEnumerable[Any]:
        return of_array(permute_1(f, to_array(xs)))
    
    return delay(arrow_230)


def chunk_by_size(chunk_size: int, xs: IEnumerable[_T]) -> IEnumerable[IEnumerable[_T]]:
    def arrow_231(chunk_size: int=chunk_size, xs: IEnumerable[_T]=xs) -> IEnumerable[IEnumerable[Any]]:
        def mapping(arr: List[_T]) -> IEnumerable[_T]:
            return of_array(arr)
        
        return of_array(map_1(mapping, chunk_by_size_1(chunk_size, to_array(xs)), None))
    
    return delay(arrow_231)


def insert_at(index: int, y: _T, xs: IEnumerable[_T]) -> IEnumerable[_T]:
    is_done : bool = False
    if index < 0:
        raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")
    
    def arrow_232(index: int=index, y: _T=y, xs: IEnumerable[_T]=xs) -> IEnumerator[Any]:
        return of_seq(xs)
    
    def arrow_233(i: int, e: IEnumerator[_T], index: int=index, y: _T=y, xs: IEnumerable[_T]=xs) -> Option[_T]:
        nonlocal is_done
        if e.System_Collections_IEnumerator_MoveNext() if (True if (is_done) else (i < index)) else (False):
            return some(e.System_Collections_Generic_IEnumerator_00601_get_Current())
        
        elif i == index:
            is_done = True
            return some(y)
        
        else: 
            if not is_done:
                raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")
            
            return None
        
    
    def arrow_234(e_1: IEnumerator[Any], index: int=index, y: _T=y, xs: IEnumerable[_T]=xs) -> None:
        dispose_2(e_1)
    
    return generate_indexed(arrow_232, arrow_233, arrow_234)


def insert_many_at(index: int, ys: IEnumerable[_T], xs: IEnumerable[_T]) -> IEnumerable[_T]:
    status : int = -1
    if index < 0:
        raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")
    
    def arrow_235(index: int=index, ys: IEnumerable[_T]=ys, xs: IEnumerable[_T]=xs) -> Tuple[IEnumerator[_T], IEnumerator[_T]]:
        return (of_seq(xs), of_seq(ys))
    
    def arrow_236(i: int, tupled_arg: Tuple[IEnumerator[_T], IEnumerator[_T]], index: int=index, ys: IEnumerable[_T]=ys, xs: IEnumerable[_T]=xs) -> Option[_T]:
        nonlocal status
        e1 : IEnumerator[_T] = tupled_arg[0]
        e2 : IEnumerator[_T] = tupled_arg[1]
        if i == index:
            status = 0
        
        inserted : Option[_T]
        if status == 0:
            if e2.System_Collections_IEnumerator_MoveNext():
                inserted = some(e2.System_Collections_Generic_IEnumerator_00601_get_Current())
            
            else: 
                status = 1
                inserted = None
            
        
        else: 
            inserted = None
        
        if inserted is None:
            if e1.System_Collections_IEnumerator_MoveNext():
                return some(e1.System_Collections_Generic_IEnumerator_00601_get_Current())
            
            else: 
                if status < 1:
                    raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")
                
                return None
            
        
        else: 
            return some(value_1(inserted))
        
    
    def arrow_237(tupled_arg_1: Tuple[IEnumerator[_T], IEnumerator[_T]], index: int=index, ys: IEnumerable[_T]=ys, xs: IEnumerable[_T]=xs) -> None:
        dispose_2(tupled_arg_1[0])
        dispose_2(tupled_arg_1[1])
    
    return generate_indexed(arrow_235, arrow_236, arrow_237)


def remove_at(index: int, xs: IEnumerable[_T]) -> IEnumerable[_T]:
    is_done : bool = False
    if index < 0:
        raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")
    
    def arrow_238(index: int=index, xs: IEnumerable[_T]=xs) -> IEnumerator[Any]:
        return of_seq(xs)
    
    def arrow_239(i: int, e: IEnumerator[_T], index: int=index, xs: IEnumerable[_T]=xs) -> Option[_T]:
        nonlocal is_done
        if e.System_Collections_IEnumerator_MoveNext() if (True if (is_done) else (i < index)) else (False):
            return some(e.System_Collections_Generic_IEnumerator_00601_get_Current())
        
        elif e.System_Collections_IEnumerator_MoveNext() if (i == index) else (False):
            is_done = True
            return some(e.System_Collections_Generic_IEnumerator_00601_get_Current()) if (e.System_Collections_IEnumerator_MoveNext()) else (None)
        
        else: 
            if not is_done:
                raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")
            
            return None
        
    
    def arrow_240(e_1: IEnumerator[Any], index: int=index, xs: IEnumerable[_T]=xs) -> None:
        dispose_2(e_1)
    
    return generate_indexed(arrow_238, arrow_239, arrow_240)


def remove_many_at(index: int, count: int, xs: IEnumerable[_T]) -> IEnumerable[_T]:
    if index < 0:
        raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")
    
    def arrow_241(index: int=index, count: int=count, xs: IEnumerable[_T]=xs) -> IEnumerator[Any]:
        return of_seq(xs)
    
    def arrow_242(i: int, e: IEnumerator[_T], index: int=index, count: int=count, xs: IEnumerable[_T]=xs) -> Option[_T]:
        if i < index:
            if e.System_Collections_IEnumerator_MoveNext():
                return some(e.System_Collections_Generic_IEnumerator_00601_get_Current())
            
            else: 
                raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")
            
        
        else: 
            if i == index:
                for _ in range(1, count + 1, 1):
                    if not e.System_Collections_IEnumerator_MoveNext():
                        raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "count")
                    
            
            return some(e.System_Collections_Generic_IEnumerator_00601_get_Current()) if (e.System_Collections_IEnumerator_MoveNext()) else (None)
        
    
    def arrow_243(e_1: IEnumerator[Any], index: int=index, count: int=count, xs: IEnumerable[_T]=xs) -> None:
        dispose_2(e_1)
    
    return generate_indexed(arrow_241, arrow_242, arrow_243)


def update_at(index: int, y: _T, xs: IEnumerable[_T]) -> IEnumerable[_T]:
    is_done : bool = False
    if index < 0:
        raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")
    
    def arrow_244(index: int=index, y: _T=y, xs: IEnumerable[_T]=xs) -> IEnumerator[Any]:
        return of_seq(xs)
    
    def arrow_245(i: int, e: IEnumerator[_T], index: int=index, y: _T=y, xs: IEnumerable[_T]=xs) -> Option[_T]:
        nonlocal is_done
        if e.System_Collections_IEnumerator_MoveNext() if (True if (is_done) else (i < index)) else (False):
            return some(e.System_Collections_Generic_IEnumerator_00601_get_Current())
        
        elif e.System_Collections_IEnumerator_MoveNext() if (i == index) else (False):
            is_done = True
            return some(y)
        
        else: 
            if not is_done:
                raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")
            
            return None
        
    
    def arrow_246(e_1: IEnumerator[Any], index: int=index, y: _T=y, xs: IEnumerable[_T]=xs) -> None:
        dispose_2(e_1)
    
    return generate_indexed(arrow_244, arrow_245, arrow_246)


