
from distutils.core import setup

setup(
    name='Spidy',
    version=open('spidy/VERSION').read().strip(),
    description='Spidy - Web scraping simplified!',
    long_description = open('README.rst').read(),
    url='https://github.com/alexpereverzyev/spidy',
    author='Spidy developers',
    maintainer='Alex Pereverzyev',
    maintainer_email='pereverzev.alex@gmail.com',
    license='BSD',
    platforms = [
        'Mac OS',
        'Linux',
        'Windows',
    ],
    classifiers = [
        'Environment :: Console',
        'Environment :: Web Environment',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: BSD License',        
        'Intended Audience :: Developers',        
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Interpreters',
        'Topic :: Software Development :: Libraries :: Python Modules',      
    ],
    requires = [
        'HTMLParser',
        'json',
        'xml.parsers.expat',
        'httplib',
        'codecs',
        'logging',
    ],
    packages = [
        'spidy',
        'spidy.common',
        'spidy.document',
        'spidy.language'
    ])