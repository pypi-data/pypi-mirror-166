from setuptools import setup, find_packages

requrements = []
with open('src/tb_rna_velo/requirements.txt') as f:
        requrements = [line.replace('\n', '') for line in f.readlines()]

#print(requrements)



setup(
    name='tb_rna_velo',
    version='0.3',
    license='TEST',
    author="RijeshShrestha",
    author_email='craaabby@gmail.com.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    keywords='example project',
    install_requires=requrements
)