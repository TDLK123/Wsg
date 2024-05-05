import json
from PyQt6.QtWidgets import QLineEdit,QFileDialog, QApplication, QMainWindow, QStackedWidget, QPushButton, QListWidget, QListWidgetItem, QLabel, QVBoxLayout, QWidget, QScrollArea, QDialog, QComboBox, QMessageBox
from PyQt6.QtGui import QPixmap
from PyQt6 import uic
from PyQt6.QtCore import Qt
import re

class Login(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/login.ui", self)

    # Bắt sự kiện click chuột vào nút login
        self.pushButton.clicked.connect(self.check_login)
    #Bắt sự kiện click chuột vào nút sign up
        self.pushButton_6.clicked.connect(self.showRegister)

    def check_login(self):
        # Lấy thông tin email và mật khẩu từ người dùng
        email = self.lineEdit.text()
        password = self.lineEdit_2.text()
        
        # Kiểm tra email và mật khẩu có được nhập hay không
        if not email: 
            msg_box.setText("Please enter your email or phone number!")
            msg_box.exec()
            return
        if not password:
            msg_box.setText("Please enter a password!")
            msg_box.exec()
            return
    
    # Kiểm tra email và mật khẩu có khớp với tài khoản admin hay không
        if email == "admin@example.com" and password == "admin":
            # Nếu đăng nhập thành công, chuyển sang giao diện chính (Main)
            self.close()
            mainPage.show()  
        else:
            # Nếu đăng nhập không thành công, hiển thị thông báo lỗi
            msg_box.setText("Incorrect email or password!")
            msg_box.exec()

    def showRegister(self):
        registerPage.show()
        self.close()

# Lớp chứa giao diện đăng ký
class Register(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/signup.ui", self)
        self.name = ""
        
        # Bắt sự kiện click chuột vào nút đăng ký
        self.pushButton.clicked.connect(self.Register)

        #Bắt sự kiện "đã có tài khoản" và chuyển sag trang đăng nhập
        self.pushButton_1.clicked.connect(self.showLoginPage)
    
    def Register(self):
        # Lấy thông tin email, username và mật khẩu từ người dùng
        self.name = self.lineEdit_3.text()
        email = self.lineEdit.text()
        password = self.lineEdit_2.text()
        
        # Kiểm tra các trường thông tin có được nhập hay không
        if not self.name:
            msg_box.setText("Please enter your name!")
            msg_box.exec()
            return
        if not email: 
            msg_box.setText("Please enter your email or phone number!")
            msg_box.exec()
            return
        if not password:
            msg_box.setText("Please enter a password!")
            msg_box.exec()
            return
        if not self.checkBox.isChecked():
            msg_box.setText("Please read and agree to the terms and conditions of The App!")
            msg_box.exec()
            return
        if not self.validate_password(password):
            msg_box.setText("Password must contain at least 8 characters, including uppercase, lowercase, numbers, and special characters.")
            msg_box.exec()
            return
        if not self.validate_email(email):
            msg_box.setText("Invalid email format!")
            msg_box.exec()
            return
  
        mainPage = mainwindowPage.stackedWidget.currentWidget()
        mainPage.label.setText(self.name)
        mainwindowPage.show()        
        self.close()

    def showLoginPage(self):
        loginPage.show()
        self.close()

    def validate_password(self, password):
        if len(password) < 8:  # Kiểm tra độ dài mật khẩu
            return False
        if not re.search('[a-z]', password):  # Kiểm tra có chứa ký tự thường trong mật khẩu hay không
            return False
        if not re.search('[A-Z]', password):  # Kiểm tra có chứa ký tự in hoa trong mật khẩu hay không
            return False
        if not re.search('[0-9]', password):  # Kiểm tra có chứa chữ số trong mật khẩu hay không
            return False
        if not re.search('[^a-zA-Z0-9]', password):  # Kiểm tra có chứa ký tự đặc biệt trong mật khẩu hay không
            return False
        return True  # Mật khẩu hợp lệ

    def validate_email(self, email):
        if '@' not in email:  # Kiểm tra xem có ký tự '@' trong email hay không
            return False
        return True  # Email hợp lệ
class ItemLoader:
    def __init__(self, json_file):
        with open(json_file, 'r', encoding='utf8') as file:
            self.data = json.load(file)

    def get_items(self):
        items = []
        for item in self.data:
            id = item['id']
            name = item['name']
            description = item['description']
            price = item['price']
            ingredients = item['ingredients']
            rating = item['rating']
            category = item['category']
            image_path = item['image']
            items.append((id, name, description, price, ingredients, rating, category, image_path))
        return items

    def update_items(self, items):
        updated_data = []
        existing_items = self.get_items()  # Lấy danh sách các mục hiện tại từ self.data

        for existing_item in existing_items:
            item_id = existing_item[0]
            # Tìm các mục trong danh sách cần cập nhật có cùng ID
            matching_items = [item for item in items if item[0] == item_id]

            if matching_items:
                updated_item = matching_items[0]  # Chỉ lấy một mục duy nhất nếu có nhiều mục khớp
            else:
                updated_item = existing_item  # Nếu không tìm thấy mục trong danh sách cần cập nhật, giữ nguyên mục hiện tại

            # Tạo một đối tượng mục mới với thông tin đã cập nhật và thêm vào danh sách updated_data
            updated_data.append({
                'id': updated_item[0],
                'name': updated_item[1],
                'description': updated_item[2],
                'price': updated_item[3],
                'ingredients': updated_item[4],
                'rating': updated_item[5],
                'category': updated_item[6],
                'image': updated_item[7]
            })

        with open('data.json', 'w') as file:
            json.dump(updated_data, file, indent=4)  # Ghi danh sách mục đã cập nhật vào tệp JSON

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.stackedWidget = QStackedWidget()
        self.setCentralWidget(self.stackedWidget)

        self.loadUiFiles()
        self.displays()
        self.resize(800, 500)

    def loadUiFiles(self):
        ui_files = ['ui/main.ui', 'ui/list.ui', 'ui/search.ui', 'ui/contact.ui']

        for ui_file in ui_files:
            widget = uic.loadUi(ui_file)
            self.stackedWidget.addWidget(widget)

        self.showMainPage()
        self.showItems()

    def displays(self):
        main_widget = self.stackedWidget.widget(0)
        main_widget.pushButton_2.clicked.connect(self.showListPage)
        main_widget.pushButton_4.clicked.connect(self.showSearchPage)
        main_widget.pushButton_5.clicked.connect(self.showContactPage)

        list_widget = self.stackedWidget.widget(1)
        list_widget.pushButton_6.clicked.connect(self.showMainPage)
        list_widget.pushButton_4.clicked.connect(self.showSearchPage)
        list_widget.pushButton_5.clicked.connect(self.showContactPage)

        search_widget = self.stackedWidget.widget(2)
        search_widget.pushButton_6.clicked.connect(self.showMainPage)
        search_widget.pushButton_2.clicked.connect(self.showListPage)
        search_widget.pushButton_5.clicked.connect(self.showContactPage)

        contact_widget = self.stackedWidget.widget(3)
        contact_widget.pushButton_6.clicked.connect(self.showMainPage)
        contact_widget.pushButton_4.clicked.connect(self.showSearchPage)
        contact_widget.pushButton_2.clicked.connect(self.showListPage)

        # # Kết nối comboBox với phương thức sortItems
        list_widget.comboBox.currentTextChanged.connect(self.sortItems)
#Kết nối phương thức tìm kiếm
        search_widget = self.stackedWidget.widget(2)  # Lấy widget của trang tìm kiếm từ stackedWidget
        search_widget.pushButton_7.clicked.connect(self.searchItems)  # Khi nhấn vào nút, thực hiện phương thức searchItems 
 
    def showMainPage(self):
        self.stackedWidget.setCurrentIndex(0)

    def showListPage(self):
        self.stackedWidget.setCurrentIndex(1)

    def showSearchPage(self):
        self.stackedWidget.setCurrentIndex(2)

    def showContactPage(self):
        self.stackedWidget.setCurrentIndex(3)

    def showItems(self):
        list_widget = self.stackedWidget.widget(1)
        scroll_area = list_widget.scrollArea
        scroll_content_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_content_widget)

        self.item_loader = ItemLoader('data.json')
        items = self.item_loader.get_items()

        for item in items:
            detail_widget = DetailWidget(item, self.item_loader)
            scroll_layout.addWidget(detail_widget)

        scroll_area.setWidget(scroll_content_widget)

    #Phương thức sắp xếp
    def sortItems(self, sort_ingredients):
        list_widget = self.stackedWidget.widget(1)
        scroll_area = list_widget.scrollArea
        scroll_content_widget = scroll_area.widget()
        scroll_layout = scroll_content_widget.layout()

        # Xóa các mục hiện có trong scroll_area
        while scroll_layout.count():
            child = scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Sắp xếp danh sách các mục
        items = self.item_loader.get_items()
        if sort_ingredients == 'Rating: Sắp xếp giảm dần':
            items.sort(key=lambda x: x[5], reverse=True)  # Sắp xếp theo rating từ cao xuống thấp
        elif sort_ingredients == 'Rating: Sắp xếp tăng dần':
            items.sort(key=lambda x: x[5])  # Sắp xếp theo rating từ thấp lên cao

        # Hiển thị danh sách đã sắp xếp
        for item in items:
            detail_widget = DetailWidget(item)
            scroll_layout.addWidget(detail_widget)

        scroll_area.setWidget(scroll_content_widget)

    # Phương thức tìm kiếm
    def searchItems(self):
        search_widget = self.stackedWidget.widget(2)  # Lấy widget của trang tìm kiếm từ stackedWidget
        line_edit = search_widget.lineEdit  # Lấy lineEdit từ widget trang tìm kiếm
        search_text = line_edit.text()  # Lấy văn bản tìm kiếm từ lineEdit

        found_items = []
        items = self.item_loader.get_items()  # Lấy danh sách các mục từ đối tượng ItemLoader

        for item in items:
            # Tìm kiếm theo tên (không phân biệt chữ hoa, chữ thường)
            if search_text.lower() in item[1].lower():
                found_items.append(item)

        msg_box = QMessageBox()  # Tạo một QMessageBox để hiển thị thông báo
        msg_box.setWindowTitle("Search Results")  # Đặt tiêu đề của hộp thoại thông báo

        # Hiển thị kết quả tìm kiếm
        if found_items:
            search_widget = self.stackedWidget.widget(2)  # Lấy widget của trang tìm kiếm từ stackedWidget
            scroll_area = search_widget.scrollArea  # Lấy scrollArea từ widget trang tìm kiếm
            scroll_content_widget = QWidget()  # Tạo một QWidget để chứa nội dung cuộn
            scroll_layout = QVBoxLayout(scroll_content_widget)  # Tạo một QVBoxLayout cho scroll_content_widget

            for item in found_items:
                detail_widget = DetailWidget(item, self.item_loader)  # Truyền thêm đối số item_loader
                scroll_layout.addWidget(detail_widget)

            scroll_area.setWidget(scroll_content_widget)  # Đặt scroll_content_widget làm nội dung cuộn của scroll_area
            self.stackedWidget.setCurrentIndex(2)  # Chuyển sang trang kết quả tìm kiếm trên stackedWidget
        else:
            # Hiển thị thông báo khi không tìm thấy kết quả
            msg_box.setText("No items found.")
            msg_box.exec()
#Lớp hiển thị các đối tượng được quản lý
class DetailWidget(QWidget):
    def __init__(self, item, item_loader):
        super().__init__()
        self.item = item
        self.item_loader = item_loader
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label_id = QLabel(f"ID: {item[0]}")
        self.label_name = QLabel(f"Name: {item[1]}")
        self.label_rating = QLabel(f"Rating: {item[5]}")
        pixmap = QPixmap(item[7])
        self.label_image = QLabel()
        self.label_image.setPixmap(pixmap)

        self.label_id.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_rating.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.label_image)
        layout.addWidget(self.label_id)
        layout.addWidget(self.label_name)
        layout.addWidget(self.label_rating)

        self.button_show_detail = QPushButton("Show Detail")
        layout.addWidget(self.button_show_detail)

        self.button_show_detail.clicked.connect(self.showDetail)
