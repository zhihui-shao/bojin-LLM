from paddleocr import PPStructure, draw_structure_result, save_structure_res
import re
import datetime
import os
import cv2
from PIL import Image

import fitz  # fitz就是pip install PyMuPDF

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'


def pyMuPDF_fitz(pdfPath, imagePath):

    startTime_pdf2img = datetime.datetime.now()  # 开始时间

    print("imagePath=" + imagePath)
    pdfDoc = fitz.open(pdfPath)
    for pg in range(0, pdfDoc.page_count):
        page = pdfDoc[pg]
        rotate = int(0)
        # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
        # 此处若是不做设置，默认图片大小为：792X612, dpi=96
        zoom_x = 2  # (1.33333333-->1056x816)   (2-->1584x1224)
        zoom_y = 2
        mat = fitz.Matrix(zoom_x, zoom_y).prerotate(rotate)
        pix = page.get_pixmap(matrix=mat, alpha=False)

        if not os.path.exists(imagePath):  # 判断存放图片的文件夹是否存在
            os.makedirs(imagePath)  # 若图片文件夹不存在就创建

        pix._writeIMG(imagePath + '/' + 'images_%s.png' % pg, format=1)  # 将图片写入指定的文件夹内

    endTime_pdf2img = datetime.datetime.now()  # 结束时间
    print('pdf2img时间 =', (endTime_pdf2img - startTime_pdf2img).seconds)


def get_excel(save_folder, img_path):

    table_engine = PPStructure(show_log=True)

    img_files = os.listdir(img_path)
    for index in range(0, len(img_files)):
        img_file = img_path + img_files[index]
        img = cv2.imread(img_file)

        result = table_engine(img)
        save_structure_res(result, save_folder, os.path.basename(img_path).split('.')[0])


# if __name__ == "__main__":
#     # 1、PDF地址
#     pdfPath = r'../bs_challenge_financial_14b_dataset/pdf/3e0ded8afa8f8aa952fd8179b109d6e67578c2dd.PDF'
#     # 2、需要储存图片的目录
#     imagePath = './imgs/3e0ded8afa8f8aa952fd8179b109d6e67578c2dd'
#     pyMuPDF_fitz(pdfPath, imagePath)


if __name__ == "__main__":

    # 1、PDF地址
    pdfPath = r'../bs_challenge_financial_14b_dataset/pdf/'
    pdf_files = os.listdir(pdfPath)
    for index in range(0, len(pdf_files)):
        pdf_file = pdfPath + pdf_files[index]
        # 2、需要储存图片的目录
        image_path = './imgs/' + pdf_files[index].split('.')[0]
        pyMuPDF_fitz(pdf_file, image_path)
        # 你的文件结果目录
        save_folder = './excel/' + pdf_files[index].split('.')[0]
        # 输入的图片
        img_path = './imgs/' + pdf_files[index].split('.')[0] + '/'
        get_excel(save_folder, img_path)

