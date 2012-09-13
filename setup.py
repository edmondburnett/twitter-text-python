from setuptools import setup

setup(
    name='twitter-text-python',
    version='1.0',
    description='Tweet parser and formatter',
    long_description=open('README.rst').read(),
    author='Ivo Wetzel (fork by Ian Ozsvald)',
    author_email='',
    url='https://github.com/ianozsvald/twitter-text-python',
    license='GPL',
    py_modules=['ttp'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    classifiers=[
        'Environment :: Web Environment',
        # I don't know what exactly this means, but why not?
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
