from setuptools import setup, find_packages

setup(
    name="aoc2022",
    description="Evan Sultanik's Advent of Code 2022",
    url="https://github.com/esultanik/aoc2022",
    author="Evan Sultanik",
    version="1.0",
    packages=find_packages(exclude=['test']),
    python_requires='>=3.9',
    install_requires=[],
    entry_points={
        'console_scripts': [
            'aoc2022 = aoc2022.__main__:main'
        ]
    }
)
