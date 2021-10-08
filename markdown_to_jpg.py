import os
import shutil
from PIL import Image,ImageOps
import pdfkit
from markdown import markdown
import fitz
# import pyMuPdf
import cv2
import numpy as np

# input_filename = 'test.md'

# with open(input_filename, encoding='utf-8') as f:
#     text = f.read()

class MarkdownToJpg:
    def __init__(self,txt,cssfile='d:\\py\\test\\my.css',temp_dir='d:\\temp\\temp_dzxc'):
        self.txt=txt
        self.cssfile=cssfile.replace('\\','/')
        # print(self.cssfile)
        self.temp_dir=temp_dir

    def crop_margin_xy(self,img,crop_size=[34,22],page_one='no'):    
        ivt_image = ImageOps.invert(img)
        xy=list(ivt_image.getbbox())
        # print(xy)
        if page_one=='no':
            xy[0],xy[1],xy[2],xy[3]=0,xy[1]-crop_size[0],img.size[0],xy[3]+crop_size[1]
        else:
            xy[0],xy[1],xy[2],xy[3]=0,0,img.size[0],xy[3]+crop_size[1]
        return xy

    def md_to_png(self,width=1024):
        output_filename='htmlto_pdf.pdf'
        output_filename=os.path.join(self.temp_dir,output_filename)
        extensions = [ #根据不同教程加上的扩展
            'markdown.extensions.extra',
            'markdown.extensions.codehilite', #代码高亮扩展
            'markdown.extensions.toc',
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code',
        ]

        html = '''
        <!DOCTYPE html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1, minimal-ui">
                <title>linenum</title>
                <link rel="stylesheet" href="file:///{0}">
            </head>
            <body>
                <article class="markdown-body" style="width:{1}px;">
                    {2}
                </article>
            </body>
        </html>
        '''

        shutil.rmtree(self.temp_dir) 
        os.makedirs(self.temp_dir)
        text = markdown(self.txt, output_format='html',extensions=extensions)  # MarkDown转HTML
        html=html.format(self.cssfile,str(width),text)

        wkhtmltopdf = r'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'  # 指定wkhtmltopdf
        configuration = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf)


        options = {
            'encoding': 'utf-8',
            'enable-local-file-access': None
        }
        pdfkit.from_string(html, output_filename, configuration=configuration, options=options)  # HTML转PDF
        # pdfkit.from_file('test_h.html',output_filename, configuration=configuration, options=options)
        # os.startfile(output_filename)
        
        

        pdf=fitz.open(output_filename)
        for pg in range(0, pdf.pageCount):
            page = pdf[pg]
            # 设置缩放和旋转系数
            trans = fitz.Matrix(1.6, 1.6).preRotate(0)
            pm = page.getPixmap(matrix=trans, alpha=False)
            # 开始写图像
            pm.writePNG(os.path.join(self.temp_dir,str(pg) + ".png"))
            # pm.writeJPG('d:\\temp\\' + str(pg) + ".jpg")
        pdf.close()
        # os.remove(output_filename)

    def crop_and_merge(self):
        pics_srcs=[]
        for fn in os.listdir(self.temp_dir):
            if fn[-3:].lower()=='png':
                img=Image.open(os.path.join(self.temp_dir,fn))
                extrema = img.convert("L").getextrema()
                if extrema[0]!=255:
                    pics_srcs.append(os.path.join(self.temp_dir,fn))

        # crop_top,crop_bottom=35,35
        pics=[]
        total_high=0
        for id,pic in enumerate(pics_srcs):       
            if id==0:
                bg=Image.open(pic)
                bg_xy=self.crop_margin_xy(bg,crop_size=[20,20],page_one='yes')
                bg=bg.crop(bg_xy)
                total_high+=bg.size[1]
                pics.append(bg)
            else:
                cover=Image.open(pic)
                cover_xy=self.crop_margin_xy(cover,crop_size=[20,20],page_one='no')
                cover=cover.crop(cover_xy)
                # cover=cover.crop((0,crop_top,cover.size[0],cover.size[1]))
                # cover=cover.crop((0,0,cover.size[0],cover.size[1]-crop_bottom))
                total_high+=cover.size[1]
                pics.append(cover)
        
        # total_high=len(pics)*pics[0].size[1]-(crop_top+crop_bottom)*(len(pics)-1)
        # total_high=
        new_img=Image.new('RGB',(pics[0].size[0],total_high))
        y_cover=0
        for pic_cover in pics:        
            new_img.paste(pic_cover,(0,y_cover))
            y_cover+=pic_cover.size[1]
        
            # print(new_img.size)
        # new_img.show()
        # new_img.save(os.path.join(self.temp_dir,'merge.jpg'))
        return new_img

    def to_jpg(self):
        self.md_to_png(width=1024)
        jpg=self.crop_and_merge()
        print('正在删除临时文件……',end='')
        for fn in os.listdir(self.temp_dir):
            if fn[-3:].lower()!='jpg':
                os.remove(os.path.join(self.temp_dir,fn))
        print('完成\n')
        print('生成图片完成')
        return jpg
        

if __name__=='__main__':

    t='''
# 第一步：允许合理宣泄

当孩子闹情绪的时候，很多家长的内心诉求是：**赶紧想个办法**，立刻搞定。于是家长们会想要迅速地掌控局面，比如用一堆道理劝说、大声呵斥制止等，想让孩子听话。但这样做效果往往不好，孩子该闹还是闹，与家长僵持不下。而且这些被压抑的情绪会一直堵在孩子心里，影响心理健康。
更可行的方法是：沉住气，给孩子的情绪以充足的时间，同时琢磨孩子到底想要干什么。

# 第二步：表达关心，听孩子倾诉表达


    '''
    mdfile=MarkdownToJpg(txt=t,cssfile='d:\\py\\test\\my.css',temp_dir='d:\\temp\\temp_dzxc')
    jpg=mdfile.to_jpg()
    jpg.show()
    # mdfile.md_to_png(txt=t,width=1024,output_filename=output_filename)
    # mdfile.crop_and_merge()

    # img=Image.open('d:\\temp\\temp_dzxc\\3.png')
    # ivt=ImageOps.invert(img)
    # print(ivt.getbbox())
    

    # print(crop_margin_xy(img,crop_size=[20,20],page_one='no'))