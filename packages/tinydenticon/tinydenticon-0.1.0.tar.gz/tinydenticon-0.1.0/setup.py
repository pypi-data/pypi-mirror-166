# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tinydenticon']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.2.0,<10.0.0',
 'pycryptodomex>=3.15.0,<4.0.0',
 'webcolors>=1.12,<2.0']

setup_kwargs = {
    'name': 'tinydenticon',
    'version': '0.1.0',
    'description': 'identicon.js compatible Identicon implementation in Python 3',
    'long_description': '# tinydenticon\n\nPython 3 implementation of Identicon.\n\nSpecifically designed to produce the same results as [identicon.js](https://github.com/stewartlord/identicon.js)\n\n## Installation:\n### Pip:\n```sh\npip3 install tinydenticon\n```\n\n## Usage example:\n```python\nfrom PIL import Image\nfrom tinydenticon import Identicon\n\n\ndef main():\n    text = "tinytengu"\n    size = 500\n    rounds = 1337\n\n    identicon = Identicon(text.encode(), hash_rounds=rounds, image_side=size)\n\n    image = Image.new("RGB", (size, size))\n    image.putdata(identicon.get_pixels())\n    image.show()\n\n\nif __name__ == "__main__":\n    main()\n\n```\n\n## License\n[GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.html)',
    'author': 'tinytengu',
    'author_email': 'tinytengu@yandex.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
