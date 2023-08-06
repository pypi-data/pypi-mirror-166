from setuptools import find_packages, setup

setup(
    name="HangmanLibrary",
    packages = find_packages(include=["HangmanLibrary"]),
    version="0.2.0",
    author="CitrusBoy",
    license="MIT",
    setup_requires=["pytest-runner"],
    tests_require=["pytest==4.4.1"],
    download_url = "https://github.com/GuiOliv/HangmanLibrary/archive/refs/tags/0.2.0.tar.gz",
    )
