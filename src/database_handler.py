# -*- coding: UTF-8 -*-

import sqlite3

import os
from pathlib import Path


class 数据库处理器:
    def __init__(self, 数据库路径: str = None) -> None:
        if 数据库路径 is None:
            # 获取项目根目录
            项目根目录 = Path(__file__).parent.parent
            # 创建数据库目录
            数据库目录 = 项目根目录 / "database"
            数据库目录.mkdir(parents=True, exist_ok=True)
            # 设置数据库文件路径
            数据库路径 = str(数据库目录 / "竹影.sqlite")

        self.数据库 = sqlite3.connect(数据库路径)
        self.游标 = self.数据库.cursor()
        self.表名: str = "视频"

    def 创建表(self) -> int:
        try:
            self.游标.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {self.表名} (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    文件名 TEXT NOT NULL,
                    文件路径 TEXT NOT NULL,
                    转录文本 TEXT
                )
            """
            )
            self.数据库.commit()
            return 1
        except sqlite3.Error as e:
            print(f"创建表失败: {e}")
            return 0
        finally:
            self.游标.close()
            self.数据库.close()

    def 保存视频记录(self, 文件名: str, 文件路径: str, 转录文本: str = None) -> bool:
        try:
            self.游标.execute(
                f"""
                INSERT INTO {self.表名} (文件名, 文件路径, 转录文本)
                VALUES (?, ?, ?)
                """,
                (文件名, 文件路径, 转录文本),
            )
            self.数据库.commit()
            return True
        except sqlite3.Error as e:
            print(f"保存记录失败: {e}")
            return False

    def 获取视频记录(self, 文件路径: str = None) -> list:
        try:
            if 文件路径:
                self.游标.execute(
                    f"SELECT * FROM {self.表名} WHERE 文件路径 = ?", (文件路径,)
                )
                return self.游标.fetchone()
            else:
                self.游标.execute(f"SELECT * FROM {self.表名}")
                return self.游标.fetchall()
        except sqlite3.Error as e:
            print(f"获取记录失败: {e}")
            return []

    def 更新转录文本(self, 文件路径: str, 转录文本: str) -> bool:
        """更新视频的转录文本"""
        try:
            self.游标.execute(
                f"""
                UPDATE {self.表名}
                SET 转录文本 = ?
                WHERE 文件路径 = ?
                """,
                (转录文本, 文件路径),
            )
            self.数据库.commit()
            return True
        except sqlite3.Error as e:
            print(f"更新转录文本失败: {e}")
            return False
