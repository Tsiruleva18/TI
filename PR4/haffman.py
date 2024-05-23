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

            # Подсчитываем частоты символов
            frequencies = Counter(text)

            # Создаем листовые узлы для каждого символа
            nodes = [Node(symbol=symbol, freq=freq) for symbol, freq in frequencies.items()]

            # Строим дерево Хаффмана
            while len(nodes) > 1:
                nodes = sorted(nodes, key=lambda node: node.freq)
                left = nodes.pop(0)
                right = nodes.pop(0)
                new_node = Node(left=left, right=right, freq=left.freq + right.freq)
                nodes.append(new_node)

            # Генерируем коды для символов
            root = nodes[0]
            code = {}

            def walk(node, path=''):
                if node.symbol is not None:
                    code[node.symbol] = path
                    return
                if node.left:
                    walk(node.left, path + '0')
                if node.right:
                    walk(node.right, path + '1')

            walk(root)

            # Создаем папку для сохранения результата
            current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            folder_name = os.path.join(os.getcwd(), current_time)
            os.makedirs(folder_name)

            # Сохраняем коды в JSON файл
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
    if result:
        print(f"Сгенерированный код Хаффмана сохранен в файле: {result}")
    else:
        print("Не удалось сгенерировать код Хаффмана.")
