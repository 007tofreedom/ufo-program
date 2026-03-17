from setuptools import setup, find_packages

setup(
    name="ufo-program",
    version="0.1.0",                  # bump when you change things
    packages=find_packages(),
    install_requires=[
        "pygame",
        "requests",
        "colorama",
        "blessed",
        "beautifultable",
    ],
    entry_points={
        "console_scripts": [
            "ufo-program = ufo_interactive_super_advanced_disc_combined_with_api_realtime:main",
        ],
    },
    # optional but nice
    python_requires=">=3.8",
    description="ASCII UFO simulator for the terminal",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
