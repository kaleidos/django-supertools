# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name = 'django-supertools',
    version = "0.1",
    description = "Generic tools for django apps.",
    long_description = "",
    keywords = 'django',
    author = 'Jesús Espino García & Andrey Antukh',
    author_email = 'jespinog@gmail.com, niwi@niwi.be',
    url = 'https://github.com/kaleidos/django-supertools',
    license = 'BSD',
    include_package_data = True,
    packages = find_packages(),
    install_requires=[
        'pytz',
    ],
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Django',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
    ]
)
