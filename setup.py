from setuptools import setup, find_packages

setup(
    name='easybot_py',
    version='0.0.4',
    packages=find_packages(),
    install_requires=[
        'openai',
    ],
    entry_points={
        'console_scripts': [
            'easybot_py=easybot_py.easybot_py:main',
        ],
    },
    author='Enrique Madrid',
    author_email='contact@nervess.cat',
    description='A library to help and facilitate the creation of bots and AI assistants',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/nervesscat/easy_bot',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
)