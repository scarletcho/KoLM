from setuptools import setup
print('Setting up KoLM...')
setup(
    name = "kolm",
    version = "1.1.3",
    description = "Korean LM toolkit for building ASR system",
    author = "Yejin Cho",
    author_email = "scarletcho@gmail.com",
    keywords = "Korean Language Modeling Toolkit",
    url = "https://github.com/scarletcho/KoLM",
    packages = ['kolm'],
    install_requires = [
    	'JPype1',
    	'konlpy',
    	'korean',
    	'hanja'],
    dependency_links=['https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh'],
    include_package_data = True,
    package_data = {
        '': ['*.txt'],
    }
)
