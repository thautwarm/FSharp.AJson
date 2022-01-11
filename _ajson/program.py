from __future__ import annotations
from array import array
import sys
from typing import (MutableSequence, TypeVar, Generic, Any, List)
from .ajson import (obj_from_json, parse_json, serialize_json, obj_to_json)
from .fable_modules.fable_library.list import of_array
from .fable_modules.fable_library.option import Option
from .fable_modules.fable_library.reflection import (TypeInfo, int32_type, array_type, option_type, record_type, string_type, list_type, int8_type, union_type)
from .fable_modules.fable_library.string import (to_console, printf)
from .fable_modules.fable_library.types import (Record, Union)
from .fable_modules.fable_library.util import equals

_A = TypeVar("_A")

def expr_0(gen0: TypeInfo) -> TypeInfo:
    return record_type("Prog.testRecord`1", [gen0], test_record_1, lambda: [["x", gen0], ["y", array_type(int32_type)], ["c", option_type(int32_type)]])


class test_record_1(Record, Generic[_A]):
    def __init__(self, x: _A, y: MutableSequence[int], c: Option[int]) -> None:
        super().__init__()
        self.x = x
        self.y = y
        self.c = c
    

test_record_1_reflection = expr_0

def expr_1(gen0: TypeInfo) -> TypeInfo:
    return union_type("Prog.S`1", [gen0], S_1, lambda: [[["Item", gen0]], [["Item1", string_type], ["Item2", gen0]], [["Item", array_type(S_1_reflection(gen0))]], [["Item", list_type(gen0)]], [["Item1", array_type(int8_type)], ["Item2", list_type(S_1_reflection(gen0))]]])


class S_1(Union, Generic[_A]):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag : int = tag or 0
        self.fields : List[Any] = list(fields)
    
    @staticmethod
    def cases() -> List[str]:
        return ["S1", "S2", "S3", "S4", "S5"]
    

S_1_reflection = expr_1

def test(_arg1: List[str]) -> int:
    arg10 : test_record_1[int] = obj_from_json(test_record_1_reflection(int32_type), parse_json("{\"x\": 2, \"y\": [3, 5, 6], \"c\": null}"))
    to_console(printf("%A"))(arg10)
    arg10_1 : test_record_1[int] = obj_from_json(test_record_1_reflection(int32_type), parse_json("{\"x\": 100, \"y\": [], \"c\": 10}"))
    to_console(printf("%A"))(arg10_1)
    arg10_2 : test_record_1[int] = obj_from_json(test_record_1_reflection(int32_type), parse_json("{\"x\": 100, \"y\": [], \"c\": 10}"))
    to_console(printf("%A"))(arg10_2)
    arg10_3 : S_1[int] = obj_from_json(S_1_reflection(int32_type), parse_json("{\"_TAG\": \"S1\", \"_VALUES\": [3]}"))
    to_console(printf("%A"))(arg10_3)
    r : test_record_1[int] = obj_from_json(test_record_1_reflection(int32_type), parse_json("{\"x\": 100, \"y\": [], \"c\": 10}"))
    s1 : S_1[test_record_1[int]] = S_1(0, r)
    s2 : S_1[test_record_1[int]] = S_1(1, "string", r)
    s3 : S_1[test_record_1[int]] = S_1(2, [s1, s2])
    s5 : S_1[test_record_1[int]] = S_1(4, array("b", [(int(2) + 0x80 & 0xFF) - 0x80]), of_array([s1, s2, s3, S_1(3, of_array([r, r]))]))
    s_5 : str = serialize_json(obj_to_json(S_1_reflection(test_record_1_reflection(int32_type)), s5))
    to_console(printf("%s"))(s_5)
    arg10_5 : bool = equals(obj_from_json(S_1_reflection(test_record_1_reflection(int32_type)), parse_json(s_5)), s5)
    to_console(printf("%A"))(arg10_5)
    return 0


if __name__ == "__main__":
    test(sys.argv[1:])


