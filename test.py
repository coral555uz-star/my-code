from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLineEdit, QApplication

app = QApplication([])
window = QWidget()
layout = QHBoxLayout()

btn1 = QPushButton("按钮1")
edit = QLineEdit()
btn2 = QPushButton("按钮2")

layout.addWidget(btn1)
layout.addWidget(edit)
layout.addWidget(btn2)

window.setLayout(layout)
window.show()
app.exec_()