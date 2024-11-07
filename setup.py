from setuptools import setup, find_packages

setup(
    name="flask-ezlogin",
    version="0.2.1",
    description="Easy login setup with Flask and Flask-Login",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Artur Arantes Santos da Silva",
    author_email="arturarantesads@gmail.com",
    url="https://github.com/arturads/flask-ezlogin",
    packages=find_packages(),
    install_requires=["Flask", "Flask-Login"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Flask",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
