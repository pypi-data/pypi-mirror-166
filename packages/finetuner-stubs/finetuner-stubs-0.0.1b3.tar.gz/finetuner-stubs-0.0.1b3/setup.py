import os

from setuptools import setup

# package version
__version__ = '0.0.0'
try:
    libinfo_py = os.path.join(os.getcwd(), '../__init__.py')
    libinfo_content = open(libinfo_py, 'r', encoding='utf8').readlines()
    version_line = [
        line.strip() for line in libinfo_content if line.startswith('__version__')
    ][0]
    exec(version_line)  # gives __version__
except FileNotFoundError:
    pass

if __name__ == '__main__':
    setup(
        name='finetuner-stubs',
        packages=['stubs'],
        version='0.0.1b3',
        include_package_data=True,
        description='The finetuner-stubs package includes the interface of finetuner.runner.',
        author='Jina AI',
        author_email='team-finetuner@jina.ai',
        url='https://github.com/jina-ai/finetuner.fit/',
        license='Proprietary',
        download_url='https://github.com/jina-ai/finetuner.fit/tags',
        long_description_content_type='text/markdown',
        zip_safe=False,
        setup_requires=['setuptools>=18.0', 'wheel'],
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
