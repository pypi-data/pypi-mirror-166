# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['memory_efficient_transformer',
 'memory_efficient_transformer.models',
 'memory_efficient_transformer.utils',
 'memory_efficient_transformer.utils.jax',
 'memory_efficient_transformer.utils.stub']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21.6', 'torch>=1.10.2', 'tqdm>=4.64.0', 'transformers>=4.20.1']

setup_kwargs = {
    'name': 'memory-efficient-transformer-pytorch',
    'version': '0.2.0',
    'description': 'Implementation on PyTorch of Self-attention Does Not Need $O(n^2)$ Memory',
    'long_description': '# faster-transformer\n\n*Self-attention Does Not Need $O(n^2)$ Memory*のPytorch実装\n\n```bibtex\n@misc{rabe2021selfattention,\n    title={Self-attention Does Not Need $O(n^2)$ Memory}, \n    author={Markus N. Rabe and Charles Staats},\n    year={2021},\n    eprint={2112.05682},\n    archivePrefix={arXiv},\n    primaryClass={cs.LG}\n}\n```\n',
    'author': 'yuta0306',
    'author_email': 'you-2001-3-6@ezweb.ne.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yuta0306/memory-efficient-transformer-pytorch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
