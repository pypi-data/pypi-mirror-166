from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]
setup(
    name="PyNodeCDN",
    version='0.0.2',
    description='A simple implementation for webservers that provides a cool, consistent route to NodeCDN on your site.',
    long_description=f'A simple implementation for webservers that provides a cool, consistent route to NodeCDN on your site. More features coming soon. \n\n{open("CHANGELOG","r").read()}\n\nCurrently supports these: \n{open("SUPPORTED_WS_OPTIONS", "r").read()}',
    url='',
    author='Eric Vicente',
    author_email='justaneric.c@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='JavaScript, Python, Webserver, Development',
    packages=find_packages(),
    install_requires=['']
)