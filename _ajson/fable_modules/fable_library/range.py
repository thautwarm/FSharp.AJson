from typing import (TypeVar, Callable, Tuple, Any)
from .big_int import (from_zero, op_addition)
from .decimal import (from_parts, op_addition as op_addition_1)
from .long import (from_bits, op_addition as op_addition_2)
from .option import Option
from .seq import (delay, unfold)
from .util import (compare, IEnumerable)

_T = TypeVar("_T")

def make_range_step_function(step: _T, stop: _T, zero: _T, add: Callable[[_T, _T], _T]) -> Callable[[_T], Option[Tuple[_T, _T]]]:
    step_compared_with_zero : int = compare(step, zero) or 0
    if step_compared_with_zero == 0:
        raise Exception("The step of a range cannot be zero")
    
    step_greater_than_zero : bool = step_compared_with_zero > 0
    def arrow_134(x: _T=None, step: _T=step, stop: _T=stop, zero: _T=zero, add: Callable[[_T, _T], _T]=add) -> Option[Tuple[_T, _T]]:
        compared_with_last : int = compare(x, stop) or 0
        return (x, add(x, step)) if (True if (compared_with_last <= 0 if (step_greater_than_zero) else (False)) else (compared_with_last >= 0 if (not step_greater_than_zero) else (False))) else (None)
    
    return arrow_134


def integral_range_step(start: _T, step: _T, stop: _T, zero: _T, add: Callable[[_T, _T], _T]) -> IEnumerable[_T]:
    step_fn : Callable[[_T], Option[Tuple[_T, _T]]] = make_range_step_function(step, stop, zero, add)
    def arrow_135(start: _T=start, step: _T=step, stop: _T=stop, zero: _T=zero, add: Callable[[_T, _T], _T]=add) -> IEnumerable[Any]:
        return unfold(step_fn, start)
    
    return delay(arrow_135)


def range_big_int(start: Any, step: Any, stop: Any) -> IEnumerable[Any]:
    def arrow_136(x: Any, y: Any, start: Any=start, step: Any=step, stop: Any=stop) -> Any:
        return op_addition(x, y)
    
    return integral_range_step(start, step, stop, from_zero(), arrow_136)


def range_decimal(start: Any, step: Any, stop: Any) -> IEnumerable[Any]:
    def arrow_137(x: Any, y: Any, start: Any=start, step: Any=step, stop: Any=stop) -> Any:
        return op_addition_1(x, y)
    
    return integral_range_step(start, step, stop, from_parts(0, 0, 0, False, 0), arrow_137)


def range_double(start: float, step: float, stop: float) -> IEnumerable[float]:
    def arrow_138(x: float, y: float, start: float=start, step: float=step, stop: float=stop) -> float:
        return x + y
    
    return integral_range_step(start, step, stop, 0, arrow_138)


def range_int64(start: Any, step: Any, stop: Any) -> IEnumerable[Any]:
    def arrow_139(x: Any, y: Any, start: Any=start, step: Any=step, stop: Any=stop) -> Any:
        return op_addition_2(x, y)
    
    return integral_range_step(start, step, stop, from_bits(0, 0, False), arrow_139)


def range_uint64(start: Any, step: Any, stop: Any) -> IEnumerable[Any]:
    def arrow_140(x: Any, y: Any, start: Any=start, step: Any=step, stop: Any=stop) -> Any:
        return op_addition_2(x, y)
    
    return integral_range_step(start, step, stop, from_bits(0, 0, True), arrow_140)


def range_char(start: str, stop: str) -> IEnumerable[str]:
    int_stop : int = ord(stop) or 0
    def arrow_141(start: str=start, stop: str=stop) -> IEnumerable[str]:
        def step_fn(c: int) -> Option[Tuple[str, int]]:
            if c <= int_stop:
                return (chr(c), c + 1)
            
            else: 
                return None
            
        
        return unfold(step_fn, ord(start))
    
    return delay(arrow_141)


