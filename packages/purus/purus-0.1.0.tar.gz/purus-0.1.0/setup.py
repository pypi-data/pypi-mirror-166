# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['purus']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'purus',
    'version': '0.1.0',
    'description': 'parse parameters',
    'long_description': '# purus\n\n`purus` parses parameters provided from AWS services.\nIt is named after The Purus River, or a tributary of The Amazon River.\n\n\n## Install\n\n```shell\n$ pip install purus\n```\n\n## Usage\n\n### CloudFront:Lambda@Edge\n\n`purus` can parse parameters of\n\n- viewer-request\n- origin-request\n- origin-response\n- viewer-response\n\n```python\n# Lambda@Edge\nfrom purus.amazon_cloudfront import CloudFrontLambdaEdge\n\n# on viewer-request or origin-request\ndef lambda_handler(event: dict, _):\n    data = event["Records"][0]["cf"]\n    # load data\n    lambda_edge = CloudFrontLambdaEdge.from_dict(data=data)\n    \n    # return on error\n    if some_error_occurred:\n        response = lambda_edge.add_pseudo_response(\n            status="400",\n            status_description="error_occurred"\n        )\n        return response\n    \n    # add headers to request\n    modified_request = lambda_edge.append_request_header(\n        key="X-Original-Header",\n        value="Your data"\n    ).append_request_header(\n        key="X-Original-Header",\n        value="Your additional data"\n    )\n    \n    # to request\n    return  modified_request.request\n\n\n```',
    'author': 'acxelerator',
    'author_email': 'acx0911@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/acxelerator/purus',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
