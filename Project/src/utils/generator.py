import os
import cv2
import numpy as np

class BloodCellGenerator:
    """Генератор синтетических изображений клеток крови с разметкой в формате YOLO."""
    def __init__(self, data_dir, image_size=(1024, 1024)):
        """Инициализация генератора с путями к данным и целевым размером изображения."""
        self.cells_dir = os.path.join(data_dir, "cells")
        self.backgrounds_dir = os.path.join(data_dir, "backgrounds")
        self.image_size = image_size
        self.cells = self._load_cells()
        self.backgrounds = self._load_backgrounds()

    def _load_cells(self):
        """Загружает изображения отдельных клеток."""
        images = []
        for fname in os.listdir(self.cells_dir):
            path = os.path.join(self.cells_dir, fname)
            img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
            if img is not None:
                images.append(img)
        return images

    def _load_backgrounds(self):
        """Загружает фоновые изображения и приводит их к заданному размеру."""
        images = []
        for fname in os.listdir(self.backgrounds_dir):
            path = os.path.join(self.backgrounds_dir, fname)
            img = cv2.imread(path)
            if img is not None:
                resized = cv2.resize(img, (500, 500))
                images.append(resized)
        return images

    def _generate_background(self):
        """Создает комбинированный фон через бесшовное клонирование."""
        base = self.backgrounds[np.random.randint(len(self.backgrounds))]
        canvas = cv2.resize(base, self.image_size)
        for _ in range(10):
            bg = self.backgrounds[np.random.randint(len(self.backgrounds))]
            mask = np.full_like(bg, 255)
            h, w = bg.shape[:2]
            center_y = np.random.randint(0, self.image_size[0])
            center_x = np.random.randint(0, self.image_size[1])
            h_up = center_y - h // 2
            h_down = center_y + h // 2
            w_left = center_x - w // 2
            w_right = center_x + w // 2

            if w_left < 0:
                bg = bg[:, -w_left:]
                mask = mask[:, -w_left:]
                center_x -= w_left // 2
                w = bg.shape[1]
            elif w_right > canvas.shape[1]:
                limit = canvas.shape[1] - w_right
                bg = bg[:, :limit]
                mask = mask[:, :limit]
                center_x += limit // 2
                w = bg.shape[1]
            else:
                w = bg.shape[1]

            if h_up < 0:
                bg = bg[-h_up:, :]
                mask = mask[-h_up:, :]
                center_y -= h_up // 2
                h = bg.shape[0]
            elif h_down > canvas.shape[0]:
                limit = canvas.shape[0] - h_down
                bg = bg[:limit, :]
                mask = mask[:limit, :]
                center_y += limit // 2
                h = bg.shape[0]
            else:
                h = bg.shape[0]

            center = (center_x, center_y)
            canvas = cv2.seamlessClone(bg, canvas, mask, center, cv2.MIXED_CLONE)
        return canvas

    def _generate_cells(self, canvas):
        """Размещает на фоне случайное число клеток и возвращает список их рамок."""
        bboxes = []
        count = np.random.randint(5, 30)
        for _ in range(count):
            cell = self.cells[np.random.randint(len(self.cells))]
            cell = cv2.resize(cell, (100, 100))
            if cell.shape[2] == 4:
                alpha = cell[:, :, 3] / 255.0
                rgb = cell[:, :, :3]
            else:
                alpha = np.ones((cell.shape[0], cell.shape[1]), dtype=float)
                rgb = cell

            h, w = rgb.shape[:2]
            y = np.random.randint(0, self.image_size[0] - h)
            x = np.random.randint(0, self.image_size[1] - w)
            alpha_lvl = np.random.uniform(0.6, 1.0)
            for c in range(3):
                canvas[y:y+h, x:x+w, c] = (
                    alpha_lvl * alpha * rgb[:, :, c] +
                    (1 - alpha_lvl * alpha) * canvas[y:y+h, x:x+w, c]
                ).astype(np.uint8)
            bboxes.append({"x": x, "y": y, "w": w, "h": h})
        return canvas, bboxes

    def generate_image(self, return_bboxes=False):
        """Создает одно синтетическое изображение и возвращает рамки клеток."""
        bg = self._generate_background()
        if return_bboxes:
            image, bboxes = self._generate_cells(bg)
            return image, bboxes
        image, _ = self._generate_cells(bg)
        return image

    def create_dataset(self, output_dir, num_images, class_id=0):
        """Генерирует набор изображений с YOLO-разметкой.

        Args:
            output_dir: Корневая папка для сохранения изображений и меток.
            num_images: Число изображений для генерации.
            class_id: Идентификатор класса (модель ожидает 0 по умолчанию).
        """
        images_dir = os.path.join(output_dir, "images")
        labels_dir = os.path.join(output_dir, "labels")
        os.makedirs(images_dir, exist_ok=True)
        os.makedirs(labels_dir, exist_ok=True)

        for idx in range(num_images):
            img, bboxes = self.generate_image(return_bboxes=True)
            img_name = f"img_{idx:05d}.png"
            img_path = os.path.join(images_dir, img_name)
            cv2.imwrite(img_path, img)

            label_name = f"img_{idx:05d}.txt"
            label_path = os.path.join(labels_dir, label_name)
            with open(label_path, "w") as f:
                for box in bboxes:
                    xc = (box["x"] + box["w"] / 2) / self.image_size[1]
                    yc = (box["y"] + box["h"] / 2) / self.image_size[0]
                    nw = box["w"] / self.image_size[1]
                    nh = box["h"] / self.image_size[0]
                    line = f"{class_id} {xc:.6f} {yc:.6f} {nw:.6f} {nh:.6f}\n"
                    f.write(line)
