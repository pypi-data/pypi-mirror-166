import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="convrewriting",
    version="0.0.1",
    author="Cristina Muntean",
    author_email="cristina.muntean@isti.cnr.it",
    description="Question rewriting for conversational search based on unsupervised and supervised methods.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hpclab/adaptive-utterance-rewriting-conversational-search",
    classifiers=[
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.7',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # package_dir={"": "convrewriting"},
    packages=["convrewriting", "convrewriting.data", "convrewriting.supervised", "convrewriting.unsupervised"],
    python_requires=">=3.7",
    include_package_data=True
)