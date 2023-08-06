# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ETH_Terminal']

package_data = \
{'': ['*']}

install_requires = \
['nonebot-adapter-onebot>=2.1.0,<3.0.0', 'nonebot2>=2.0.0b3,<3.0.0']

setup_kwargs = {
    'name': 'nonebot2-plugin-eth-terminal',
    'version': '0.0.1',
    'description': '查询 ETH 预计难度到达 5.875E18 合并难度的时间',
    'long_description': '# nonebot2_plugin_eth_terminal\n\n查询 ETH 合并日期\n\n<div align="center">\n\n# 查询 ETH 合并日期\n\n</div>\n\n## 版本\n\nv0.0.1\n\n## 安装\n\n1. 通过`pip`和`nb`安装；\n\n命令\n\n`pip install nonebot_plugin_eth_terminal`\n`nb plugin install nonebot_plugin_eth_terminal`\n\n## 功能\n\n查询 ETH 预计难度到达 5.875E18 合并难度的时间\n\n## 命令\n\n`ETH` `eth`\n',
    'author': 'Sclock',
    'author_email': '1342810270@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Sclock/nonebot2_plugin_eth_terminal',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
