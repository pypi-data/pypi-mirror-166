import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='databiz',
    packages=['databiz'],
    version='0.0.2',
    license='MIT',
    description='Testing installation of Package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='DataBizx',
    author_email='databizx@gmail.com',
    url='https://github.com/databizx/databiz',
    project_urls={  # Optional
        "Bug Tracker": "https://github.com/databizx/databiz/issues"
    },
    install_requires=['pandas'],
    keywords=["pandas", "manipulation", "databiz"],
    classifiers=[  # https://pypi.org/classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Documentation',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',

    ],

    download_url="https://github.com/databizx/databiz/archive/refs/tags/databiz.tar.gz",
)
