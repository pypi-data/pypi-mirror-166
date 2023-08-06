# potc_typing

[![PyPI](https://img.shields.io/pypi/v/potc-typing)](https://pypi.org/project/potc-typing/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/potc-typing)](https://pypi.org/project/potc-typing/)

[![Code Test](https://github.com/potc-dev/potc-typing/workflows/Code%20Test/badge.svg)](https://github.com/potc-dev/potc-typing/actions?query=workflow%3A%22Code+Test%22)
[![Package Release](https://github.com/potc-dev/potc-typing/workflows/Package%20Release/badge.svg)](https://github.com/potc-dev/potc-typing/actions?query=workflow%3A%22Package+Release%22)
[![codecov](https://codecov.io/gh/potc-dev/potc-typing/branch/main/graph/badge.svg?token=XJVDP4EFAT)](https://codecov.io/gh/potc-dev/potc-typing)

[![GitHub stars](https://img.shields.io/github/stars/potc-dev/potc-typing)](https://github.com/potc-dev/potc-typing/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/potc-dev/potc-typing)](https://github.com/potc-dev/potc-typing/network)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/potc-dev/potc-typing)
[![GitHub issues](https://img.shields.io/github/issues/potc-dev/potc-typing)](https://github.com/potc-dev/potc-typing/issues)
[![GitHub pulls](https://img.shields.io/github/issues-pr/potc-dev/potc-typing)](https://github.com/potc-dev/potc-typing/pulls)
[![Contributors](https://img.shields.io/github/contributors/potc-dev/potc-typing)](https://github.com/potc-dev/potc-typing/graphs/contributors)
[![GitHub license](https://img.shields.io/github/license/potc-dev/potc-typing)](https://github.com/potc-dev/potc-typing/blob/master/LICENSE)

A simple demo of `potc` plugin, which can make the dict prettier.

## Installation

You can simply install it with `pip` command line from the official PyPI site.

```shell
pip install potc-typing
```

Or install this  plugin by source code

```shell
git clone https://github.com/potc-dev/potc-typing.git
cd potc-typing
pip install .
```

## Effect show

We prepare a python script named `test_data.py`, like this

```python
import types
from typing import List, Union, Tuple, Callable, Dict

t_lst = List[int]
t_tps = Union[Tuple[int, ...], int]
t_func = Callable[[Union[str, int, None], int], Dict[str, types.FunctionType]]

```

Before the installation mentioned above, we try to export the `b` in `test_data.py` by the following CLI command

```shell
potc export -v 'test_data.t_*'
```

We can get this dumped source code.

```python
from typing import _GenericAlias

from potc.supports import typed_object

__all__ = ['t_func', 't_lst', 't_tps']
t_func = typed_object(
    _GenericAlias,
    b'x\x9cE\x8d\xbdn\xc20\x1c\xc4\x03\xa1\x1f\xfc\xcbG\xa1@_\xa1\x13/\x01#b\xb0@bA\x96\xe3X\xd8\x92c\xe7Rw\xe8\xd6%\xe6\xb5\x89\x85T\x96\x1b\xee~w\xf7\x97K\xeek\xd5\x88\xe0\x1b\xba\xa8`\x82\xaa\x08\x99\x0c\xbf\xb5q\x17\xda\x08kEa\x15\xa1wF\xffK\xff\x07Gg\xbc#\xe4\xb24\xd6\xaeyR\xe2\xd6\x8b\x92w@\x87\x0fNy\x96e\xdf\xa1\xc1S\x8bg\x86\x17}w\x8c\x0bxm1d \xc9y\xf1cl0\x8es\xda{\xa7\x0e\xa9y\xc5[\xc4\x88a\xacI=\xee\xb6F\x06\xc2D\xa7\x19\xeafv\xa2*J\x91\n\x98\xb6xg\x98E\xcc#>\x18\x16\x11\xcb\x88\x15\xc3\xe7\xfa\x06\xe4\xe1E\x9e'
)
t_lst = typed_object(
    _GenericAlias,
    b'x\x9ck`N\x8e\xcf/H-J,\xc9/\xe2JO-\xc9,I\xcd\xe5*dH.\xa9,\xc8\xccK\xe7\xf2\xc9,.\xe1*dLN\xc9\xcc\xc9\xd1\x8b\x07\x91\\\xf19\xf9\x89)\xf1@\xf9T\xaeB\xa6\x08f\x06\x06\x86\xcc\xbc\x92B\xe6\xd6B\x96\xa0B\xd6\xb6B\xb6\xa0Bv=\x00\x12K\x1b\xf8'
)
t_tps = typed_object(
    _GenericAlias,
    b"x\x9cU\xcaK\x0e\xc2 \x14\x85a\xb4Z\xeb\xf5\xb9\x92\xee\xc2\r\x10M:#MK\xda\x9b p(\x9a8sR\xd6-NL\x9c\x9c\xc1\x7f\xbew\xd1)\xe7uh\xa3\x0b4\xe8\xc8Q\xdf\t\xa2\x8b/\xcfv\xa0\x9beg\t\x8b\xf1W\xae\x0fo4a\xd9\xf5lL\xad\xbeK\xca\xb8\xb6W\x19\xe4\xa3h\n!\x04\xdb\x88\xd5\x8c\xb5D\xf9\x07\xf5\xb35*h\x1f\x08\x9b\xa6\xca\xf0b\x0c\xfb\x89'T3\xb6\x12\x94\xb0K\xd8K\x1c\xc62\xe1\x98p\x928\xd7\x1f\x06\x835\x89"
)

```

BUT, after the installation, **we try the CLI command which is exactly the same again, we get the new code**

```python
import types
from typing import Callable, Dict, List, Optional, Tuple, Union

__all__ = ['t_func', 't_lst', 't_tps']
t_func = Callable[[Optional[Union[str, int]], int], Dict[str, types.LambdaType]]
t_lst = List[int]
t_tps = Union[Tuple[int, ...], int]
```

That is all of this plugin. **When you need to build your own plugin, maybe this demo can help you :smile:.**

