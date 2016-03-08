from setuptools import setup

setup(
    name='instagram-text-python',
    version='2.0.0',
    description='Instagram Tweet parser and formatter',
    long_description="Extract @users, #hashtags and URLs (and unwind shortened links) from instagram captions and comments including entity locations, also generate HTML for output. Visit https://github.com/takumihq/instagram-text-python for examples.",
    author='Maintained by Takumi (previously twitter-text-python, which is maintained by Edmond Burnett (previously Ian Ozsvald; originally Ivo Wetzel))',
    author_email='itp@takumihq.com',
    url='https://github.com/takumihq/instagram-text-python',
    license='MIT',
    packages=['itp'],
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
