from setuptools import setup, find_packages

setup(
    name="sshm",
    version="0.1.0",
    description="AI-powered terminal assistant",
    python_requires=">=3.10",
    packages=find_packages(),
    install_requires=[
        "groq",
        "python-dotenv",
        "prompt_toolkit",
    ],
    entry_points={
        "console_scripts": [
            "sshm=sshm.main:main",
        ],
    },
)
