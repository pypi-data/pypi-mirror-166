from setuptools import find_packages, setup

setup(
    name="HangmanLibrary",
    packages = find_packages(include=["HangmanLibrary"]),
    version="0.1.0",
    author="CitrusBoy",
    license="MIT",
    install_requires=["random",],
    setup_requires=["pytest-runner"],
    tests_require=["pytest==4.4.1"],
    download_url = "https://github.com/GuiOliv/HangmanLibrary/archive/refs/tags/0.1.0.tar.gz",
    )
