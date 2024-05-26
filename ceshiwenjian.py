import os
from mmseg.apis import init_model, inference_model, show_result_pyplot

# 配置文件路径和权重文件路径
config_path = 'configs/unet/unet-s5-d16_pspnet_4xb4-40k_rsDataset.py'
checkpoint_path = 'checkpoints/unet_40000.pth'

# 文件夹路径，包含要进行推理的所有图像文件
image_folder = r"E:\PycharmPrograms\seg-detection\mmsegmentation\dataset\CD\train\A"

# 输出文件夹路径，用于保存推理结果
output_folder = 'work_dirs/Unet/A/'
# 创建输出文件夹（如果不存在）
os.makedirs(output_folder, exist_ok=True)
# 从配置文件和权重文件构建模型
model = init_model(config_path, checkpoint_path, device='cuda:0')

# 遍历文件夹中的所有图像文件
for filename in os.listdir(image_folder):
    if filename.endswith('.tif'):
        img_path = os.path.join(image_folder, filename)
        result = inference_model(model, img_path)
        # 构建输出文件路径
        output_file = os.path.join(output_folder, f'{os.path.splitext(filename)[0]}.png')
        # 保存可视化结果到输出文件夹
        vis_image = show_result_pyplot(model, img_path, result, opacity=0.3, show=False, out_file=output_file)
        # print(f'Inference for {filename} done. Result saved as {output_file}')
