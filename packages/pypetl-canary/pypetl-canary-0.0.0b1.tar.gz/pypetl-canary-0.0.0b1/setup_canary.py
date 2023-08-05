from setuptools import setup, find_packages
  
with open("README.md", "r") as fh:
    description = fh.read()
  
setup(
    name="pypetl-canary",
    version="0.0.0-beta1",
    author="Asyraf N. Adianto",
    author_email="asyraf.adianto@renos.id",
    package_dir={'': '.'},
    packages=find_packages('.'),
    description="Python ETL Tools",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/asyraf-adianto/pypetl",
    license='MIT',
    python_requires='>=3.0',
    install_requires=[
        'pandas>=1.4.3',
        'petl>=1.7.11',
        'redshift-connector>=2.0.908',
        'psycopg2-binary>=2.9.3',
        'paramiko>=2.11.0',
        'sshtunnel>=0.4.0'
    ]
)