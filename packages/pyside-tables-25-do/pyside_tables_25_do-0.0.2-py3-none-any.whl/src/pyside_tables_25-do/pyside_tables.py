import sqlite3
from PySide6.QtWidgets import QPushButton, QTableWidgetItem


class ExtraTableQt:
    """loads data from Sqlite3 database to the QTableWidgetItem tables with styled buttons
    Basic Usage

    >>> TableQt.loadtable(
            tablename = self.ui.tableWidget_39,
            column_num = [5],
            funccalled = [ self.department_update_page],
            sqlquery = "SELECT dep_name, dep_code, dep_level, dep_supirior, status FROM department",
    >>>     btn_name = ["update"], pathtodb = "mydatabase.db")

    """
    def loadtable(
            tablename: str,
            column_num: list,
            funccalled: list,
            sqlquery: str,
            btn_name: list[str],
            pathtodb: str,
            style_sheet: str = None) -> None:
        connection = sqlite3.connect(pathtodb)
        query = sqlquery
        result = connection.execute(query).fetchall()

        tablename.setRowCount(0)
        for row_number, row_data in enumerate(result):
            tablename.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                tablename.setItem(
                    row_number,
                    column_number,
                    QTableWidgetItem(
                        str(data)))
                for cn_num, b_name, func_called in zip(
                        column_num, btn_name, funccalled):
                    b_name = QPushButton(b_name)
                    if style_sheet is None:
                        pass
                    else:
                        b_name.setStyleSheet(f"{style_sheet}")
                    tablename.setCellWidget(row_number, cn_num, b_name)
                    b_name.clicked.connect(func_called)
