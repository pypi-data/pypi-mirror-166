from setuptools import setup, find_packages
setup(
        name='scGCO',
        version='1.1.2',
        description='single-cell graph cuts optimization',
        url='https://github.com/WangPeng-Lab/scGCO',
        packages=find_packages(),
        include_package_data=True,
        install_requires=['pandas','numpy','matplotlib','scipy','sklearn','seaborn','parmap','Cython','pygco',
                        'tqdm','networkx','shapely','statsmodels','hdbscan','pillow','scikit-image','umap-learn','pysal==2.0.0'],
        author='Peng Wang',
        author_email='wangpeng@pb.ac.cn',
        license='MIT'

)

## pip install numpy
## pip install pygco
## conda install -c conda-forge cython
## pip uninstall shapely && conda install -c r shapely   
