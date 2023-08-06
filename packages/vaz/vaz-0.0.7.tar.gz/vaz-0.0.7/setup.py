import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='vaz',
    packages=['vaz'],
    version='0.0.7',
    license='MIT',
    description='Testing installation of Package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Saman Siadati',
    author_email='siadatisaman@gmail.com',
    url='https://github.com/samansiadati/vaz',
    project_urls={  # Optional
        "Bug Tracker": "https://github.com/samansiadati/vaz/issues"
    },
    install_requires=['pandas'],
    keywords=["pandas", "manipulation", "vaz"],
    classifiers=[  # https://pypi.org/classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Documentation',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',

    ],

    download_url="https://github.com/samansiadati/vaz/archive/refs/tags/vaz.tar.gz",
)

