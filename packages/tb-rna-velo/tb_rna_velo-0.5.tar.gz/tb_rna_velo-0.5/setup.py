from setuptools import setup, find_packages

setup(
    name='tb_rna_velo',
    version='0.5',
    license='TEST',
    author="RijeshShrestha",
    author_email='craaabby@gmail.com.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    keywords='example project',
    install_requires=[
        'anndata',
        'matplotlib',
        'pandas',
        'scikit_learn',
        'scipy',
        'scvelo',
        'seaborn',
        'tensorflow',
        'numpy==1.20'
    ]
)