from distutils.core import setup
setup(
  name = 'gptc',
  packages = ['gptc'],
  version = '2.0.0a',
  license='MIT',
  description = 'General-purpose English text classifier',
  author = 'ScoopGracie',
  author_email = 'scoopgracie@scoopgracie.com',
  url = 'https://github.com/scoopgracie/gptc',
  keywords = ['nlp', 'text', 'classification'],
  install_requires=[
          'spacy',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)
