import os
import cv2
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog, QLabel, QVBoxLayout, QPushButton, QWidget, QComboBox
from augmentator import ImageAugmentor

class AugmentorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.augmentor = ImageAugmentor()
        self.images = []
        self.output_directory = ""

    def initUI(self):
        self.setWindowTitle("Image Augmentation Tool")
        self.layout = QVBoxLayout()

        self.dir_button = QPushButton("Select Dataset Directory")
        self.dir_button.clicked.connect(self.load_images)
        self.layout.addWidget(self.dir_button)

        self.method_label = QLabel("Select Augmentation Method:")
        self.layout.addWidget(self.method_label)

        self.method_selector = QComboBox()
        self.method_selector.addItems(["Add Noise", "Denoise", "Gaussian Blur", "Histogram Equalization", "Rotation", "Glass Effect", "Motion Blur"])
        self.layout.addWidget(self.method_selector)

        self.preview_label = QLabel("Preview Image:")
        self.layout.addWidget(self.preview_label)

        self.image_label = QLabel()
        self.image_label.setFixedSize(300, 300)
        self.layout.addWidget(self.image_label)

        self.apply_button = QPushButton("Apply Augmentation")
        self.apply_button.clicked.connect(self.apply_augmentation)
        self.layout.addWidget(self.apply_button)

        self.save_button = QPushButton("Select Output Directory")
        self.save_button.clicked.connect(self.select_output_directory)
        self.layout.addWidget(self.save_button)

        self.save_augmented_button = QPushButton("Save Augmented Images")
        self.save_augmented_button.clicked.connect(self.save_augmented_images)
        self.layout.addWidget(self.save_augmented_button)

        self.setLayout(self.layout)

    def load_images(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Dataset Directory")
        if folder:
            self.images = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
            if self.images:
                self.display_image(self.images[0])

    def display_image(self, image_path):
        pixmap = QtGui.QPixmap(image_path)
        pixmap = pixmap.scaled(300, 300, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)

    def apply_augmentation(self):
        method_name = self.method_selector.currentText()
        method = self.augmentor.methods[method_name]

        augmented_images = []
        for image_path in self.images:
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            if method_name == "Rotation":
                augmented_image = method(image, 45)  # Example angle
            elif method_name == "Glass Effect":
                augmented_image = method(image, 5)  # Example power
            elif method_name == "Motion Blur":
                augmented_image = method(image, 10, 45)  # Example degree and angle
            else:
                augmented_image = method(image)
            augmented_images.append((image_path, augmented_image))

        self.augmented_images = augmented_images

        if augmented_images:
            cv2.imwrite("preview.jpg", augmented_images[0][1])
            self.display_image("preview.jpg")

    def select_output_directory(self):
        self.output_directory = QFileDialog.getExistingDirectory(self, "Select Output Directory")

    def save_augmented_images(self):
        if not self.output_directory:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please select an output directory first.")
            return

        for original_path, augmented_image in self.augmented_images:
            filename = os.path.basename(original_path)
            save_path = os.path.join(self.output_directory, filename)
            cv2.imwrite(save_path, augmented_image)

        QtWidgets.QMessageBox.information(self, "Success", "Augmented images saved successfully.")

if __name__ == '__main__':
    import sys
    from PyQt5 import QtCore

    app = QtWidgets.QApplication(sys.argv)
    mainWin = AugmentorApp()
    mainWin.show()
    sys.exit(app.exec_())
