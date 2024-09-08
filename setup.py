from setuptools import setup, find_packages

setup(
    name="click-migr",  # Replace with your package name
    version="0.1.0",
    description="Data Migrator For Clickhouse",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Tirth Patel",
    author_email="tirthpatel31082003@gmail.com",
    url="https://github.com/yourusername/my_project",
    packages=find_packages(),
    install_requires=[
        "clickhouse-connect",
        "dotenv",
        "argparse",
        "coloredlogs",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Specify Python versions supported
)
