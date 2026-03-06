"""
谋策智能体 - 独立知识库
Strategy Knowledge Base for MAO-Strategy Agent
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="strategy-knowledge-base",
    version="2.1.0",
    author="谋策智能体团队",
    author_email="",
    description="谋策智能体独立知识库 - 包含鬼谷子、孙子兵法、三十六计、资治通鉴、毛泽东思想的谋略知识体系",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chinjaneking/strategy-knowledge-base",
    packages=find_packages(),
    package_data={
        "strategy_knowledge": ["*.json"],
    },
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.9",
    install_requires=[
        # 纯数据包，无依赖
    ],
)
