# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['az_evgrid_pydantic_schema']

package_data = \
{'': ['*']}

install_requires = \
['datamodel-code-generator>=0.13.0,<0.14.0', 'pydantic>=1.9.1,<2.0.0']

setup_kwargs = {
    'name': 'az-evgrid-pydantic-schema',
    'version': '0.2.0',
    'description': 'Azure Event Grid の event schema  を Pydantic Model で提供',
    'long_description': '# az-evgrid-pydantic-schema\nAzure Event Grid の event schema を Pydantic Model で提供\n\n## 使い方\n\nAzure Event Grid の event データ(json形式) を Pydantic Model Object にパースできます。  \n現段階では以下のイベントに対応しています。\n\n- 実装済みのイベント\n    - Microsoft.Storage.BlobCreated イベント\n         - https://docs.microsoft.com/ja-jp/azure/event-grid/event-schema-blob-storage?tabs=event-grid-event-schema#microsoftstorageblobcreated-event\n         - https://docs.microsoft.com/ja-jp/azure/event-grid/event-schema?WT.mc_id=Portal-Microsoft_Azure_EventGrid\n\ntest ファイルの中身を見ると使い方がわかります。\n\n## 開発方法\n\n以下手順を実行して、ローカルソースを利用したテストができます。\n\n```shell\n$ poetry shell\n$ poetry run task test\n```\n\n## publish\n\n- `poetry build`\n- `poetry publish` \n    - `poetry publish` すると user と password の確認が求められます。\n- https://cocoatomo.github.io/poetry-ja/repositories/\n',
    'author': 'Niten Nashiki',
    'author_email': 'n.nashiki.work@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/nnashiki/az-evgrid-pydantic-schema',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
