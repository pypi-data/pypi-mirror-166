# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyautoppt']

package_data = \
{'': ['*']}

install_requires = \
['pywin32>=304,<305']

setup_kwargs = {
    'name': 'pyautoppt',
    'version': '0.1.1',
    'description': '这是一个简单的 PPT 自动化',
    'long_description': '# pyautoppt\n\n## 基本用法\n\n```python\nfrom pyautoppt import ppt\n\n# 新建 ppt文件\npre_ref = ppt.add()\n# 添加幻灯片\npre_ref.slides.add(1,12)\n\n```\n',
    'author': 'wn0x00',
    'author_email': '320753691@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://python-poetry.org/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
