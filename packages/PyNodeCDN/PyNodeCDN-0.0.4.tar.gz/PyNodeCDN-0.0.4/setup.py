from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]
setup(
    name="PyNodeCDN",
    version='0.0.4',
    description='A simple implementation for webservers that provides a cool, consistent route to NodeCDN on your site.',
    long_description=f'A simple implementation for webservers that provides a cool, consistent route to NodeCDN on your site. More features coming soon. \n\n(Lastest on top)\n - Added Version 0.0.4(made flask available)\n - Added Version 0.0.3\n - Added Version 0.0.2\n\nCurrently supports these: \n- Flask',
    url='',
    author='Eric Vicente',
    author_email='justaneric.c@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='JavaScript, Python, Webserver, Development',
    packages=find_packages(),
    install_requires=['']
)