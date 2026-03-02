from setuptools import setup, find_packages

setup(
    name="subtitler",
    version="1.0.0",
    description="Local AI-powered subtitle generator and translator",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "faster-whisper>=1.0.0",
        "argostranslate>=1.9.0",
        "pysrt>=1.1.2",
    ],
    entry_points={
        "console_scripts": [
            "subtitler=subtitler.cli:main",
        ],
    },
)
