import setuptools
from fiter import __version__
#python ns.py sdist bdist_wheel
#python -m twine upload dist/*


setuptools.setup(
    name="fiter",
    version=__version__,
    license="MIT",
    author="VoidAsMad",
    author_email="voidasmad@gmail.com",
    description="문자열 포맷팅 라이브러리",
    long_description=open("README.md", "rt", encoding="UTF8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/VoidAsMad/fiter",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)