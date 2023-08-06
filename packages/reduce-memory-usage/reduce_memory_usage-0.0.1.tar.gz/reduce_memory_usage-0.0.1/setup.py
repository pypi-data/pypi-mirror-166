import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='reduce_memory_usage',
    version='0.0.1',
    author='Taichi Nakabeppu',
    author_email='nakabepputaichi@gmail.com',
    description='Python scripts to reduce memory usage',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/nakabeppu/reduce_memory_usage.git',
    packages=setuptools.find_packages(),
    keywords='reduce, memory',
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)