from setuptools import setup, find_packages

setup(
    name="safe_path_lib",
    version="0.1.0",
    author="Aarya",
    description="AI-based safe path detection library using camera vision",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "opencv-python",
        "numpy",
        "networkx"
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'run-safe-path=examples.run_example:main',
        ]
    },
)
