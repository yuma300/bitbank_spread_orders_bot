from setuptools import setup

setup(
    name="bbitbank_spread_orders_bot",
    version="0.0.1",
    #install_requires=["packageA"]
    dependency_links=[
      'git+https://github.com/bitbankinc/python-bitbankcc@<commit_hash>\#egg=python-bitbankcc',
    ],
    #packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    #py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')]
)
