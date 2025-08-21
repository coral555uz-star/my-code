import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QGridLayout, QScrollArea, QFrame
)
from PyQt5.QtCore import Qt

# 模拟芯片数据
chipData = [
    {"id": 1, "name": "STM32F407VET6", "type": "MCU微控制器", "manufacturer": "意法半导体", "package": "LQFP",
     "params": {"核心架构": "ARM Cortex-M4", "主频": "168MHz", "Flash": "512KB", "RAM": "192KB"}, "status": "可用"},
    {"id": 2, "name": "TMS320F28335", "type": "DSP数字信号处理器", "manufacturer": "德州仪器", "package": "LQFP",
     "params": {"核心架构": "C28x", "主频": "150MHz", "Flash": "512KB", "RAM": "68KB"}, "status": "可用"},
    {"id": 3, "name": "LPC1768FBD100", "type": "MCU微控制器", "manufacturer": "恩智浦", "package": "LQFP",
     "params": {"核心架构": "ARM Cortex-M3", "主频": "100MHz", "Flash": "512KB", "RAM": "64KB"}, "status": "禁用"},
    # ...可继续添加
]

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
            val = QLabel(v)
            val.setStyleSheet("color: #333;")
            row.addWidget(val, 1)
            layout.addLayout(row)
        status = QLabel(chip["status"])
        if chip["status"] == "可用":
            status.setStyleSheet("background:#E8F5E9; color:#4CAF50; border-radius:4px; padding:3px 8px;")
        else:
            status.setStyleSheet("background:#FFEBEE; color:#F44336; border-radius:4px; padding:3px 8px;")
        layout.addWidget(status)
        btns = QHBoxLayout()
        btns.addWidget(QPushButton("查看详情"))
        btns.addWidget(QPushButton("加入项目"))
        layout.addLayout(btns)
        self.setLayout(layout)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("芯片查询系统")
        self.resize(1200, 900)
        main_layout = QVBoxLayout(self)

        # 顶部
        header = QHBoxLayout()
        title = QLabel("芯片查询系统")
        title.setStyleSheet("font-size:24px; font-weight:bold; color:#2A5CAA;")
        header.addWidget(title, 1)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("输入芯片名称或型号...")
        self.search_input.textChanged.connect(self.update_results)
        header.addWidget(self.search_input, 2)
        main_layout.addLayout(header)

        # 筛选区
        filter_layout = QHBoxLayout()
        self.type_combo = QComboBox()
        self.type_combo.addItems(["", "MCU微控制器", "FPGA可编程芯片", "SoC系统芯片", "DSP数字信号处理器"])
        self.type_combo.currentIndexChanged.connect(self.update_results)
        filter_layout.addWidget(self.type_combo)
        self.manuf_combo = QComboBox()
        self.manuf_combo.addItems(["", "德州仪器", "意法半导体", "恩智浦", "微芯科技"])
        self.manuf_combo.currentIndexChanged.connect(self.update_results)
        filter_layout.addWidget(self.manuf_combo)
        self.pkg_combo = QComboBox()
        self.pkg_combo.addItems(["", "QFN", "BGA", "SOP", "LQFP"])
        self.pkg_combo.currentIndexChanged.connect(self.update_results)
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
            if t and chip["type"] != t:
                continue
            if m and chip["manufacturer"] != m:
                continue
            if p and chip["package"].upper() != p.upper():
                continue
            if keyword and keyword not in chip["name"].lower():
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
                self.grid.addWidget(ChipCard(chip), idx // 3, idx % 3)

    def reset_filters(self):
        self.type_combo.setCurrentIndex(0)
        self.manuf_combo.setCurrentIndex(0)
        self.pkg_combo.setCurrentIndex(0)
        self.search_input.clear()
        self.update_results()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())