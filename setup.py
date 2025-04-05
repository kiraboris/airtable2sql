from setuptools import setup, find_packages

setup(
    name="airtable2sql",
    version="1.0.0",
    author="Antton Alberdi",
    author_email="antton.alberdi@sund.ku.dk",
    description="Export Airtable bases into sql databases",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pandas",
        "requests",
        "pyairtable",
        "sqlalchemy"
    ],
    entry_points={
        "console_scripts": [
            "airtable2sql=airtable2sql.cli:main"
        ],
    },
    python_requires=">=3.12",
)
