import ast
import io
import re

from setuptools import setup, find_packages

with io.open('README.md', 'rt', encoding="utf8") as f:
    readme = f.read()

_description_re = re.compile(r'description\s+=\s+(?P<description>.*)')

with open('lektor_test.py', 'rb') as f:
    description = str(ast.literal_eval(_description_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    author='25349023',
    author_email='25349023.qq@gmail.com',
    description=description,
    keywords='Lektor plugin',
    license='MIT',
    long_description=readme,
    long_description_content_type='text/markdown',
    name='lektor-markdown-ruby-blocks',
    packages=find_packages(),
    py_modules=['lektor-markdown-ruby-blocks'],
    url='https://github.com/25349023/lektor-markdown-ruby-blocks',
    version='0.1.1',
    classifiers=[
        'Framework :: Lektor',
        'Environment :: Plugins',
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={
        'lektor.plugins': [
            'markdown-ruby-blocks = lektor_markdown_ruby_blocks:RubyBlockPlugin',
        ]
    }
)
