from setuptools import setup, find_packages


setup(
    name='foscat',
    version='1.0.0',
    description='Synthesise 2D or Healpix data using Cross Scattering Transform' ,
    long_description='Synthesise data (2D or Healpix) using Cross Scattering Transform (https://arxiv.org/abs/2207.12527) usable for component separation (e.g. denoising).\n#startup\nTo generate test files run the follosing lines in python:\n>python\n>> import foscat.build_demo as dem\n>> dem.genDemo()\n>> quit()\n\n##run 2D test\n\n>python test2D.py\n\nto plot results\n>python test2Dplot.py\n##run Healpix test\n>python testHealpix.py\nto plot results\n>python testHplot.py\nNote: If mpi is availble you can run testHealpix_mpi.py that uses 3 nodes to do the same computation than tesHealpix.py' ,
    license='MIT',
    author='Jean-Marc DELOUIS',
    author_email='jean.marc.delouis@ifremer.fr',
    maintainer='Theo Foulquier',
    maintainer_email='theo.foulquier@ifremer.fr',
    packages=['foscat'],
    package_dir={'': 'src'},
    url='https://gitlab.ifremer.fr/deepsee/foscat',
    keywords=['Scattering transform','Component separation', 'denoising'],
    install_requires=[
          'imageio',
          'matplotlib',
          'numpy',
          'tensorflow-gpu',
          'healpy',
      ],

)
