# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ulinkme', 'ulinkme.handlers']

package_data = \
{'': ['*']}

install_requires = \
['watchdog>=2.1.9,<3.0.0']

entry_points = \
{'console_scripts': ['ulinkme = ulinkme.main:cli']}

setup_kwargs = {
    'name': 'ulinkme',
    'version': '0.1.0',
    'description': 'A cross-platform tool for automatically creating hard links recursively in real time for all files in a given folder.',
    'long_description': '## ULinkMe\n\n一个用于自动为指定文件夹内的所有文件实时递归创建硬链接的跨平台工具\n\nA cross-platform tool for automatically creating hard links recursively in real time for all files in a given folder\n\n### Usage 使用\n\n\n\n1. 使用pip下载ulinkme\nUse pip to download ulinkme\n\n```bash\npip install ulinkme\n```\n\n2. 创建json配置文件，一份示例配置参照[config.example.json](config.example.json)\nCreate a json configuration file, a sample configuration reference [config.example.json](config.example.json)\n\n3. 运行ulinkme\nRun ulinkme\n\n```bash\nulinkme ./config.json\n```\n\n### Configuration 配置文件\n\n| 键值             | 类型 / 默认值                 | 说明                                                               |\n| ---------------- | ----------------------------- | ------------------------------------------------------------------ |\n| `log.level`      | `String` / `warning`          | 日志的等级，可选debug/info/warning/errorg                          |\n| `log.logdir`     | `String` / `None`             | 日志的输出目录，不填写则输出至标准流中                             |\n| `links`          | `list[Link]` / `[]`           | 描述链接目录的对象列表                                             |\n| `Link.target`    | `String` / required           | 链接的目标文件夹名，如果不存在则会自动创建                         |\n| `Link.name`      | `String` / required           | 链接的文件夹名，我们将会创建形如`name->target`的硬链接             |\n| `Link.recursive` | `Bool` / `true`               | 是否递归链接文件夹下的文件，目前只支持文件夹到文件夹的递归链接     |\n| `Link.events`    | `list[String]` / `["create"]` | 同步两个文件夹下的哪些操作，目前支持的有`create`, `move`, `delete` |\n\n| Key              | Value Type / Default Value    | Description                                                                                                     |\n| ---------------- | ----------------------------- | --------------------------------------------------------------------------------------------------------------- |\n| `log.level`      | `String` / `warning`          | The level of the log, optional debug/info/warning/error                                                         |\n| `log.logdir`     | `String` / `None`             | The output directory of the logs, or to the standard stream if not filled in                                    |\n| `links`          | `list[Link]` / `[]`           | List of objects describing the linked directory                                                                 |\n| `Link.target`    | `String` / required           | Target folder name of the link, create automatically if doesn\'t exist                                           |\n| `Link.name`      | `String` / required           | For the linked folder name, we will create a hard link like `name->target`                                      |\n| `Link.recursive` | `Bool` / `true`               | Whether to recursively link files under folders, currently only folder-to-folder recursive linking is supported |\n| `Link.events`    | `list[String]` / `["create"]` | What operations are synchronized under two folders, currently supported are `create`, `move`, `delete`          |\n\n### LICENSE 协议\n\n项目使用MIT LICENSE开源\n\nThe project is licensed under MIT LICENSE\n',
    'author': 'Hyiker',
    'author_email': 'hyikerhu0212@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Hyiker/ULinkMe',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
