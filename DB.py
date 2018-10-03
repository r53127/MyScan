import sqlite3

from PyQt5.QtWidgets import QMessageBox
from openpyxl import load_workbook


class StudentDB():
    def __init__(self):
        self.initDB()

    def initDB(self):
        db_path = 'data/student.db'
        # 连接到SQLite数据库
        # 如果文件不存在，会自动在当前目录创建:
        self.conn = sqlite3.connect(db_path)
        # 创建一个Cursor:
        self.cursor = self.conn.cursor()
        # 执行一条SQL语句，创建user表:AUTOINCREMENT类型必须是主键
        self.cursor.execute(
            r'CREATE TABLE IF NOT EXISTS student (userid INTEGER  primary key AUTOINCREMENT ,stuid int,name varchar(20),gender varchar(4),classid varchar(20))')

    def importStuFromXLS(self, file):
        students = []
        wb = load_workbook(file)
        sheet = wb["Sheet1"]
        # A1格必须是“学号”两个字
        if sheet['A1'].value != '学号':
            QMessageBox.information(None, '提示', '这不是有效的学生库文件！')
            return False
        for row in sheet.rows:  # 使用rows属性，行内第一格从0开始
            student = {}
            # 跳过标题行
            if row[0].value == '学号':
                continue
            # 如果学号不是空
            if row[0].value is not None:
                student['学号'] = row[0].value
                student['姓名'] = row[1].value
                student['性别'] = row[2].value
                student['班级'] = row[3].value
                students.append(student)
        for stud in students:
            # 检查重复
            if self.checkData(stud['学号'], stud['班级']):
                QMessageBox.information(None, '提示', '该学生重复！' + str(stud['姓名'] + str(stud['学号'])) + str(stud['班级']))
                continue
            self.insertDB(stud['学号'], stud['姓名'], stud['性别'], stud['班级'])
        return True

    def insertDB(self, stuid, name, gender, classid):
        # 继续执行一条SQL语句，插入一条记录:
        insert_statement = r'insert into student (stuid,name,gender,classid) values (?,?,?,?)'
        self.conn.execute(insert_statement, (stuid, name, gender, classid))
        self.conn.commit()  # 修改类操作必须commit

    def checkData(self, stuid, classid):
        query_statement = r"select * from student where stuid='" + str(stuid) + "' and classid='" + str(classid) + "'"
        self.cursor.execute(query_statement)
        return self.cursor.fetchall()

    def closeDB(self):
        # 关闭Cursor:
        self.cursor.close()


class AnswerDB():
    @classmethod
    def importAnswerFromXLS(cls, file):
        answer = {}
        wb = load_workbook(file)
        sheet = wb["Sheet1"]
        # for i in range(2, sheet.max_row):
        #     answer[sheet["A%d" % i].value] = (sheet["B%d" % i].value, sheet['C%d' % i].value) ## 第一种方法：%字符串占位操作符
        if sheet['A1'].value != '题号':
            QMessageBox.information(None, '提示', '这不是有效的答案文件！')
            return None
        for row in sheet.rows:  # 第二种方法使用rows属性
            if row[0].value == '题号':
                continue
            if row[0].value is not None:
                answer[row[0].value] = (row[1].value, row[2].value)
        return answer

class ScanDB():
    pass

class ScoreDB():
    pass