#Them nút chinh sửa cho mỗi đối tượng và keests nối tới phương thức chỉnh sửa
        self.button_edit = QPushButton("Edit")
        self.button_edit.clicked.connect(self.editItem)
        layout.addWidget(self.button_edit)
#Thêm nút xóa cho mỗi đối tượng và kết nối tới phương thức xóa
        self.button_delete = QPushButton("Delete")
        layout.addWidget(self.button_delete)
        self.button_delete.clicked.connect(self.deleteItem)

 
 #Phương thức hiển thị chi tiết thông tin của mỗi đối tượng
    def showDetail(self):
        list_widget = QListWidget()
        list_widget.addItem(f"ID: {self.item[0]}")
        list_widget.addItem(f"Name: {self.item[1]}")
        list_widget.addItem(f"Description: {self.item[2]}")
        list_widget.addItem(f"Price: {self.item[3]}")
        list_widget.addItem(f"Ingredients: {self.item[4]}")
        list_widget.addItem(f"Rating: {self.item[5]}")
        list_widget.addItem(f"Category: {self.item[6]}")

        detail_dialog = QDialog(self)
        detail_dialog.setWindowTitle("Item Detail")
        detail_dialog.setFixedSize(300, 300)

        layout = QVBoxLayout(detail_dialog)
        layout.addWidget(list_widget)

        detail_dialog.exec()
    #Phương thức chỉnh sửa
    def editItem(self):
        edit_dialog = QDialog(self)
        edit_dialog.setWindowTitle("Edit Item")
        edit_dialog.setFixedSize(400, 400)

        layout = QVBoxLayout(edit_dialog)

        label_id = QLabel(f"ID: {self.item[0]}")
        layout.addWidget(label_id)

        label_name = QLabel("Name:")
        layout.addWidget(label_name)

        line_edit_name = QLineEdit(str(self.item[1]))
        layout.addWidget(line_edit_name)

        label_description = QLabel("Description:")
        layout.addWidget(label_description)

        line_edit_description = QLineEdit(str(self.item[2]))
        layout.addWidget(line_edit_description)

        label_Price = QLabel("Price:")
        layout.addWidget(label_Price)

        line_edit_Price = QLineEdit(str(self.item[3]))
        layout.addWidget(line_edit_Price)

        label_Ingredients = QLabel("Ingredients:")
        layout.addWidget(label_Ingredients)

        line_edit_Ingredients = QLineEdit(str(self.item[4]))
        layout.addWidget(line_edit_Ingredients)

        label_rating = QLabel("Rating:")
        layout.addWidget(label_rating)

        line_edit_rating = QLineEdit(str(self.item[5]))
        layout.addWidget(line_edit_rating)

        label_Category = QLabel("Category:")
        layout.addWidget(label_Category)

        line_edit_Category = QLineEdit(str(self.item[6]))
        layout.addWidget(line_edit_Category)

        button_upload_image = QPushButton("Upload Image")
        layout.addWidget(button_upload_image)

        button_upload_image.clicked.connect(lambda: self.uploadImage(line_edit_image))

        line_edit_image = QLineEdit()
        layout.addWidget(line_edit_image)

        button_save = QPushButton("Save")
        layout.addWidget(button_save)

        button_save.clicked.connect(lambda: self.saveItem(line_edit_name.text(),
                                                          line_edit_description.text(),
                                                          line_edit_Price.text(),
                                                          line_edit_Ingredients.text(),
                                                          line_edit_rating.text(),
                                                          line_edit_Category.text(),
                                                          line_edit_image.text(), edit_dialog))

        edit_dialog.exec()
