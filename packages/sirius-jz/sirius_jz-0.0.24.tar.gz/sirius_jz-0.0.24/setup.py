from setuptools import setup
from pathlib import Path

curd = Path(__file__).parent

page_description = (curd / "README.md").read_text(encoding='utf-8')
setup(
    name='sirius_jz',
    version='0.0.24',
    author='LUIZ GUILHERME C S PADUA',
    author_email='jzguipadua@gmail.com',
    packages=['sirius_jz'],
    description='Sirius Studio for development',
    long_description=page_description,
    long_description_content_type='text/markdown',
    url='https://github.com/',
    project_urls={
        'Código fonte': 'https://github.com/',
        'Download': 'https://github.com/'
    },
    license='MIT',
    keywords='JackZafira Sirius Studio si Bifrost',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Portuguese (Brazilian)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Internationalization'
    ]
)
