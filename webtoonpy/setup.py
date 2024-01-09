#btw it is not reccomended to install
# if input("do you REALLY want to install this [y/N]:").lower() == "y":
from setuptools import setup, find_packages
setup(
    name="webtoonpy",
    version="0.0.2",
    license="MIT",
    description="a small lil' webtoon rapidapi api wrapper",
    author="hugie999",
    author_email="prefer not to say",
    url="https://github.com/hugie999/webtoon-api",
    packages=find_packages("webtoonpy",['testedoutputs.txt']),
    requires=["requests","base64"]
)