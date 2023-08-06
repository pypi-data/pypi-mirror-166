from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='ExtremePluginManager',
    version='1.0.0',
    packages=['ExtremePluginManager'],
    url='https://github.com/CPSuperstore/ExtremePluginManager',
    license='MIT Licence',
    author='CPSuperstore',
    author_email='cpsuperstoreinc@gmail.com',
    description='A powerful library for managing plugins in your Python application.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        "Bug Tracker": "https://github.com/CPSuperstore/ExtremePluginManager/issues",
    },
    keywords=['Plugin', 'Manager'],
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Topic :: Desktop Environment',
        'Topic :: Games/Entertainment',
        'Topic :: Software Development',
        'Topic :: Utilities'
    ]
)
