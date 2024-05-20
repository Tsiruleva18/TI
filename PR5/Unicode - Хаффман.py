import json
import os
import math

class Huffman:
    """
    Класс для кодирования и декодирования текстовых файлов с использованием кода Хаффмана.
    """
    def __init__(self):
        pass
    
    def encode(self, text_file, huffman_code_file, output_file):
        """
        Кодирует текстовый файл с использованием кода Хаффмана и сохраняет результат в бинарный файл.
        """
        # Загрузка кода Хаффмана из JSON файла
        with open(huffman_code_file, 'r', encoding='utf-8') as code_file:
            huffman_code = json.load(code_file)
        
        # Чтение текста из файла
        with open(text_file, 'r', encoding='utf-8') as file:
            text = file.read()
        
        # Кодирование текста
        encoded_text = ''.join([huffman_code[char] for char in text])
        
        # Запись закодированного текста в бинарный файл
        encoded_text = encoded_text + '0' * (8 - (len(encoded_text) % 8))
        encoded_bytes = bytearray([int(encoded_text[i*8:i*8+8], 2) for i in range(int(len(encoded_text) / 8))])
        with open(output_file, 'wb') as file:
            file.write(encoded_bytes)
        
        return encoded_text
    
    def decode(self, encoded_file, huffman_code_file, output_file):
        """
        Декодирует закодированный бинарный файл с использованием кода Хаффмана и сохраняет результат в текстовый файл.
        """
        # Загрузка кода Хаффмана
        with open(huffman_code_file, 'r', encoding='utf-8') as code_file:
            huffman_code = json.load(code_file)
        
       
        with open(encoded_file, 'rb') as file:
            encoded_bytes = file.read()
        
       
        encoded_text = ''.join(['{:0>8}'.format(str(bin(item))[2:]) for item in encoded_bytes])
        
        # Декодирование текста
        decoded_text = ''
        current_code = ''
        for bit in encoded_text:
            current_code += bit
            for char, code in huffman_code.items():
                if current_code == code:
                    decoded_text += char
                    current_code = ''
                    break
        
       
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(decoded_text)
        
        return decoded_text
    
    def get_file_size(self, file_path):
        """
        Возвращает размер файла в байтах.
        """
        return os.path.getsize(file_path)
    
    def calculate_entropy(self, text):
        """
        Рассчитывает энтропию текста.
        """
        frequency = {char: text.count(char) / len(text) for char in set(text)}
        return -sum(freq * math.log2(freq) for freq in frequency.values())

if __name__ == "__main__":
    encoder_decoder = Huffman()
    
    # Пример использования:
    text_file = input("Введите путь к текстовому файлу: ")
    huffman_code_file = input("Введите путь к файлу с кодом Хаффмана (JSON): ")
    encoded_file = input("Введите путь к закодированному файлу: ")
    output_file = input("Введите путь к выходному файлу (декодированный текст): ")
    
    encoded_text = encoder_decoder.encode(text_file, huffman_code_file, encoded_file)
    print(f"Закодированный текст сохранен в файле: {encoded_file}")
    
    decoded_text = encoder_decoder.decode(encoded_file, huffman_code_file, output_file)
    print(f"Декодированный текст сохранен в файле: {output_file}")
    
    original_file_size = encoder_decoder.get_file_size(text_file)
    encoded_file_size = encoder_decoder.get_file_size(encoded_file)
    entropy = encoder_decoder.calculate_entropy(decoded_text)
    
    print(f"Размер исходного файла: {original_file_size} байт")
    print(f"Размер закодированного файла: {encoded_file_size} байт")
    print(f"Энтропия исходного текста: {entropy}")
    print(f"Среднее количество бит на символ в закодированном файле: {encoded_file_size / len(encoded_text)}")
    print(f"Степень сжатия: {original_file_size / encoded_file_size}")