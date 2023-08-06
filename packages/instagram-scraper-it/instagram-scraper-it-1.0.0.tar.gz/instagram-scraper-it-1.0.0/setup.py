from setuptools import setup

setup(
  name = 'instagram-scraper-it',         
  packages = ['instagram-scraper-it'],   
  version = '1.0.0',      
  license='The Unlicense',        
  description = 'The instagram-scraper-it can collect information related to the things like post date, images,followers,following,user data etc.',
  author = 'suresh p',                   
  author_email = 'suresh.pandiyan1@outlook.com',      
  url = 'https://github.com/sureshpandiyan1/instagram-scraper-it.git',   
  download_url = 'https://github.com/sureshpandiyan1/instagram-scraper-it/archive/refs/tags/v1.0.0.tar.gz',    
  keywords = ['instagram-scrapper,scraper,instagram,likes,stories,webscrap,instagram-api'],   
  install_requires=[
          'requests',
          'selenium',
          'time',
          'json',
          're',
          'datetime'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: The Unlicense (Unlicense)',
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)