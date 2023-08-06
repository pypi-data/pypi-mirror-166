import types

from potc.fixture import rule, Addons
from potc.rules import builtin_type


@rule(type_=type)
def type_none(v, addon: Addons):
    if v == type(None):
        return addon.val(type)(None)
    else:
        addon.unprocessable()


_TYPES_CLASSES = {
    name: getattr(types, name)
    for name in dir(types) if isinstance(getattr(types, name), type) and not name.startswith('_')
}
_TYPES_MAP = {
    obj.__name__: name for name, obj in _TYPES_CLASSES.items()
}


@rule(type_=type)
def types_class(v, addon: Addons):
    if v.__name__ in _TYPES_MAP:
        return getattr(addon.obj(types), _TYPES_MAP[v.__name__])
    else:
        addon.unprocessable()


types_all = [
    (type_none, types_class, builtin_type)
]
