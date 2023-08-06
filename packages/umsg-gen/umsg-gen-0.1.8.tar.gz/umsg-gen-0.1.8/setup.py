from setuptools import setup

setup(
    name='umsg-gen',
    version='0.1.8',
    author="Alex Pabouctsidis",
    author_email='alex.pabouct@gmail.com',
    url='https://github.com/Amcolex/umsg_gen.git',
    py_modules=['umsg_gen'],
    packages=['umsg_gen'],
    include_package_data=True,
    install_requires=[
        'jinja2',
    ],
    entry_points='''
        [console_scripts]
        umsg-gen=umsg_gen:main
    ''',
)