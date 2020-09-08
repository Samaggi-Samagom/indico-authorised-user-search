from setuptools import setup, find_packages


setup(
    name='indico-authorised-user-search',
    version='0.1.0',
    author='Samaggi Samagom',
    author_email='tech@samaggisamagom.com',
    description='An Indico 2 plugin for allowing only users in a single group to search for other users',
    packages=find_packages(),
    install_requires=[
        'indico>=2.0'
    ],
    entry_points={
        'indico.plugins': {'authorised_user_search = indico_authorised_user_search.plugin:AuthorisedUserSearchPlugin'}}
)
