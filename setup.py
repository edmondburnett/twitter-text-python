from setuptools import setup

setup(
    name='twitter-text-python',
    version='1.1.1',
    description='Twitter Tweet parser and formatter',
    long_description="Extract @users, #hashtags and URLs (and unwind shortened links) from tweets including entity locations, also generate HTML for output. Visit https://github.com/edburnett/twitter-text-python for examples.",
    author='Maintained by Edmond Burnett (previously Ian Ozsvald; originally Ivo Wetzel)',
    author_email='_@edmondburnett.com',
    url='https://github.com/edburnett/twitter-text-python',
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
