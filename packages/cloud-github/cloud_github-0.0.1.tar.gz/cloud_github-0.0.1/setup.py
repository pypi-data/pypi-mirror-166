from setuptools import setup, find_packages

setup(
    name='cloud_github',
    version='0.0.1',
    license='apache',
    author="WQ Yan",
    author_email='yan66665@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    keywords='github',
    install_requires=[
        'requests',
    ],
    description="Github rest API by python."
)
