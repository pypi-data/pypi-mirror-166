# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aio_clients', 'aio_clients.multipart']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.0']

setup_kwargs = {
    'name': 'aio-clients',
    'version': '1.0.0',
    'description': 'Python aiohttp client',
    'long_description': '# aiohttp client\n\n### What is the difference from aiohttp.Client?\n\nIt is simpler and as a Requests\n\n----\n\n## Install beta:\n\n```bash\npip install aio-clients\n```\n\n----\n\n# Example:\n\n## Base reqeust:\n\n```python\nimport asyncio\nfrom aio_clients import Http, Options\n\n\nasync def main():\n    r = await Http().get(\'https://google.com\', o=Options(is_json=False, is_close_session=True))\n    print(f\'code={r.code} body={r.body}\')\n\n\nasyncio.run(main())\n```\n\n## Async reqeust\n\n```python\nimport asyncio\n\nimport aiohttp\nfrom aio_clients import Http, Options\n\n\nasync def on_request_start(session, trace_config_ctx, params):\n    print("Starting request")\n\n\nasync def on_request_end(session, trace_config_ctx, params):\n    print("Ending request")\n\n\nasync def main():\n    trace_config = aiohttp.TraceConfig()\n    trace_config.on_request_start.append(on_request_start)\n    trace_config.on_request_end.append(on_request_end)\n\n    http = Http(\n        host=\'https://google.com/search\',\n        option=Options(trace_config=trace_config, is_json=False),\n    )\n\n    r = await asyncio.gather(\n        http.get(q_params={\'q\': \'test\'}),\n        http.get(q_params={\'q\': \'hello_world\'}),\n        http.get(q_params={\'q\': \'ping\'}),\n    )\n\n    print(f\'status code={[i.code for i in r]} body={[i.body for i in r]}\')\n    await http.close()\n\n\nasyncio.run(main())\n```\n\n## Multipart reqeust:\n\n```python\nimport asyncio\nfrom aio_clients import Http, Options\nfrom aio_clients.multipart import Easy, Form, File, Writer\n\n\nasync def main():\n    with Easy(\'form-data\') as form:\n        form.add_form(Form(key=\'chat_id\', value=12345123))\n        form.add_form(Form(key=\'audio\', value=\'hello world\'))\n        form.add_form(File(key=\'file\', value=b\'hello world file\', file_name=\'test.py\'))\n\n    r = await Http(option=Options(is_close_session=True, is_json=False)).post(\n        \'http://localhost:8081\',\n        form=form,\n    )\n\n    writer = Writer()\n    await form.write(writer)\n\n    print(f\'code={r.code} body={r.body}\')\n    print(f\'full body:\\n{writer.buffer.decode()}\')\n\n\nasyncio.run(main())\n```\n',
    'author': 'Denis Malin',
    'author_email': 'denis@malina.page',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/skar404/aio-clients',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
