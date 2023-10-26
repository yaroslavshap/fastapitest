import os
import time

import httpx

# URL адрес первого микросервиса (отправителя)
sender_url = "http://localhost:8000/send-images/"

# Путь к папкам с изображениями на сервере отправителя
folder1 = "/Users/aroslavsapoval/myProjects/images_grpc_1980/left"
folder2 = "/Users/aroslavsapoval/myProjects/images_grpc_1980/right"

async def send_images():
    try:
        # Получение списка файлов из папок
        files1 = os.listdir(folder1)
        files2 = os.listdir(folder2)

        # Проверка, что количество файлов в папках совпадает
        if len(files1) != len(files2):
            return {"message": "Mismatch in the number of files in folders."}

        total_time = 0

        async with httpx.AsyncClient() as client:
            # Организация цикла для отправки каждой пары изображений
            for filename1, filename2 in zip(files1, files2):
                file1_path = os.path.join(folder1, filename1)
                file2_path = os.path.join(folder2, filename2)

                # Отправляем пару изображений на второй сервер
                with open(file1_path, "rb") as file1, open(file2_path, "rb") as file2:
                    data = {"image_name": filename1, "image_name_2": filename2}  # Используем имя первого изображения для уникальности

                    start_time = time.time()  # Засекаем время передачи
                    response = await client.post(sender_url, files={"file1": file1, "file2": file2}, data=data)
                    end_time = time.time()  # Засекаем время завершения передачи
                    transfer_time = end_time - start_time
                    total_time += transfer_time

                    response_data = response.json()

                    if response.status_code == 200:
                        print(f"Images {filename1} and {filename2} sent successfully.")
                        print(f"время передачи этой пары изображений: {transfer_time} секунд.")
                        print("Ответ сервера:", response.text)  # Вывод ответа от сервера
                    else:
                        print(f"Error sending images {filename1} and {filename2}: {response.text}")

            print(f"Общее время передачи изображений: {total_time} секунд.")
    except Exception as e:
        print(f"Error sending images: {str(e)}")

if __name__ == "__main__":
    import asyncio

    asyncio.run(send_images())