# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wagtail_svg_images',
 'wagtail_svg_images.migrations',
 'wagtail_svg_images.models',
 'wagtail_svg_images.templatetags']

package_data = \
{'': ['*'],
 'wagtail_svg_images': ['static/js/*',
                        'templates/wagtailadmin/edit_handlers/*']}

install_requires = \
['wagtail>=3.0,<4.0', 'wagtailsvg>=0.0.33,<0.0.34']

setup_kwargs = {
    'name': 'wagtail-svg-images',
    'version': '0.1.21',
    'description': 'Workaround to support SVG as Images in Wagtail',
    'long_description': None,
    'author': 'Ramiro A Alvarez U',
    'author_email': 'liko28s@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
