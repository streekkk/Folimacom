import os
import requests
from PySide6.QtCore import Qt, Slot, QDir
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, \
    QFileDialog, QGridLayout, QCheckBox
from helpers.center_window import center_window
from pathlib import Path
from helpers.zip_worker import unzip_file, remove_zip, zip_file
from helpers.search_for_images import search_for_images
from helpers.image_compressor_multithread import compress_images_multithread
from helpers.create_folder import create_folder
from helpers.move_file import move_file

basedir = os.path.dirname(__file__)
GITHUB_API_URL = "https://api.github.com/repos/streekkk/Folimacom/releases/latest"
LOCAL_VERSION_FILE = "version.txt"
UPDATE_ZIP = "update.zip"


class Folimacom_ui(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Folimacom')
        self.setWindowIcon(QIcon(os.path.join(basedir, 'icons/logo.png')))
        self.__init_ui()
        center_window(self)

    def __init_ui(self) -> None:
        self.setFixedSize(450, 400)
        self.msgBox = QMessageBox()

        self.warning_msg = QLabel()
        self.warning_msg.setObjectName("warning_msg")
        self.warning_msg.setWordWrap(True)
        self.warning_msg.setFixedSize(450, 30)

        self.tip_search = QLabel('Выберите файл:')
        self.tip_search.setFixedSize(110, 30)

        self.tip_zip = QLabel('Работа с ZIP:')
        self.tip_zip.setFixedSize(110, 30)

        self.img_path = QLineEdit()
        self.img_path.textChanged.connect(self.__show_tooltip)

        self.is_zip = QCheckBox(text="ZIP-архив")

        self.file_dialog_button = QPushButton('Обзор...')
        self.file_dialog_button.setFixedWidth(70)
        self.file_dialog_button.clicked.connect(self.__select_file)

        self.resume_button = QPushButton("Сжать")
        self.resume_button.setFixedWidth(100)
        self.resume_button.clicked.connect(self.__compress_process)

        self.page_layout = QVBoxLayout()
        self.page_layout.setContentsMargins(20, 0, 20, 0)
        self.page_layout.setSpacing(0)

        self.fields_layout = QVBoxLayout()
        self.fields_layout_inner_search = QGridLayout()
        self.fields_layout_inner_search.setSpacing(5)
        self.fields_layout_inner = QGridLayout()
        self.fields_layout_inner.setSpacing(10)
        self.fields_layout_inner.addWidget(self.tip_zip, 0, 0, Qt.AlignmentFlag.AlignLeft)
        self.fields_layout_inner.addWidget(self.is_zip, 0, 1, Qt.AlignmentFlag.AlignLeft)
        self.fields_layout_inner.addWidget(self.tip_search, 1, 0, Qt.AlignmentFlag.AlignLeft)
        self.fields_layout_inner.addLayout(self.fields_layout_inner_search, 1, 1, Qt.AlignmentFlag.AlignHCenter)
        self.fields_layout.addWidget(self.warning_msg, 1, Qt.AlignmentFlag.AlignHCenter)
        self.fields_layout.addLayout(self.fields_layout_inner)
        self.fields_layout.setSpacing(10)
        self.fields_layout_inner_search.addWidget(self.img_path, 1, 0, Qt.AlignmentFlag.AlignLeft)
        self.fields_layout_inner_search.addWidget(self.file_dialog_button, 1, 1, Qt.AlignmentFlag.AlignLeft)
        self.fields_layout.addWidget(self.resume_button, 1, Qt.AlignmentFlag.AlignHCenter)
        self.page_layout.addLayout(self.fields_layout)
        self.setLayout(self.page_layout)

    '''
    def __get_local_version(self) -> str:
        if not os.path.exists(LOCAL_VERSION_FILE):
            return "1.0.0"
        with open(LOCAL_VERSION_FILE, "r") as file:
            return file.read().strip()

    def __get_version(self) -> str:
        try:
            response = requests.get(GITHUB_API_URL, headers={"Accept": "application/vnd.github.v3+json"})
            data = response.json()
    '''

    def __select_file(self) -> None:
        if not os.path.exists(os.path.join(basedir, "helpers/search_history.txt")):
            file = open(os.path.join(basedir, "helpers/search_history.txt"), "w")
            file.close()
        with open(os.path.join(basedir, "helpers/search_history.txt"), 'r+') as file:
            default_path = file.read()
            if not os.path.exists(default_path):
                default_path = default_path.rsplit('/', maxsplit=1)[0]
            if self.is_zip.isChecked():
                self.img_path_url: str = QFileDialog.getOpenFileName(self, 'Выберите архив со скриншотами',
                                                                     default_path,
                                                                     filter='Архивы (*.zip)')[0]
            else:
                self.img_path_url: str = QFileDialog.getExistingDirectory(self, 'Выберите папку со скриншотами', default_path)
            self.img_path.setText(f'{self.img_path_url}')
            file.seek(0)
            file.write(self.img_path_url)


    def __format_path(self, img_path_url: str) -> Path:
        if not img_path_url.endswith('/') and not self.img_path_url.endswith('.zip'):
            img_path_url = f'{img_path_url}/'
        img_path = Path(img_path_url)
        return img_path

    def __show_tooltip(self) -> None:
        self.warning_msg.setText('Убедитесь, что в папке только те скрины, которые хотите сжать!')

    def __error_message(self, error_msg: str, msg_box: QMessageBox) -> None:
        msg_box.setWindowTitle("Ошибка!")
        msg_box.setText(error_msg)
        msg_box.setWindowIcon(QIcon(os.path.join(basedir, "icons/warning.png")))
        msg_box.show()

    @Slot(QMessageBox)
    def __success_message(self, msg_box: QMessageBox) -> None:
        msg_box.setWindowTitle("Успешно!")
        msg_box.setText("Сжатие произошло без ошибок!")
        msg_box.setWindowIcon(QIcon(os.path.join(basedir, "icons/right.png")))
        msg_box.show()

    def __compress_process(self) -> None:
        text = self.img_path.text()
        if text == "":
            self.__error_message(error_msg="Не выбран файл. Повторите попытку.", msg_box=self.msgBox)
        else:
            try:
                img_path = self.__format_path(img_path_url=text)
                folder_path = create_folder(img_path)
                new_img_path = move_file(old_path=img_path, new_path=folder_path)
                unzip_file(new_img_path)
                remove_zip(new_img_path)
                images_list = search_for_images(img_path=new_img_path.parent)
                compress_images_multithread(images_list=images_list)
                zip_file(source_dir=new_img_path)
            except Exception as e:
                self.__error_message(error_msg=f"Ошибка: {str(e)}", msg_box=self.msgBox)
            finally:
                self.__success_message(msg_box=self.msgBox)
