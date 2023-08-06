# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['youtubedanyukla']
install_requires = \
['pytube>=12.1.0,<13.0.0']

setup_kwargs = {
    'name': 'youtubedanyukla',
    'version': '0.0.1',
    'description': 'Ushbu kutubxona yordamida Youtubedan videolarni osonlik bilan yuklab olishingiz mumkin!',
    'long_description': '```python\nfrom youtubedanyukla import Yukla\nYukla("https://youtu.be/9_A5sK1Kdzw", "H")\n```\n\n```html\n<h4>M - videoni musiqa ko\'rinishida yuklab olish</h4>\n<h4>H - videoni yuqori sifatda yuklab olish</h4>\n<h4>L - videoni past sifatda yuklab olish</h4>\n```',
    'author': 'YusupovDeveloper',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
