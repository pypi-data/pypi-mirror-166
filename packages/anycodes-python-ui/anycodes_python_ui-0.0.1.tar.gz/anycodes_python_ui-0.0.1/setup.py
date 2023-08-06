from setuptools import setup, find_packages

setup(
    name = "anycodes_python_ui",
    version = "0.0.1",
    keywords = ["python ui", "anycodes"],
    description = "Anycodes 在线编程 Python 运行时调试 UI",
    long_description = "Anycodes 在线编程 Python 运行时调试 UI",
    license = "MIT Licence",
    url = "https://www.anycodes.cn",
    author = "Anycodes",
    author_email = "service@anycodes.cn",
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = []
)