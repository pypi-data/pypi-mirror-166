from setuptools import setup

setup(
    name = 'rnadecoder',
    version = '1.0.4',
    author = 'Rodrigo Forti',
    author_email = 'rodrigofort14@gmail.com',
    packages = ['rnadecoder'],
    description = "Use genetic code table as a basis for translating a strand of mRNA.",
    long_description = 'It uses the genetic code table as a basis for translating a strand of mRNA, thus generating the protein including its primary structure (Amino Acid Sequence)',
    url = 'https://github.com/FortiHub/rnadecoder',
    project_urls = {
        'Código fonte': 'https://github.com/FortiHub/rnadecoder',
        'Download': 'https://github.com/FortiHub/rnadecoder/archive/refs/heads/main.zip'
    },
    license = 'MIT',
    keywords = 'Decrypt based RNA code to protein.',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Portuguese (Brazilian)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Internationalization',
        'Topic :: Scientific/Engineering :: Physics'
    ]
)
