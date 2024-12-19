import csv
import cv2



class HistEncoder:
    @staticmethod
    def encode(file_path, data):
        raise NotImplementedError()

class CsvHistEncoder(HistEncoder):
    @staticmethod
    def encode(file_path, data):
        with open(file_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            for key, value in data.items():
                writer.writerow([key, value])

class ImageHistEncoder(HistEncoder):
    @staticmethod
    def encode(file_path, data):
        cv2.imwrite(file_path, data)



