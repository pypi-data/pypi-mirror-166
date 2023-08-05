from setuptools import setup, find_namespace_packages


def _read(filename: str) -> str:
    """
    Reads in the content of the file.

    :param filename:    The file to read.
    :return:            The file content.
    """
    with open(filename, "r") as file:
        return file.read()


setup(
    name="wai.annotations.coqui",
    description="Module with plugins for managing datasets for coqui.ai TTS and STT.",
    long_description=f"{_read('DESCRIPTION.rst')}\n"
                     f"{_read('CHANGES.rst')}",
    url="https://github.com/waikato-datamining/wai-annotations-coqui",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Programming Language :: Python :: 3',
    ],
    license='Apache License Version 2.0',
    package_dir={
        '': 'src'
    },
    packages=find_namespace_packages(where='src'),
    namespace_packages=[
        "wai",
        "wai.annotations"
    ],
    version="1.0.0",
    author='Peter Reutemann',
    author_email='fracpete@waikato.ac.nz',
    install_requires=[
        "wai.annotations.core>=0.1.8"
    ],
    entry_points={
        "wai.annotations.plugins": [
            # Speech Formats
            "from-coqui-stt-sp=wai.annotations.coqui.specifier:CoquiSTTInputFormatSpecifier",
            "from-coqui-tts-sp=wai.annotations.coqui.specifier:CoquiTTSInputFormatSpecifier",
            "to-coqui-stt-sp=wai.annotations.coqui.specifier:CoquiSTTOutputFormatSpecifier",
            "to-coqui-tts-sp=wai.annotations.coqui.specifier:CoquiTTSOutputFormatSpecifier",
        ]
    }
)
