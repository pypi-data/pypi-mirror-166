from setuptools import setup, find_packages

setup(
    name='tb_rna_velo',
    version='0.4',
    license='TEST',
    author="RijeshShrestha",
    author_email='craaabby@gmail.com.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    keywords='example project',
    install_requires=[
        'anndata==0.8.0',
        'matplotlib==3.5.1',
        'pandas==1.4.1',
        'scikit_learn==1.1.2',
        'scipy==1.8.0',
        'scvelo==0.2.4',
        'seaborn==0.11.2',
        'tensorflow==2.9.1',
        'numpy==1.20'
    ]
)