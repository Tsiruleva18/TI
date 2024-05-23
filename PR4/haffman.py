import os
import json
from collections import Counter
from datetime import datetime

class Node:
    """
    Класс Node для дерева Хаффмана.
    """
    def __init__(self, symbol=None, freq=None, left=None, right=None):
        self.symbol = symbol
        self.freq = freq
        self.left = left
        self.right = right
    def __lt__(self, other):
        return self.freq < other.freq
    def __eq__(self, other):
        return self.freq == other.freq
    def __ne__(self, other):
        return self.freq != other.freq

class CodeGenerator:
    """
    Генерирует коды Хаффмана для символов на основе их частотности.
    """
    def __init__(self):
        pass
    def gen_code(self, file_path):
        """
        Генерирует коды Хаффмана для символов на основе их частотности в заданном текстовом файле.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            letters = set(text)
            frequencies = [(text.count(letter), letter) for letter in letters]

            while len(frequencies) > 1:
                frequencies = sorted(frequencies, key=lambda x: x[0], reverse=True)
                first = frequencies.pop()
                second = frequencies.pop()
                freq = first[0] + second[0]
                frequencies.append((freq, Node(left=first[1], right=second[1])))
            root = frequencies[0][1]
            code = {}
            def walk(node, path=''):
                if isinstance(node, str):
                    code[node] = path
                    return
                walk(node.left, path + '0')
                walk(node.right, path + '1')
                walk(root)
            current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            folder_name = os.path.join(os.getcwd(), current_time)
            os.makedirs(folder_name)
            json_file_path = os.path.join(folder_name, "code.json")
            with open(json_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(code, json_file, ensure_ascii=False, indent=4)
            return json_file_path
        except Exception as e:
            print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    generator = CodeGenerator()
    file_path = input("Введите путь к текстовому файлу: ")
    result = generator.gen_code(file_path)
    print(f"Сгенерированный код Хаффмана сохранен в файле: {result}")
