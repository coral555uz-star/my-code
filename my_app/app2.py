import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QGridLayout, QScrollArea, QFrame
)
from PyQt5.QtCore import Qt
import pymysql


#MYSQL配置
MYSQL_CONFIG={
    'host':'127.0.0.1',
    'user':'root',
    'password':'123456',
    'database':'chip',
    'charset':'utf8mb4'
}

#数据库操作get
def get_conn():
    return pymysql.connect(**MYSQL_CONFIG)

#数据库操作init
def init_db():
    conn=get_conn()
    with conn.cursor() as cursor:
        cursor.execute('''USE chip;''')
    conn.commit()
    conn.close()

#数据库操作load2data
def load_data():
    conn=get_conn()
    data=[]
    with conn.cursor() as cursor:
        cursor.execute("SELECT chip_name, guo_chan, car_type, score, shipment, intro, chip_application, summary FROM chip_info")
        for chip_name, guo_chan, car_type, score, shipment, intro, chip_application, summary in cursor.fetchall():
            chip = {
                "id": 95,
                "name": chip_name,
                "guo_chan": guo_chan,
                "car_type": car_type,
                "params": {
                    'shipment': shipment,
                    "intro": intro,
                    "chip_application": chip_application,
                    "summary": summary
                }
            }
            data.append(chip)
    conn.close()
    return data


chipData = load_data()

class ChipCard(QFrame):
    def __init__(self, chip):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("QFrame { border: 1px solid #E0E0E0; border-radius: 8px; background: white; }")
        layout = QVBoxLayout()
        name = QLabel(chip["name"])
        name.setStyleSheet("font-weight: bold; font-size: 18px; color: #333;")
        layout.addWidget(name)
        for k, v in chip["params"].items():
            row = QHBoxLayout()
            row.addWidget(QLabel(f"{k}："), 0)
            val = QLabel(str(v))
            val.setStyleSheet("color: #333;")
            row.addWidget(val, 1)
            layout.addLayout(row)
        # status = QLabel(chip["status"])
        # if chip["status"] == "可用":
        #     status.setStyleSheet("background:#E8F5E9; color:#4CAF50; border-radius:4px; padding:3px 8px;")
        # else:
        #     status.setStyleSheet("background:#FFEBEE; color:#F44336; border-radius:4px; padding:3px 8px;")
        # layout.addWidget(status)
        btns = QHBoxLayout()
        btns.addWidget(QPushButton("查看详情"))
        btns.addWidget(QPushButton("更新内容"))
        layout.addLayout(btns)
        self.setLayout(layout)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("车身智能开闭室芯片查询系统")
        self.resize(1200, 900)
        main_layout = QVBoxLayout(self)

        # 顶部
        header = QHBoxLayout()
        title = QLabel("车身智能开闭室芯片查询系统")
        title.setStyleSheet("font-size:24px; font-weight:bold; color:#2A5CAA;")
        header.addWidget(title, 1)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("输入芯片名称或型号...")
        self.search_input.textChanged.connect(self.update_results)
        header.addWidget(self.search_input, 2)
        main_layout.addLayout(header)

        #增加查询按钮
        search_btn = QPushButton("查找")
        search_btn.clicked.connect(self.update_results)
        header.addWidget(search_btn)

        # 筛选区  待更新与sql系统的连接
        filter_layout = QHBoxLayout()
        self.type_combo = QComboBox()
        self.load_db_companies("brand_name", "chip_brand", self.type_combo)
        filter_layout.addWidget(self.type_combo)
        self.manuf_combo = QComboBox()
        self.load_db_companies("name", "chip_category", self.manuf_combo)
        filter_layout.addWidget(self.manuf_combo)
        self.pkg_combo = QComboBox()
        self.load_db_companies("chip_name", "chip_info", self.pkg_combo)
        filter_layout.addWidget(self.pkg_combo)
        reset_btn = QPushButton("重置")
        reset_btn.clicked.connect(self.reset_filters)
        filter_layout.addWidget(reset_btn)
        main_layout.addLayout(filter_layout)

        # 结果区
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.results_widget = QWidget()
        self.grid = QGridLayout(self.results_widget)
        self.scroll.setWidget(self.results_widget)
        main_layout.addWidget(self.scroll)
        self.update_results()

    def update_results(self):
        # 过滤数据
        keyword = self.search_input.text().strip().lower()
        t = self.type_combo.currentText()
        m = self.manuf_combo.currentText()
        p = self.pkg_combo.currentText()
        filtered = []

        for chip in chipData:
            # if t and chip["name"] != t:
            #     continue
            # if m and chip["id"] != m:
            #     continue
            if p and chip["name"].upper() != p.upper():
                continue
            if keyword and keyword not in chip["car_type"].lower():
                continue
            filtered.append(chip)
        # 清空并重新布局
        for i in reversed(range(self.grid.count())):
            w = self.grid.itemAt(i).widget()
            if w:
                w.setParent(None)
        if not filtered:
            self.grid.addWidget(QLabel("未找到匹配的芯片"), 0, 0)
        else:
            for idx, chip in enumerate(filtered):
                print(idx,chip)
                self.grid.addWidget(ChipCard(chip), idx // 4, idx % 4)

    def reset_filters(self):
        self.type_combo.setCurrentIndex(0)
        self.manuf_combo.setCurrentIndex(0)
        self.pkg_combo.setCurrentIndex(0)
        self.search_input.clear()
        self.update_results()

    def load_db_companies(self,key,table,combo):
        conn = get_conn()
        with conn.cursor() as cursor:
            sql=f"SELECT {key} FROM {table}"
            cursor.execute(sql)  # 假设company表有name字段
            results = cursor.fetchall()
            for row in results:
                combo.addItem(row[0])  # row[0]是公司名
        conn.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())