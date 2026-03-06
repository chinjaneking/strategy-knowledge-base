"""
谋策智能体 - 独立知识库模块
Strategy Knowledge Base - Independent Knowledge Repository

Version: 2.1.0
Description: 包含鬼谷子、孙子兵法、三十六计、资治通鉴、毛泽东思想的谋略知识体系
"""

from .knowledge_manager import KnowledgeManager
from .wisdom_manager import WisdomManager

__version__ = "2.1.0"
__author__ = "谋策智能体团队"

__all__ = [
    "KnowledgeManager",
    "WisdomManager",
]