#phương thức tải ảnh khi chỉnh sửa
    def uploadImage(self, line_edit_image):
        file_dialog = QFileDialog()  # Tạo QFileDialog để chọn file hình ảnh
        file_dialog.setDefaultSuffix('.png')  # Đặt phần mở rộng mặc định là .png
        file_dialog.setNameFilter("Images (*.png *.xpm *.jpg *.bmp *.gif)")  # Đặt bộ lọc để chỉ cho phép chọn các file hình ảnh

        if file_dialog.exec():  # Nếu người dùng chọn một file
            selected_files = file_dialog.selectedFiles()  # Lấy danh sách các file đã chọn
            line_edit_image.setText(selected_files[0])  # Hiển thị đường dẫn file trong QLineEdit
#Phương thức lưu các thông tin đã chỉnh sửa
    def saveItem(self, name, description, price, ingredients, rating, category, image, edit_dialog):
        self.item = (
            self.item[0],
            str(name),
            str(description),
            str(price),
            str(ingredients),
            float(rating),
            str(category),
            image
        )
        self.item_loader.update_items([self.item])
        self.label_id.setText(f"ID: {self.item[0]}")
        self.label_name.setText(f"Name: {self.item[1]}")
        self.label_rating.setText(f"Rating: {self.item[5]}")
        pixmap = QPixmap(self.item[7])
        self.label_image.setPixmap(pixmap)

        edit_dialog.close()

