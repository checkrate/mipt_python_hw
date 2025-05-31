import os
import argparse
from datetime import datetime
import cv2
from experiment_db import init_db, save_experiment
from tools.ml_model import MLModel
from tools.classic_model import ClassicModel
from tools.cnn_model import CNNModel
from utils.generator import BloodCellGenerator

def run_methods_on_image(image_path: str):
    """
    Загружает изображение по пути и запускает все три модели анализа клеток.

    Args:
        image_path: путь к изображению.

    Returns:
        tuple: результаты трёх методов (int, int, int).
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Не удалось загрузить изображение: {image_path}")

    ml_model = MLModel()
    classic_model = ClassicModel()
    cnn_model = CNNModel()

    m1 = ml_model.predict(image)
    m2 = classic_model.predict(image)
    m3 = cnn_model.predict(image)

    return m1, m2, m3

def generate_dataset(data_dir: str, output_dir: str, num_images: int):
    """
    Генерирует синтетический датасет с разметкой в формате YOLO.

    Args:
        data_dir: папка, где находятся subfolders "cells" и "backgrounds".
        output_dir: куда сохранять сгенерированные изображения и метки.
        num_images: количество изображений для генерации.
    """
    generator = BloodCellGenerator(data_dir)
    generator.create_dataset(output_dir, num_images)
    print(f"Сгенерировано {num_images} изображений в папке:\n  {output_dir}/images\n  {output_dir}/labels")

def save_single_experiment(image_path: str, m1: int, m2: int, m3: int):
    """
    Сохраняет результаты прогона на одном изображении в БД.

    Args:
        image_path: путь к реальному изображению.
        m1: результат первого метода.
        m2: результат второго метода.
        m3: результат третьего метода.
    """
    init_db()
    save_experiment(
        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        real_data_path=image_path,
        gen_params="",
        method1=m1,
        method2=m2,
        method3=m3
    )
    print("Результаты сохранены в БД.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Утилита для генерации датасета и/или прогона моделей на изображении."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Параметры для генерации датасета
    gen_parser = subparsers.add_parser("generate", help="Сгенерировать синтетический датасет с разметкой YOLO.")
    gen_parser.add_argument(
        "--data_dir",
        type=str,
        required=True,
        help="Папка, где находятся подпапки 'cells' и 'backgrounds'."
    )
    gen_parser.add_argument(
        "--output_dir",
        type=str,
        required=True,
        help="Папка для сохранения сгенерированных изображений и меток."
    )
    gen_parser.add_argument(
        "--num_images",
        type=int,
        required=True,
        help="Количество изображений для генерации."
    )

    # Параметры для прогона на одном изображении
    run_parser = subparsers.add_parser("run", help="Запустить прогон моделей на одном изображении.")
    run_parser.add_argument(
        "--image_path",
        type=str,
        required=True,
        help="Путь к изображению, на котором нужно запустить модели."
    )
    run_parser.add_argument(
        "--save_db",
        action="store_true",
        help="Сохранить результаты прогона в БД (по умолчанию просто выводит в консоль)."
    )

    args = parser.parse_args()

    if args.command == "generate":
        # Генерация датасета
        data_dir = args.data_dir
        output_dir = args.output_dir
        num_images = args.num_images

        os.makedirs(output_dir, exist_ok=True)
        generate_dataset(data_dir, output_dir, num_images)

    elif args.command == "run":
        # Прогон моделей на одном изображении
        image_path = args.image_path
        m1, m2, m3 = run_methods_on_image(image_path)
        print("Результаты прогона на изображении:")
        print(f"  MLModel:      {m1}")
        print(f"  ClassicModel: {m2}")
        print(f"  CNNModel:     {m3}")

        if args.save_db:
            save_single_experiment(image_path, m1, m2, m3)
