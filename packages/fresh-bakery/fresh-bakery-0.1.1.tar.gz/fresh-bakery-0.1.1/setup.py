# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bakery']

package_data = \
{'': ['*']}

modules = \
['py']
entry_points = \
{'pytest11': ['bakery_mock = bakery.testbakery']}

setup_kwargs = {
    'name': 'fresh-bakery',
    'version': '0.1.1',
    'description': 'Bake your dependencies stupidly simple!',
    'long_description': '\n<p align="center">\n  <a href="https://fresh-bakery.readthedocs.io/en/latest/"><img width="300px" src="https://user-images.githubusercontent.com/17745407/187294435-a3bc6b26-b7df-43e5-abd3-0d7a7f92b71e.png" alt=\'fresh-bakery\'></a>\n</p>\n<p align="center">\n    <em>🍰 The little DI framework that taste like a cake. 🍰</em>\n</p>\n\n---\n\n**Documentation**: [https://fresh-bakery.readthedocs.io/en/latest/](https://fresh-bakery.readthedocs.io/en/latest/)\n\n---\n\n# Fresh Bakery\n\nFresh bakery is a lightweight [Dependency Injection][DI] framework/toolkit,\nwhich is ideal for building object dependencies in Python.\n\nIt is [nearly] production-ready, and gives you the following:\n\n* A lightweight, stupidly simple DI framework.\n* Fully asynchronous, no synchronous mode.\n* Any async backends compatible (`asyncio`, `trio`).\n* Zero dependencies.\n* `Mypy` compatible (no probably need for `# type: ignore`).\n* `FastAPI` fully compatible.\n* `Pytest` fully compatible (Fresh Bakery encourages the use of `pytest`).\n* Ease of testing.\n* Easily extended (contribution is welcome).\n\n## Requirements\n\nPython 3.6+\n\n## Installation\n\n```shell\n$ pip3 install fresh-bakery\n```\n\n## Example\n\n**example.py**:\n\n```python\nimport asyncio\nfrom dataclasses import dataclass\nfrom bakery import Bakery, Cake\n\n@dataclass\nclass Settings:\n    database_dsn: str\n    info_id_list: list[int]\n    \nclass Database:\n    def __init__(self, dsn: str):\n        self.dsn: str = dsn\n    async def fetch_info(self, info_id: int) -> dict:\n        return {"dsn": self.dsn, "info_id": info_id}\n        \nclass InfoManager:\n    def __init__(self, database: Database):\n        self.database: Database = database\n    async def fetch_full_info(self, info_id: int) -> dict:\n        info: dict = await self.database.fetch_info(info_id)\n        info["full"] = True\n        return info\n        \nclass MyBakery(Bakery):\n    settings: Settings = Cake(Settings, database_dsn="my_dsn", info_id_list=[1,2,3])\n    database: Database = Cake(Database, dsn=settings.database_dsn)\n    manager: InfoManager = Cake(InfoManager, database=database)\n    \nasync def main() -> None:\n    async with MyBakery() as bakery:\n        for info_id in bakery.settings.info_id_list:\n            info: dict = await bakery.manager.fetch_full_info(info_id)\n            assert info["dsn"] == bakery.settings.database_dsn\n            assert info["info_id"] == info_id\n            assert info["full"]\n            \nif __name__ == "__main__":\n    asyncio.run(main())\n```\n\nFor a more complete example, see [bakery examples](https://github.com/Mityuha/fresh-bakery/tree/main/examples).\n\n## Dependencies\n\nNo dependencies ;)\n\n---\n\n<p align="center"><i>Fresh Bakery is <a href="https://github.com/Mityuha/fresh-bakery/blob/main/LICENSE">MIT licensed</a> code.</p>\n',
    'author': 'Dmitry Makarov',
    'author_email': 'mit.makaroff@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<3.11',
}


setup(**setup_kwargs)
