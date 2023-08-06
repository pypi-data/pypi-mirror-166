from typing import NoReturn, TypeVar, Dict, Callable, List
from unittest import skipUnless

import pytest

from potc.testing import provement
from potc.testing import transobj_assert
from .testings import is_3_6, is_3_9


@pytest.mark.unittest
class TestTyping(provement()):
    def test_typing_items(self):
        with transobj_assert(NoReturn) as (obj, name):
            assert obj is NoReturn
            assert name == 'typing_items'

    def test_collection_types(self):
        with transobj_assert(List) as (obj, name):
            assert obj == List
            assert name == ('typing_items' if not is_3_6 else 'builtin_type')

        with transobj_assert(Dict) as (obj, name):
            assert obj == Dict
            assert name == ('typing_items' if not is_3_6 else 'builtin_type')

    def test_simple_collections(self):
        with transobj_assert(List[int]) as (obj, name):
            assert obj == List[int]
            assert name == 'typing_wrapper'

        with transobj_assert(Dict[int, List[int]]) as (obj, name):
            assert obj == Dict[int, List[int]]
            assert name == 'typing_wrapper'

    def test_callable(self):
        with transobj_assert(Callable[[], int]) as (obj, name):
            assert obj == Callable[[], int]
            assert name == 'typing_callable'

        with transobj_assert(Callable[..., int]) as (obj, name):
            assert obj == Callable[..., int]
            assert name == 'typing_callable'

        with transobj_assert(Callable[[int, str], List[int]]) as (obj, name):
            assert obj == Callable[[int, str], List[int]]
            assert name == 'typing_callable'

    @skipUnless(is_3_9, 'python 3.9 only')
    def test_advanced_general_alias(self):
        with transobj_assert(list[int]) as (obj, name):
            assert obj == list[int]
            assert name == 'typing_wrapper'

        with transobj_assert(dict[int, list[int]]) as (obj, name):
            assert obj == dict[int, list[int]]
            assert name == 'typing_wrapper'

    def test_typevar(self):
        K = TypeVar('K', bound=int, contravariant=True)
        V = TypeVar('V', int, str, covariant=True)

        with transobj_assert(K) as (obj, name):
            assert isinstance(obj, TypeVar)
            assert obj.__name__ == 'K'
            assert obj.__constraints__ == ()
            assert obj.__bound__ == int
            assert not obj.__covariant__
            assert obj.__contravariant__

            assert name == 'typing_typevar'

        with transobj_assert(V) as (obj, name):
            assert isinstance(obj, TypeVar)
            assert obj.__name__ == 'V'
            assert obj.__constraints__ == (int, str)
            assert obj.__bound__ is None
            assert obj.__covariant__
            assert not obj.__contravariant__

            assert name == 'typing_typevar'

        with transobj_assert(Dict[K, V]) as (obj, name):
            assert obj.__origin__ == (Dict if is_3_6 else dict)
            _k, _v = obj.__args__
            assert isinstance(_k, TypeVar)
            assert _k.__name__ == 'K'
            assert _k.__constraints__ == ()
            assert _k.__bound__ == int
            assert not _k.__covariant__
            assert _k.__contravariant__

            assert isinstance(_v, TypeVar)
            assert _v.__name__ == 'V'
            assert _v.__constraints__ == (int, str)
            assert _v.__bound__ is None
            assert _v.__covariant__
            assert not _v.__contravariant__

            assert name == 'typing_wrapper'
