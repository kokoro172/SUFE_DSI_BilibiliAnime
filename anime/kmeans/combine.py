import os
import matplotlib.pyplot as plt
from PIL import Image

# 定义文件夹路径和图像文件名列表
folder_path = "./"  # 本文件夹
image_files = ["kmeans_clusters1.png", "kmeans_clusters2.png", "kmeans_clusters3.png", "kmeans_clusters4.png"]

# 定义输出合成图片的保存路径和文件名
save_path = "./combined_image.png"

# 创建一个 2x2 的画布
fig, axes = plt.subplots(2, 2, figsize=(8, 8))

# 遍历图像文件列表
for i, image_file in enumerate(image_files):
    if i >= 4:
        break
    image_path = os.path.join(folder_path, image_file)

    # 打开图像文件并添加到对应的子图
    img = Image.open(image_path)
    ax = axes[i // 2, i % 2]
    ax.imshow(img)
    ax.axis('off')
    ax.text(0.5, -0.1, f"k={i+1}", transform=ax.transAxes, ha='center', fontsize=12)  # 添加图注，位于子图下方

# 调整子图之间的间距为0
fig.subplots_adjust(wspace=0, hspace=0)

# 保存合成的图像
plt.savefig(save_path)
plt.close()
