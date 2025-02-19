# -*- coding: UTF-8 -*-

import sqlite3


class 数据库处理器:
    def __init__(self, 数据库路径: str = "../database/竹影.sqlite"):
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
            return 0
        finally:
            self.游标.close()
            self.数据库.close()
