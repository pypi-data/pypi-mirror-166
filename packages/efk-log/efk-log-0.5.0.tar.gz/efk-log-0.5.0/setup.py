# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['efk_log']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'efk-log',
    'version': '0.5.0',
    'description': '',
    'long_description': "# Efk-log\n\n## Quick start\n\n> Called from where the project was launched.\n\n## Install\n`pip install efk-log==0.31` : no trace-code\n`pip install efk-log==0.5.0` : add trace-code\n\n\n\n\n### En\n\n1. Logs in json format are easily collected in es and can be easily indexed on top of kibana for related fields.\n\n2. Note that it is important to avoid index value conflicts, as different value types for the same index name can cause conflicts.\n\n3. Use the supervisor to guard the service processes started by gunicorn when starting a multi-process service, in conjunction with the supervisor's logging feature.\n\n   1. file_path=None\n\n   2. supervisor-related parameters are sliced to avoid large log files.\n\n      ```\n      stdout_logfile_maxbytes = 50MB   ; max # logfile bytes b4 rotation (default 50MB)\n      stdout_logfile_backups = 10 ; # of stdout logfile backups (default 10)\n      stdout_logfile = /data/logs/efk-log/efk-log.log\n      ```\n\n### Zh\n\n1. json 格式的日志 方便收集到es中可方便对相关字段在kibana上面创建索引\n\n2. 需要注意的是，要避免索引值的冲突，相同的索引名，数值类型不同就会造成冲突\n\n3. 多进程启动 服务时候配合 supervisor 的日志功能使用，使用supervisor 守护gunicorn 启动的服务进程\n\n   1. file_path=None\n\n   2. supervisor 相关参数 进行切分，避免日志文件太大\n\n      ```\n      stdout_logfile_maxbytes = 50MB   ; max # logfile bytes b4 rotation (default 50MB)\n      stdout_logfile_backups = 10 ; # of stdout logfile backups (default 10)\n      stdout_logfile = /data/logs/efk-log/efk-log.log\n      ```\n\n\n\n### Flask \n\n```\nLogJsonFormat(file_path=None, console=True, project='efk-log')\n```\n\n### Celery\n\n```\nfrom celery.signals import setup_logging\n\n@setup_logging.connect\ndef set_log(*args, **kwargs):\n    LogJsonFormat(file_path=None, console=True, project='celery-prd')\n```\n\n\n\n### Demo\n\n```\nfrom efk_log import LogJsonFormat\n\nif __name__ == '__main__':\n    LogJsonFormat(file_path=None, console=True, project='efk-log')\n\n    import logging\n\n    LOGGER = logging.getLogger(__name__)\n\n    LOGGER.info('get user info', extra={'metrics': {\n        'cid': 'xxxxxx'\n    }})\n\n    try:\n        2 / 0\n    except Exception as e:\n        LOGGER.exception('except...', exc_info=e)\n\n    LOGGER.error('error')\n```\n",
    'author': 'lishulong',
    'author_email': 'lishulong.never@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
