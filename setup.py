from setuptools import setup, find_packages

install_requires = [
        'setuptools',
        'Django',
        'geopy',
        'gvis-api',
]

dependency_links = [
        'http://pypi.saaskit.org/geopy/',
        'http://pypi.saaskit.org/gvis-api/',
        'http://dist.repoze.org',
]
 
setup(name="saaskit-trackerstats",
           version="0.1",
           description="Django application viewing statistics information via Google Visialuzation API",
           author="CrowdSense",
           author_email="admin@crowdsense.com",
           packages=find_packages(),
           include_package_data=True,
           install_requires = install_requires,
           entry_points="""
           # -*- Entry points: -*-
           """,
           dependency_links = dependency_links,
)
