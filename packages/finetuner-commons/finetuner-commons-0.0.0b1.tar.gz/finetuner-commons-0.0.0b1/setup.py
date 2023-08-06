import os

from setuptools import find_packages, setup

# package version
__version__ = '0.0.0'
try:
    libinfo_py = os.path.join('__init__.py')
    libinfo_content = open(libinfo_py, 'r', encoding='utf8').readlines()
    version_line = [
        line.strip() for line in libinfo_content if line.startswith('__version__')
    ][0]
    exec(version_line)  # gives __version__
except FileNotFoundError:
    pass

if __name__ == '__main__':
    setup(
        name='finetuner-commons',
        packages=find_packages(include=['commons*']),
        version='0.0.0b1',
        include_package_data=True,
        description='The finetuner-commons package provides common functionality between core and client.',
        author='Jina AI',
        author_email='team-finetuner@jina.ai',
        url='https://github.com/jina-ai/finetuner.fit/',
        license='Proprietary',
        download_url='https://github.com/jina-ai/finetuner.fit/tags',
        long_description_content_type='text/markdown',
        zip_safe=False,
        setup_requires=['setuptools>=18.0', 'wheel'],
        install_requires=[
            'docarray[common]>=0.13.25',
            'rich>=12.4.4',
            'torchvision==0.13.0',
            'torch==1.12.0',
            'transformers==4.20.1',
            'jina-hubble-sdk>=0.15.2',
        ],
        python_requires='>=3.7.0',
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Intended Audience :: Education',
            'Intended Audience :: Science/Research',
            'Programming Language :: Python :: 3.8',
            'Environment :: Console',
            'Operating System :: OS Independent',
            'Topic :: Scientific/Engineering :: Artificial Intelligence',
        ],
        project_urls={
            'Source': 'https://github.com/jina-ai/finetuner.fit/',
            'Tracker': 'https://github.com/jina-ai/finetuner.fit/issues',
        },
        keywords=(
            'jina neural-search neural-network deep-learning pretraining '
            'fine-tuning pretrained-models triplet-loss metric-learning '
            'siamese-network few-shot-learning'
        ),
    )
