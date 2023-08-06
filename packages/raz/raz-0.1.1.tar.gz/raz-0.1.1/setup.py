import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='raz',
    packages=['raz'],
    version='0.1.1',
    license='MIT',
    description='Testing installation of Package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Saman Siadati',
    author_email='siadatisaman@gmail.com',
    url='https://github.com/samansiadati/raz',
    project_urls={  # Optional
        "Bug Tracker": "https://github.com/samansiadati/raz/issues"
    },
    install_requires=['pandas'],
    keywords=["pandas", "manipulation", "raz"],
    classifiers=[  # https://pypi.org/classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Documentation',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',

    ],

    download_url="https://github.com/samansiadati/raz/archive/refs/tags/raz.tar.gz",
)

