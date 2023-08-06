# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hue_color_converter']

package_data = \
{'': ['*']}

install_requires = \
['Shapely>=1.8.4,<2.0.0', 'numpy>=1.23.2,<2.0.0']

setup_kwargs = {
    'name': 'hue-color-converter',
    'version': '0.2.1',
    'description': '',
    'long_description': '# Philips Hue Color Converter  (CIE xyY)\n\nConverts RGB to CIE xyY for Philips Hue\n\n```python\nfrom hue_color_converter import Converter\n\nconverter = Converter()  # optionally provide device id or "A", "B", "C" color gamut for more accurate colors\n\n(x, y), Y = converter.hex_to_xyY("ff00ff")\n# calculated brightness is on the scale of 0-1\n\nconverter.xyY_to_hex((0.3209, 0.1541), Y=0.2848)\n```\n\nClick [here](https://developers.meethue.com/develop/hue-api/supported-devices/) to see which color gamuts are supported for your device.\n\n## Installing hue-color-converter\n\n```shell\npip install hue-color-converter\n```\n\n## License\n\n[MIT](./LICENSE.txt)\n',
    'author': 'Zachary Juang',
    'author_email': 'zachary822@me.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
