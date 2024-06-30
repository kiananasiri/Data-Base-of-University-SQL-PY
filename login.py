import sys
import qtpy
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox , QVBoxLayout, QStackedWidget
from PyQt5.QtGui import QPalette, QColor , QCursor
from PyQt5 import QtCore 
import mysql.connector
from mysql.connector import Error

class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login Form')
        self.resize(500, 120)
        
        # Set the background color to lilac
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(200, 162, 200))  # lilac color
        self.setPalette(palette)
        
        # Create a stacked widget to hold different pages--------------------------------------
        self.stacked_widget = QStackedWidget(self)
        
        # Login page widget --------------------------------------------------------------------------
        self.login_widget = QWidget()
        layout = QGridLayout(self.login_widget)


        label_name = QLabel('<font size="4"> Username </font>')
        self.lineEdit_username = QLineEdit()
        self.lineEdit_username.setPlaceholderText('Please enter your username')
        layout.addWidget(label_name, 0, 0)
        layout.addWidget(self.lineEdit_username, 0, 1)

        label_password = QLabel('<font size="4"> Password </font>')
        self.lineEdit_password = QLineEdit()
        self.lineEdit_password.setPlaceholderText('Please enter your password')
        self.lineEdit_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(label_password, 1, 0)
        layout.addWidget(self.lineEdit_password, 1, 1)

        button_admin = QPushButton('Admin Login')
        button_student = QPushButton('Student Login')
        button_professor = QPushButton('Professor Login')
        
        button_student.setStyleSheet("border: 3px solid '#231942';" 
                                     + 'border-radius: 10px;' 
                                     + 'font-size: 15px;' 
                                     + 'color: white;' 
                                     + 'padding: 25x 0;' 
                                     + 'margin: 15px 20px;}'
                                     + "*:hover{background: '#5E548E';}")
        button_professor.setStyleSheet("border: 3px solid '#231942';" 
                                     + 'border-radius: 10px;' 
                                     + 'font-size: 15px;' 
                                     + 'color: white;' 
                                     + 'padding: 25x 0;' 
                                     + 'margin: 15px 20px;}'
                                     + "*:hover{background: '#5E548E';}")
        button_admin.setStyleSheet("border: 3px solid '#231942';" 
                                     + 'border-radius: 10px;' 
                                     + 'font-size: 15px;' 
                                     + 'color: white;' 
                                     + 'padding: 25x 0;' 
                                     + 'margin: 15px 20px;}'
                                     + "*:hover{background: '#5E548E';}")
        button_admin.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        button_student.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        button_professor.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        button_admin.clicked.connect(self.check_admin_password)
        layout.addWidget(button_admin, 2, 0)

        button_student.clicked.connect(self.check_student_password)
        layout.addWidget(button_student, 2, 1)

        button_professor.clicked.connect(self.check_professor_password)
        layout.addWidget(button_professor, 2, 2)

        layout.setRowMinimumHeight(2, 75)
        
        
        # Add login widget to stacked widget
        self.stacked_widget.addWidget(self.login_widget)
        self.stacked_widget.setCurrentWidget(self.login_widget)

        # Set layout for main window
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)

        self.setLayout(layout)

    def create_connection(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='mydb',
                user='root',
                password='bonjour1'
            )
            if connection.is_connected():
                return connection
        except Error as e:
            msg = QMessageBox()
            msg.setText(f"Error while connecting to MySQL: {e}")
            msg.exec_()
            return None

    def check_admin_password(self):
        connection = self.create_connection()
        if connection:
            cursor = connection.cursor()
            query = "SELECT id FROM admin WHERE username = %s"
            cursor.execute(query, (self.lineEdit_username.text(),))
            result = cursor.fetchone()
            connection.close()

            msg = QMessageBox()
            if result:
                msg.setText('Admin Login Successful')
                msg.exec_()
                # Perform further actions after successful login
                self.login_action('admin', result[0])
                
            else:
                msg.setText('Incorrect Admin Username')
                msg.exec_()

    def check_student_password(self):
        connection = self.create_connection()
        if connection:
            cursor = connection.cursor()
            query = "SELECT ENROLLMENT_STID FROM STUDENT WHERE ENROLLMENT_STID = %s"
            cursor.execute(query, (self.lineEdit_username.text(),))
            result = cursor.fetchone()
            connection.close()

            msg = QMessageBox()
            if result:
                msg.setText('Student Login Successful')
                msg.exec_()
                # Perform further actions after successful login
                self.login_action('STUDENT', result[0])
                print(result[0])
                
            else:
                msg.setText('Incorrect Student Username')
                msg.exec_()

    def check_professor_password(self):
        connection = self.create_connection()
        if connection:
            cursor = connection.cursor()
            query = "SELECT PROF_ID FROM PROFESSOR WHERE PROF_ID = %s"
            cursor.execute(query, (self.lineEdit_username.text(),))
            result = cursor.fetchone()
            connection.close()

            msg = QMessageBox()
            if result:
                msg.setText('Professor Login Successful')
                msg.exec_()
                # Perform further actions after successful login
                self.login_action('PROFESSOR', result[0])
                
            else:
                msg.setText('Incorrect Professor Username')
                msg.exec_()

    def login_action(self, user_type, user_id):
    # Clear any previous pages from stacked widget
        while self.stacked_widget.count() > 1:
            self.stacked_widget.removeWidget(self.stacked_widget.widget(1))

        # Fetch user data from database based on user_type and user_id
        connection = self.create_connection()
        if connection:
            cursor = connection.cursor()
            if user_type == 'STUDENT':
                query = "SELECT * FROM STUDENT WHERE ENROLLMENT_STID = %s"
            elif user_type == 'PROFESSOR':
                query = "SELECT * FROM PROFESSOR WHERE PROF_ID = %s"
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()  # Assuming there's only one record for the ID

            # Close the database connection
            connection.close()

            if result:
                # Create a new widget to display user data
                user_page = QWidget()
                layout = QVBoxLayout(user_page)

                # Iterate over result columns and display data
                for col_index, col_value in enumerate(result):
                    label = QLabel(f"{cursor.description[col_index][0]}: {col_value}")
                    layout.addWidget(label)

                self.stacked_widget.addWidget(user_page)
                self.stacked_widget.setCurrentWidget(user_page)
            else:
                # Handle case where no data was found (though it shouldn't happen if login is successful)
                msg = QMessageBox()
                msg.setText('No data found for user ID.')
                msg.exec_()
        else:
            # Handle case where database connection failed
            msg = QMessageBox()
            msg.setText('Database connection failed.')
            msg.exec_()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = LoginForm()
    form.show()
    sys.exit(app.exec_())

