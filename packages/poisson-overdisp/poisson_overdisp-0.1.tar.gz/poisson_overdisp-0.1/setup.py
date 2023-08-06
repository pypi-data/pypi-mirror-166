from distutils.core import setup

setup(name='poisson_overdisp',
      packages=['poisson_overdisp'],
      version='0.1',
      description='Overdispersion test for statsmodels poisson model',
      url='https://github.com/helderprado/overdisp.git',
      download_url='https://github.com/helderprado/overdisp/archive/refs/tags/0.1.tar.gz',
      author='Luiz Paulo Fávero',
      author_email='lpfavero@usp.br',
      keywords=['statsmodels', 'overdisp'],
      license='MIT',  # YOUR LICENSE HERE!

      install_requires=['statsmodels'],  # YOUR DEPENDENCIES HERE


      classifiers=[
          # "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',
          'License :: OSI Approved :: MIT License',  # Your License Here
          # List Python versions that you support Here
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
      ],
      )