#Phương thức xóa đối tượng
    def deleteItem(self):
        confirm_dialog = QDialog(self)  # Tạo QDialog để xác nhận xóa mục
        confirm_dialog.setWindowTitle("Confirm Delete")  # Đặt tiêu đề cho QDialog
        confirm_dialog.setFixedSize(300, 100)  # Đặt kích thước cố định cho QDialog

        layout = QVBoxLayout(confirm_dialog)  # Tạo QVBoxLayout để chứa các phần tử trong QDialog

        label_message = QLabel("Are you sure you want to delete this item?")  # Tạo QLabel để hiển thị thông báo xác nhận xóa
        layout.addWidget(label_message)  # Thêm QLabel thông báo vào layout

        button_confirm = QPushButton("Confirm")  # Tạo QPushButton để xác nhận xóa
        layout.addWidget(button_confirm)  # Thêm QPushButton vào layout

        button_confirm.clicked.connect(lambda: self.confirmDelete(confirm_dialog))  # Kết nối sự kiện nhấp chuột cho QPushButton với phương thức confirmDelete

        confirm_dialog.exec()  # Hiển thị QDialog
   #Phương thức xác nhận xóa đối tượng 
    def confirmDelete(self, confirm_dialog):
        items = self.item_loader.get_items()  # Lấy danh sách các mục từ item_loader
        if self.item in items:  # Nếu mục hiện tại tồn tại trong danh sách
            items.remove(self.item)  # Xóa mục trong danh sách
            self.item_loader.update_items(items)  # Cập nhật thông tin mục trong item_loader
            self.setParent(None)  # Xóa QDialog cha của mục
            self.deleteLater()  # Xóa mục

        confirm_dialog.close()  # Đóng QDialog xác nhận xóa

if __name__ == '__main__':
    app = QApplication([])
    #Tạo các đối tượng tương ứng với các trang giao diện
    loginPage = Login()
    loginPage.show()
    registerPage = Register()
    mainwindowPage = MainWindow()
    # Thiết lập hộp thoại thông báo lỗi
    msg_box = QMessageBox()
    msg_box.setWindowTitle("Error")
    msg_box.setIcon(QMessageBox.Icon.Warning)
    msg_box.setStyleSheet("background-color: #F8F2EC; color: #356a9c")
    
    app.exec()
















































































    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    ()

            
    
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    #Tạo các đối tượng tương ứng với các trang giao diện
    loginPage = Login()
    loginPage.show()
    registerPage = Register()
    mainPage = Main()
    # Thiết lập hộp thoại thông báo lỗi
    msg_box = QMessageBox()
    msg_box.setWindowTitle("Error")
    msg_box.setIcon(QMessageBox.Icon.Warning)
    msg_box.setStyleSheet("background-color: #F8F2EC; color: #356a9c")
    
    app.exec()
