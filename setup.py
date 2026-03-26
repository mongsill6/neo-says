from setuptools import setup

setup(
    name="neo-says",
    version="1.0.0",
    description="A snarky CLI fortune teller for developers",
    py_modules=["neo_says"],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "neo-says=neo_says:main",
        ],
    },
    author="mongsill6",
    url="https://github.com/mongsill6/neo-says",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Games/Entertainment :: Fortune Cookies",
    ],
)
