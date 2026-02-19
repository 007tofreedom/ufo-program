from setuptools import setup, find_packages

setup(
    name="ufo-program",
    version="1.0.0",
    description="ASCII UFO simulator for the terminal! Command an animated disc with pulsing lights, upgradable beam/hull/sensors, movable position, speed controls & toggleable energy beam (pygame sound). Scan to collect resources + fetch real UFO sightings from API (with fallback data). Retro-style TUI adventure built with blessed, colorama & more.",
    author="007tofreedom",
    license="MIT",
    packages=find_packages(),
    py_modules=["ufo_interactive_super_advanced_disc_combined_with_api_realtime"],
    install_requires=[
        "pygame>=2.1.0",
        "requests>=2.28.0",
        "colorama>=0.4.4",
        "blessed>=1.20.0",
        "beautifultable>=1.1.0",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "ufo-program=ufo_interactive_super_advanced_disc_combined_with_api_realtime:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Topic :: Games/Entertainment",
    ],
)