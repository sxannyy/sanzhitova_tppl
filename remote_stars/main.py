import socket
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops

def recvall(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            raise ConnectionError("Не удалось подключиться")
        data.extend(packet)
    return data

host = "84.237.21.36"
port = 5152
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host, port))
    plt.ion()

    for i in range(10):
        sock.send(b"get")
        data = recvall(sock, 40_002)

        try:
            image = np.frombuffer(data[2:], dtype="uint8")
            image = image.reshape(data[0], data[1])
            binary = (image >= np.max(image) * 0.8).astype(int)
            labeled = label(binary)
            regions = regionprops(labeled)

            if len(regions) == 2:
                centroid_0 = regions[0].centroid
                centroid_1 = regions[1].centroid

                d = round(np.linalg.norm(np.array(centroid_0) - centroid_1), 1)
                
                sock.send(f"{d}".encode())
                answer = sock.recv(6).decode()

                print("Картинка номер ", i + 1, "Дистанция между точками: ", d)

                plt.clf()
                plt.title(f"Картинка номер {i + 1} Дистанция между точками: {d}")
                plt.subplot(1, 2, 1)
                plt.imshow(image)
                plt.subplot(1, 2, 2)
                plt.imshow(labeled)
                plt.pause(0.5)
        
        except Exception as e:
            print(f"Не удалось обработать картинку {i + 1}: {e}")

        sock.send(b"beat")
        beat = sock.recv(6)

print("Программа завершена. Десять картинок обработаны!")