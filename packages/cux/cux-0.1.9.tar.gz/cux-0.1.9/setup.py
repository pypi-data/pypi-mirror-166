import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cux",
    version="0.1.9",  # Latest version .
    author="r2fscg",
    author_email="r2fscg@gmail.com",
    description="PLACEHOLDER",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/private_repo/yaya",
    packages=setuptools.find_packages(),
    package_data={"cux": ["data/*.txt", "data/*.csv"],},
    entry_points={
        "console_scripts": [
            "jql=cux.main:gate",
            "redo=cux.redo:entry",
            "check_intelligence=cux.main:check_intelligence_result",
            "display_it=cux.main:display_intelligence_time_periods",
            "nsqstatus=cux.nsqstatus:cli",
            "eloop=cux.jupytersql:eloop",
        ],
    },
    install_requires=["codefast>=0.4.9", "authc", "redis", "pandas", "pymysql"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
