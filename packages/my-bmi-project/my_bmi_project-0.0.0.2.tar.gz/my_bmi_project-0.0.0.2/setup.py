from setuptools import setup, find_packages

setup(
    name = 'my_bmi_project',
    version = '0.0.0.2',
    description = 'My bmi project',
    author = 'far_away',
    author_email = 'atker14@gmail.com',
    url = "https://www.naver.com",
    license = 'MIT',
    py_modules = ['calculate_bmi'],
    python_requires = '>=3',
    packages = ['my_bmi_project']
)