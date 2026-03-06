"""
静态知识库管理器
管理谋略理论体系（三十六计、鬼谷子、孙子兵法、毛泽东思想、资治通鉴）
"""

import json
import os
from typing import Dict, List, Any, Optional


class KnowledgeManager:
    """
    静态知识库管理器

    管理五大智慧体系：
    - 三十六计
    - 鬼谷子
    - 孙子兵法
    - 毛泽东思想
    - 资治通鉴
    """

    def __init__(self, library_path: Optional[str] = None):
        """
        初始化知识库管理器

        Args:
            library_path: 知识库JSON文件路径，默认为包内static_library.json
        """
        if library_path is None:
            # 默认使用包内的知识库
            base_dir = os.path.dirname(os.path.abspath(__file__))
            self.library_path = os.path.join(base_dir, "static_library.json")
        else:
            self.library_path = library_path

        self._data = None
        self._knowledge_base = None
        self._metadata = None
        self._load_data()

    def _load_data(self):
        """加载知识库数据"""
        try:
            with open(self.library_path, 'r', encoding='utf-8') as f:
                self._data = json.load(f)
            self._knowledge_base = self._data.get("knowledge_base", {})
            self._metadata = self._data.get("metadata", {})
        except Exception as e:
            raise RuntimeError(f"加载知识库失败: {e}")

    def reload(self):
        """重新加载知识库（支持热更新）"""
        self._load_data()

    # ==================== 基础查询 ====================

    def get_metadata(self) -> Dict[str, Any]:
        """获取知识库元数据"""
        return self._metadata.copy()

    def get_version(self) -> str:
        """获取知识库版本"""
        return self._metadata.get("version", "unknown")

    def list_sources(self) -> List[str]:
        """列出所有知识来源"""
        return list(self._knowledge_base.keys())

    def get_source_info(self, source: str) -> Dict[str, Any]:
        """
        获取指定来源的详细信息

        Args:
            source: 知识来源名称（三十六计/鬼谷子/孙子兵法/毛泽东思想/资治通鉴）

        Returns:
            来源详细信息字典
        """
        source_data = self._knowledge_base.get(source, {})
        return {
            "name": source,
            "description": source_data.get("description", ""),
            "source": source_data.get("source", ""),
            "category": source_data.get("category", ""),
            "tactics_count": len(source_data.get("core_tactics", {}))
        }

    # ==================== 谋略查询 ====================

    def get_tactic(self, source: str, tactic_name: str) -> Dict[str, Any]:
        """
        获取指定谋略的详细信息

        Args:
            source: 知识来源
            tactic_name: 谋略名称

        Returns:
            谋略详细信息
        """
        source_data = self._knowledge_base.get(source, {})
        tactics = source_data.get("core_tactics", {})
        return tactics.get(tactic_name, {})

    def list_tactics(self, source: str) -> List[str]:
        """
        列出指定来源的所有谋略

        Args:
            source: 知识来源

        Returns:
            谋略名称列表
        """
        source_data = self._knowledge_base.get(source, {})
        return list(source_data.get("core_tactics", {}).keys())

    def search_tactics(self, keyword: str) -> List[Dict[str, Any]]:
        """
        根据关键词搜索谋略

        Args:
            keyword: 搜索关键词

        Returns:
            匹配的谋略列表
        """
        results = []
        keyword_lower = keyword.lower()

        for source_name, source_data in self._knowledge_base.items():
            tactics = source_data.get("core_tactics", {})

            # 处理三十六计的特殊结构
            if source_name == "三十六计":
                for category, category_data in tactics.items():
                    category_tactics = category_data.get("tactics", {})
                    for tactic_name, tactic_info in category_tactics.items():
                        if self._match_keyword(keyword_lower, tactic_name, tactic_info):
                            results.append({
                                "source": source_name,
                                "category": category,
                                "name": tactic_name,
                                "info": tactic_info
                            })
            else:
                # 其他来源的标准结构
                for tactic_name, tactic_info in tactics.items():
                    if self._match_keyword(keyword_lower, tactic_name, tactic_info):
                        results.append({
                            "source": source_name,
                            "name": tactic_name,
                            "info": tactic_info
                        })

        return results

    def _match_keyword(self, keyword: str, name: str, info: Dict) -> bool:
        """检查关键词是否匹配"""
        if keyword in name.lower():
            return True
        # 搜索各个字段
        for value in info.values():
            if isinstance(value, str) and keyword in value.lower():
                return True
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, str) and keyword in item.lower():
                        return True
        return False

    # ==================== 系统提示词 ====================

    def get_system_prompt(self) -> str:
        """获取系统提示词模板"""
        return self._data.get("system_prompt_template", "")

    def get_error_cases(self) -> Dict[str, Any]:
        """获取错误案例库"""
        return self._data.get("error_cases", {})

    # ==================== 知识库导出 ====================

    def export_knowledge_base(self) -> Dict[str, Any]:
        """导出完整知识库（供原项目使用）"""
        return self._knowledge_base.copy()

    def get_thirtysix_stratagems(self) -> Dict[str, Any]:
        """获取三十六计完整内容"""
        return self._knowledge_base.get("三十六计", {})

    def get_guiguzi_tactics(self) -> Dict[str, Any]:
        """获取鬼谷子谋略"""
        return self._knowledge_base.get("鬼谷子", {})

    def get_sunzi_tactics(self) -> Dict[str, Any]:
        """获取孙子兵法谋略"""
        return self._knowledge_base.get("孙子兵法", {})

    def get_maozedong_tactics(self) -> Dict[str, Any]:
        """获取毛泽东思想方法论"""
        return self._knowledge_base.get("毛泽东思想", {})

    def get_historical_cases(self) -> Dict[str, Any]:
        """获取资治通鉴历史案例"""
        return self._knowledge_base.get("资治通鉴", {})

    # ==================== 知识库更新接口（供升级使用） ====================

    def add_tactic(self, source: str, tactic_name: str, tactic_data: Dict[str, Any]) -> bool:
        """
        添加新谋略（用于知识库升级）

        Args:
            source: 知识来源
            tactic_name: 谋略名称
            tactic_data: 谋略数据

        Returns:
            是否添加成功
        """
        if source not in self._knowledge_base:
            return False

        try:
            self._knowledge_base[source]["core_tactics"][tactic_name] = tactic_data
            self._save_data()
            return True
        except Exception as e:
            print(f"添加谋略失败: {e}")
            return False

    def update_tactic(self, source: str, tactic_name: str, tactic_data: Dict[str, Any]) -> bool:
        """
        更新现有谋略（用于知识库升级）

        Args:
            source: 知识来源
            tactic_name: 谋略名称
            tactic_data: 谋略数据

        Returns:
            是否更新成功
        """
        return self.add_tactic(source, tactic_name, tactic_data)

    def _save_data(self):
        """保存数据到文件"""
        try:
            with open(self.library_path, 'w', encoding='utf-8') as f:
                json.dump(self._data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"保存知识库失败: {e}")


# ==================== 便捷函数 ====================

def create_manager(library_path: Optional[str] = None) -> KnowledgeManager:
    """
    创建知识库管理器的便捷函数

    Args:
        library_path: 知识库文件路径

    Returns:
        KnowledgeManager实例
    """
    return KnowledgeManager(library_path)


def get_default_system_prompt() -> str:
    """获取默认系统提示词"""
    manager = KnowledgeManager()
    return manager.get_system_prompt()
