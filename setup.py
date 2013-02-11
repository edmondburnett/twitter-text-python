from setuptools import setup

setup(
    name='twitter-text-python',
    version='1.0.0.2',
    description='Twitter Tweet parser and formatter',
    long_description="Extract @users, #hashtags and URLs from tweets including entity locations, also generate HTML for output. Visit the github site for full instructions.",
    #open('README.rst').read(),
    author='Maintained by Ian Ozsvald (originally by Ivo Wetzel)',
    author_email='ian@ianozsvald.com',
    url='https://github.com/ianozsvald/twitter-text-python',
    license='MIT',
    packages=['ttp'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Linguistic',
    ]
)
