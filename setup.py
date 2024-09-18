from setuptools import setup, find_packages

setup(
    name='easybot_py',
    version='0.0.7',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'openai',
    ],
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