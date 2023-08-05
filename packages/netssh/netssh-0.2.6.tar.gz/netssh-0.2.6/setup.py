from setuptools import find_packages, setup

from os import path
top_level_directory = path.abspath(path.dirname(__file__))
with open(path.join(top_level_directory, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='netssh',
    version='0.2.6',
    url='',
    description='NetBox WebSSH.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Maximqa',
    author_email='max.z.a2@yandex.ru',
    install_requires=[],
    packages=find_packages(),
    license='',
    include_package_data=True,
    keywords=['netbox', 'netbox-plugin', 'plugin'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)