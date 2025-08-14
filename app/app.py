import sys
import json
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QListWidget, QMessageBox, QInputDialog
)

DATA_FILE = "result.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

class ChipManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("芯片查询管理系统")
        self.resize(500, 400)
        self.data = load_data()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 搜索区
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("输入芯片名称关键词")
        search_btn = QPushButton("查找")
        search_btn.clicked.connect(self.search_chip)
        search_layout.addWidget(QLabel("查找："))
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_btn)
        layout.addLayout(search_layout)

        # 结果区
        self.result_list = QListWidget()
        layout.addWidget(self.result_list)

        # 增删改按钮区
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("添加")
        add_btn.clicked.connect(self.add_chip)
        del_btn = QPushButton("删除")
        del_btn.clicked.connect(self.delete_chip)
        edit_btn = QPushButton("修改")
        edit_btn.clicked.connect(self.edit_chip)
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(del_btn)
        btn_layout.addWidget(edit_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.refresh_list()

    def refresh_list(self, keyword=""):
        self.result_list.clear()
        for cid, items in self.data.items():
            for item in items:
                name = item.get("name", "")
                if not keyword or keyword in name:
                    self.result_list.addItem(f"分类ID:{cid}  名称:{name}")

    def search_chip(self):
        keyword = self.search_input.text().strip()
        self.refresh_list(keyword)

    def add_chip(self):
        cid, ok1 = QInputDialog.getText(self, "添加芯片", "分类ID：")
        if not ok1 or not cid.strip():
            return
        name, ok2 = QInputDialog.getText(self, "添加芯片", "芯片名称：")
        if not ok2 or not name.strip():
            return
        cid = cid.strip()
        name = name.strip()
        if cid not in self.data:
            self.data[cid] = []
        self.data[cid].append({"name": name})
        save_data(self.data)
        self.refresh_list()
        QMessageBox.information(self, "提示", "添加成功！")

    def delete_chip(self):
        item = self.result_list.currentItem()
        if not item:
            QMessageBox.warning(self, "警告", "请先选择要删除的芯片")
            return
        text = item.text()
        cid = text.split("分类ID:")[1].split("  名称:")[0]
        name = text.split("名称:")[1]
        self.data[cid] = [i for i in self.data[cid] if i.get("name") != name]
        if not self.data[cid]:
            del self.data[cid]
        save_data(self.data)
        self.refresh_list()
        QMessageBox.information(self, "提示", "删除成功！")

    def edit_chip(self):
        item = self.result_list.currentItem()
        if not item:
            QMessageBox.warning(self, "警告", "请先选择要修改的芯片")
            return
        text = item.text()
        cid = text.split("分类ID:")[1].split("  名称:")[0]
        old_name = text.split("名称:")[1]
        new_name, ok = QInputDialog.getText(self, "修改芯片名称", "新名称：", text=old_name)
        if not ok or not new_name.strip():
            return
        for chip in self.data[cid]:
            if chip.get("name") == old_name:
                chip["name"] = new_name.strip()
                break
        save_data(self.data)
        self.refresh_list()
        QMessageBox.information(self, "提示", "修改成功！")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ChipManager()
    win.show()
    sys.exit(app.exec_())