"""
动态智慧库管理器
管理从真实案例复盘中提取的实战经验
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional


class WisdomManager:
    """
    动态智慧库管理器

    管理从真实案例复盘中提取的实战经验
    支持增删改查、标签管理、相关性检索
    """

    def __init__(self, data_dir: Optional[str] = None):
        """
        初始化智慧库管理器

        Args:
            data_dir: 数据存储目录，默认为用户主目录下的.strategy_knowledge
        """
        if data_dir is None:
            # 默认保存在用户主目录下
            home_dir = os.path.expanduser("~")
            self.data_dir = os.path.join(home_dir, ".strategy_knowledge")
        else:
            self.data_dir = data_dir

        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        self.file_path = os.path.join(self.data_dir, "wisdom_library.json")
        self._init_file()

    def _init_file(self):
        """初始化智慧库文件"""
        if not os.path.exists(self.file_path):
            initial_data = {
                "metadata": {
                    "name": "谋策智能体动态智慧库",
                    "version": "2.1.0",
                    "description": "从真实案例复盘中提取的实战经验",
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                },
                "wisdoms": [],
                "tags_index": {}
            }
            self._save_data(initial_data)

    def _load_data(self) -> Dict[str, Any]:
        """加载智慧库数据"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"读取智慧库失败: {e}")
            return {"metadata": {}, "wisdoms": [], "tags_index": {}}

    def _save_data(self, data: Dict[str, Any]):
        """保存数据到智慧库"""
        try:
            # 更新最后修改时间
            if "metadata" in data:
                data["metadata"]["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                data["metadata"]["wisdom_count"] = len(data.get("wisdoms", []))

            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"写入智慧库失败: {e}")

    # ==================== 核心操作 ====================

    def add_wisdom(self,
                   original_question: str,
                   action_taken: str,
                   final_result: str,
                   extracted_wisdom: str,
                   tags: Optional[List[str]] = None,
                   category: Optional[str] = None) -> str:
        """
        添加一条新的实战智慧

        Args:
            original_question: 原决策问题
            action_taken: 实际采取的行动
            final_result: 最终结果
            extracted_wisdom: 提炼的智慧
            tags: 标签列表
            category: 分类（如商业、职场、投资等）

        Returns:
            智慧条目ID
        """
        data = self._load_data()

        # 生成ID
        wisdom_id = f"WD{len(data['wisdoms']) + 1:06d}"

        new_entry = {
            "id": wisdom_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "original_question": original_question,
            "action_taken": action_taken,
            "final_result": final_result,
            "extracted_wisdom": extracted_wisdom,
            "tags": tags or [],
            "category": category or "通用"
        }

        data["wisdoms"].append(new_entry)

        # 更新标签索引
        self._update_tags_index(data, wisdom_id, tags or [])

        self._save_data(data)
        return wisdom_id

    def _update_tags_index(self, data: Dict, wisdom_id: str, tags: List[str]):
        """更新标签索引"""
        if "tags_index" not in data:
            data["tags_index"] = {}

        for tag in tags:
            if tag not in data["tags_index"]:
                data["tags_index"][tag] = []
            if wisdom_id not in data["tags_index"][tag]:
                data["tags_index"][tag].append(wisdom_id)

    def get_wisdom(self, wisdom_id: str) -> Optional[Dict[str, Any]]:
        """
        获取指定ID的智慧条目

        Args:
            wisdom_id: 智慧条目ID

        Returns:
            智慧条目字典，不存在则返回None
        """
        data = self._load_data()
        for wisdom in data["wisdoms"]:
            if wisdom["id"] == wisdom_id:
                return wisdom
        return None

    def get_all_wisdoms(self,
                        category: Optional[str] = None,
                        tag: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        获取所有智慧条目，支持筛选

        Args:
            category: 按分类筛选
            tag: 按标签筛选

        Returns:
            智慧条目列表
        """
        data = self._load_data()
        wisdoms = data.get("wisdoms", [])

        if category:
            wisdoms = [w for w in wisdoms if w.get("category") == category]

        if tag:
            wisdoms = [w for w in wisdoms if tag in w.get("tags", [])]

        return wisdoms

    def update_wisdom(self, wisdom_id: str, **kwargs) -> bool:
        """
        更新智慧条目

        Args:
            wisdom_id: 智慧条目ID
            **kwargs: 要更新的字段

        Returns:
            是否更新成功
        """
        data = self._load_data()

        for wisdom in data["wisdoms"]:
            if wisdom["id"] == wisdom_id:
                for key, value in kwargs.items():
                    if key in wisdom and key != "id":
                        wisdom[key] = value
                self._save_data(data)
                return True

        return False

    def delete_wisdom(self, wisdom_id: str) -> bool:
        """
        删除智慧条目

        Args:
            wisdom_id: 智慧条目ID

        Returns:
            是否删除成功
        """
        data = self._load_data()

        original_count = len(data["wisdoms"])
        data["wisdoms"] = [w for w in data["wisdoms"] if w["id"] != wisdom_id]

        if len(data["wisdoms"]) < original_count:
            # 更新标签索引
            self._rebuild_tags_index(data)
            self._save_data(data)
            return True

        return False

    def _rebuild_tags_index(self, data: Dict):
        """重建标签索引"""
        data["tags_index"] = {}
        for wisdom in data["wisdoms"]:
            for tag in wisdom.get("tags", []):
                if tag not in data["tags_index"]:
                    data["tags_index"][tag] = []
                data["tags_index"][tag].append(wisdom["id"])

    # ==================== 搜索与检索 ====================

    def search_wisdoms(self, keyword: str) -> List[Dict[str, Any]]:
        """
        搜索智慧条目

        Args:
            keyword: 搜索关键词

        Returns:
            匹配的智慧条目列表
        """
        data = self._load_data()
        keyword_lower = keyword.lower()
        results = []

        for wisdom in data["wisdoms"]:
            # 搜索各个字段
            searchable_text = " ".join([
                wisdom.get("original_question", ""),
                wisdom.get("action_taken", ""),
                wisdom.get("final_result", ""),
                wisdom.get("extracted_wisdom", ""),
                wisdom.get("category", "")
            ] + wisdom.get("tags", []))

            if keyword_lower in searchable_text.lower():
                results.append(wisdom)

        return results

    def get_relevant_wisdom(self, question: str, limit: int = 3) -> str:
        """
        获取与问题相关的智慧（供智能体调用）

        Args:
            question: 当前问题
            limit: 返回条数限制

        Returns:
            格式化后的智慧文本
        """
        # 简单的关键词匹配
        data = self._load_data()
        wisdoms = data.get("wisdoms", [])

        if not wisdoms:
            return ""

        # 如果有关键词匹配，优先返回匹配的
        matching_wisdoms = self.search_wisdoms(question)

        if matching_wisdoms:
            relevant_wisdoms = matching_wisdoms[:limit]
        else:
            # 没有匹配则返回最新的
            relevant_wisdoms = sorted(wisdoms, key=lambda x: x["id"], reverse=True)[:limit]

        if not relevant_wisdoms:
            return ""

        formatted_wisdom = "\n【来自独立智慧库的历史实战经验启示（请务必参考以下教训优化你的分析）】\n"
        for w in relevant_wisdoms:
            formatted_wisdom += f"- {w['extracted_wisdom']}\n"

        return formatted_wisdom

    # ==================== 统计分析 ====================

    def get_statistics(self) -> Dict[str, Any]:
        """获取智慧库统计信息"""
        data = self._load_data()
        wisdoms = data.get("wisdoms", [])

        # 分类统计
        categories = {}
        tags_count = {}

        for wisdom in wisdoms:
            cat = wisdom.get("category", "未分类")
            categories[cat] = categories.get(cat, 0) + 1

            for tag in wisdom.get("tags", []):
                tags_count[tag] = tags_count.get(tag, 0) + 1

        return {
            "total_count": len(wisdoms),
            "categories": categories,
            "top_tags": sorted(tags_count.items(), key=lambda x: x[1], reverse=True)[:10],
            "last_updated": data.get("metadata", {}).get("last_updated", "未知")
        }

    def list_categories(self) -> List[str]:
        """列出所有分类"""
        stats = self.get_statistics()
        return list(stats["categories"].keys())

    def list_tags(self) -> List[str]:
        """列出所有标签"""
        data = self._load_data()
        return list(data.get("tags_index", {}).keys())

    # ==================== 导入导出 ====================

    def export_to_file(self, export_path: str) -> bool:
        """
        导出智慧库到指定文件

        Args:
            export_path: 导出文件路径

        Returns:
            是否导出成功
        """
        try:
            data = self._load_data()
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"导出失败: {e}")
            return False

    def import_from_file(self, import_path: str, merge: bool = True) -> bool:
        """
        从文件导入智慧

        Args:
            import_path: 导入文件路径
            merge: 是否合并（True则合并，False则覆盖）

        Returns:
            是否导入成功
        """
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)

            if merge:
                data = self._load_data()
                existing_ids = {w["id"] for w in data["wisdoms"]}

                for wisdom in import_data.get("wisdoms", []):
                    if wisdom["id"] not in existing_ids:
                        data["wisdoms"].append(wisdom)

                self._rebuild_tags_index(data)
                self._save_data(data)
            else:
                self._save_data(import_data)

            return True
        except Exception as e:
            print(f"导入失败: {e}")
            return False

    def clear_all(self, confirm: bool = False) -> bool:
        """
        清空所有智慧（危险操作）

        Args:
            confirm: 必须传入True才能执行

        Returns:
            是否清空成功
        """
        if not confirm:
            print("警告：清空操作需要 confirm=True 参数")
            return False

        data = self._load_data()
        data["wisdoms"] = []
        data["tags_index"] = {}
        self._save_data(data)
        return True
