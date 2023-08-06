from setuptools import setup, find_packages


setup(
    name='awl_telegram_connector',
    version='0.1',
    license='None',
    author="Andrew Levin",
    author_email='email@example.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    python_requires=">=3.6",
    url='https://github.com/levinandrey/awl-telegram-connector',
    keywords='example project',
    install_requires=[
        'pyaml',
        'awesome-slugify',
        'python-telegram-bot>=20.0a4',
    ],
)
