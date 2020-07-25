from setuptools import setup, find_packages


setup(
    name='indico-authorised-user-search',
    version='0.1.dev0',
    author='Samaggi Samagom',
    packages=find_packages(),
    install_requires=[
        'indico>=2.0'
    ],
    entry_points={
        'indico.plugins': {'authorised_user_search = indico_authorised_user_search.plugin:AuthorisedUserSearchPlugin'}}
)
