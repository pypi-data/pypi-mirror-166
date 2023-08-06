# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['purus']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'purus',
    'version': '0.1.1',
    'description': 'parse parameters',
    'long_description': '# purus\n\n[![Pytest](https://github.com/acxelerator/purus/actions/workflows/pytest.yml/badge.svg)](https://github.com/acxelerator/purus/actions/workflows/pytest.yml)\n[![codecov](https://codecov.io/gh/acxelerator/purus/branch/main/graph/badge.svg?token=2X3BA0RCER)](https://codecov.io/gh/acxelerator/purus)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n\n[![PythonVersion](https://img.shields.io/pypi/pyversions/purus.svg)](https://pypi.org/project/purus/)\n[![PiPY](https://img.shields.io/pypi/v/purus.svg)](https://pypi.org/project/purus/)\n\n\n`purus` parses parameters provided from Lambda@Edge on CloudFront, and it manipulates request and response.\nIt is named after The Purus River, or a tributary of The Amazon River.\n\n\n## Install\n\n```shell\n$ pip install purus\n```\n\n## Usage\n\n### CloudFront:Lambda@Edge\n\n`purus` can parse parameters of\n\n- viewer-request\n- origin-request\n- origin-response\n- viewer-response\n\n```python\n# Lambda@Edge\nfrom purus.amazon_cloudfront import CloudFrontLambdaEdge\n\n# on viewer-request or origin-request\ndef lambda_handler(event: dict, _):\n    # load data\n    lambda_edge = CloudFrontLambdaEdge.from_event(event=event)\n    \n    # return on error\n    if some_error_occurred:\n        pseudo_payload = lambda_edge.add_pseudo_response(\n            status="400",\n            status_description="error_occurred"\n        )\n        return pseudo_payload.response.format()\n    \n    # redirect\n    if redirect_condition:\n        pseudo_payload = lambda_edge.add_pseudo_redirect_response(\n            status="307",\n            status_description="Redirect",\n            location_url="https://redirect.example.com"\n        )\n        return pseudo_payload.response.format()\n    \n    # add headers to request\n    modified_request = lambda_edge.append_request_header(\n        key="X-Original-Header",\n        value="Your data"\n    ).append_request_header(\n        key="X-Original-Header",\n        value="Your additional data"\n    )\n    \n    # to request\n    return  modified_request.request.format()\n\n\n```',
    'author': 'acxelerator',
    'author_email': 'acx0911@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/acxelerator/purus',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
