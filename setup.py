from setuptools import setup, find_packages
setup(
    name='chatgpt_py',
    version='v0.4',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'chatgpt_cli=chatgpt_py.cli.chatgpt_cli:main',
        ],
    },
    requires=['openai', 'termios', 'sys', 'os', 'json', 'itertools']
)