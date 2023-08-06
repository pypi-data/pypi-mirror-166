import types

import pytest

from potc.testing import provement
from potc.testing import transobj_assert


@pytest.mark.unittest
class TestTypes(provement()):
    def test_type_none(self):
        with transobj_assert(type(None)) as (obj, name):
            assert isinstance(obj, type)
            assert isinstance(None, obj)
            assert name == 'type_none'

    def test_types_class(self):
        with transobj_assert(types.FunctionType) as (obj, name):
            assert isinstance(obj, type)
            assert obj == types.FunctionType
            assert name == 'types_class'
