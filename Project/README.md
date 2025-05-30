## Описание проекта

Система для обнаружения и подсчёта клеток крови на изображениях с помощью трёх подходов:

1. Классический метод KMeans (MLModel).
2. Детектор кругов HoughCircles (ClassicModel).
3. Сверточная сеть YOLOv8 (CNNModel).

Есть генератор синтетических изображений с разметкой в формате YOLO и утилита для запуска экспериментов и сохранения результатов в SQLite.

---

## Структура проекта

```
.
├── experiment_db.py        # Работа с SQLite
├── run.py                  # Утилита генерации датасета и прогона моделей
├── requirements.txt        # Список зависимостей
├── README.md               # Текущий файл
├── src
│   ├── tools
│   │   ├── cnn_model.py     # YOLOv8 (CNN)
│   │   ├── classic_model.py # HoughCircles (Classic)
│   │   └── ml_model.py      # KMeans (ML)
│   └── utils
│       └── generator.py     # Генератор синтетических изображений и YOLO-разметки
├── test_data
│   ├── ...                # Клетки (PNG-файлы)
└── dataset                  # Сгенерированный датасет (images/ и labels/)
    ├── images
    └── labels
```

* `experiment_db.py` — работа с БД `results.db`: создание таблицы и сохранение результатов.
* `run.py` — две команды: `generate` (синтетика) и `run` (прогон трёх моделей на одном изображении).
* В папке `src/tools` — файлы с тремя классами моделей.
* В папке `src/utils/generator.py` — генератор синтетических изображений + YOLO-разметка.

---

## Краткая характеристика методов

1. **MLModel**:
   • KMeans-кластеризация (2 кластера) для сегментации клеток.
   • Морфологическая очистка, поиск контуров и фильтрация по площади.
   • Возвращает количество найденных контуров (клеток).

2. **ClassicModel**:
   • Конвертация в оттенки серого, размытие.
   • Детекция кругов HoughCircles.
   • Возвращает число найденных окружностей.

3. **CNNModel**:
   • Загружает веса YOLOv8 (файл `best.pt` в `src/tools/weights/`).
   • Изменяет размер до 640×640, прогоняет модель, суммирует bounding boxes.
   • Опционально позволяет дообучать YOLO на своём датасете (метод `train`).

4. **BloodCellGenerator**:
   • Создаёт фон из случайных фонов с бесшовным клонированием.
   • Накладывает случайное число клеток из `data/cells/`.
   • Сохраняет изображения и YOLO-разметку (папки `images/` и `labels/`).

---

## Примеры команд запуска

1. **Генерация синтетического датасета**

   ```bash
   python run.py generate \
     --data_dir ./data \
     --output_dir ./dataset/yolo \
     --num_images 500
   ```

   Результат: папки `dataset/yolo/images/` (PNG) и `dataset/yolo/labels/` (TXT).

2. **Прогон моделей на одном изображении (консоль)**

   ```bash
   python run.py run \
     --image_path ./dataset/val/images/img_00001.png
   ```

   Выводит результаты трёх моделей (число клеток).

3. **Прогон с сохранением в БД**

   ```bash
   python run.py run \
     --image_path ./dataset/val/images/img_00001.png \
     --save_db
   ```

   Сохраняет результаты в файл `results.db`.

  4. **Ссылка на запись работы программы**
  [text](https://drive.google.com/drive/folders/15C17YqaLiZGNEuFhUgpM6DXiUWomE8gI?usp=sharing)
