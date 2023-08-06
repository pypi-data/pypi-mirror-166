from setuptools import setup, find_packages

setup(
	name="ml2ipa",
	version="0.0.4",
	description="A linguistic tool that generates IPA pronounciation for Malayalam words",
	author="Elaine Mary Rose",
	author_email="ammuelaine@gmail.com",
	url="https://github.com/erose311/ml2ipa",
	packages=find_packages(),
	install_requires=['mlphon', 'ml-to-en'],
	download_url="https://github.com/erose311/ml2ipa",
	license="MIT",
	classifiers=[
		"Intended Audience :: Developers",
		"Programming Language :: Python :: 3.9",
	]
)
