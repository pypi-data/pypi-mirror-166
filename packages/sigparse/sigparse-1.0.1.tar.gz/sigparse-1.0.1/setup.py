# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sigparse']

package_data = \
{'': ['*']}

install_requires = \
['forbiddenfruit>=0.1.4,<0.2.0']

setup_kwargs = {
    'name': 'sigparse',
    'version': '1.0.1',
    'description': 'Backports python3.10 typing features into python3.8 and python3.9.',
    'long_description': '# sigparse\n\nBackports python3.10 typing features into python3.8 and 3.9.\n\n## Example\n\n```python\nimport sigparse\n\ndef func(param_a: list[str], param_b: str | int, param_c: tuple[int | None]):\n    ...\n\n# This returns the same result in python 3.8, 3.9, and 3.10!\nsigparse.sigparse(func)\n```\n\n## Notes\n### Inspect\n\nThis module uses inspect behind the scenes. For that reason:\n\n- `sigparse.Parameter.default` is `inspect._empty` when there is no default value.\n- `sigparse.Parameter.kind` is `inspect._ParameterKind`.\n\n\n### Annotated\n`typing.Annotated` will always be evaluated with `include_extras=True` in python3.9.\n',
    'author': 'Lunarmagpie',
    'author_email': 'bambolambo0@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Lunarmagpie/sigparse',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
