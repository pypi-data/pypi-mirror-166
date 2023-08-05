from setuptools import setup, find_packages

classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: POSIX :: Linux",
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers"
]

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="firebase_dynamic_link_generator",
    version="1.0.1",
    author="Sufiyan Shaikh",
    author_email="sufiyan8shaikh@gmail.com	",
    description="Python client for Firebase Dynamic Links API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    maintainer="Sufiyan Shaikh",
    maintainer_email="sufiyan8shaikh@gmail.com",
    keywords=["firebase", "dynamic links", "url shortener", "dynamic link custom suffix"],
    url="https://github.com/zammy395/firebase-dynamic-link-generator",
    packages=find_packages(),
    classifiers=classifiers,
    install_requires=["requests", "oauth2client", "httplib2", "pycryptodome==3.10.1"],
    project_urls={
        'Bug Reports': 'https://github.com/zammy395/firebase-dynamic-link-generator/issues',
        'Source': 'https://github.com/zammy395/firebase-dynamic-link-generator',
    },

)