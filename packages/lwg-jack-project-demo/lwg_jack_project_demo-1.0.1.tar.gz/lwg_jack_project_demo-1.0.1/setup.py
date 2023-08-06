import setuptools

setuptools.setup(
    name='lwg_jack_project_demo',
    version='1.0.1',
    author='jacky',
    author_email='jacky@g.com',
    description='test Python packaging',
    url='https://www.baidu.com/',
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'requests'
    ]
)
