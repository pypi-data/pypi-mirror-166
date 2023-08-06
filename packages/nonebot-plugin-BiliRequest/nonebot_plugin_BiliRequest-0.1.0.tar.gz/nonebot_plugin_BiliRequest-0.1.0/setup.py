import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="nonebot_plugin_BiliRequest",
    version="0.1.0",
    author="Shadow403",
    author_email="anonymous_hax@foxmail.com",
    description="use bilibili uid join in group",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Shadow403/nonebot_plugin_BiliRequest.git",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)