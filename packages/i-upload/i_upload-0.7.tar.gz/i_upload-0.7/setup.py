import setuptools

setuptools.setup(
    name='i_upload',
    version='0.7',
    packages=setuptools.find_packages(),
    license='GPL-3.0',
    author='jack',
    author_email='kinginjack@gmail.com',
    description='an upload software',
    install_requires=['selenium', 'colorama', 'datetime', 'cryptography', 'webdriver-manager', 'termcolor', 'tinydb'],
    python_requires='>=3.8'
)
