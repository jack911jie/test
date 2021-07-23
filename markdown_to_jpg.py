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
output_filename = 'e:\\temp\\temp_dzxc\\testdddddd.pdf'

# with open(input_filename, encoding='utf-8') as f:
#     text = f.read()

t='''
# 第一步：允许合理宣泄

当孩子闹情绪的时候，很多家长的内心诉求是：**赶紧想个办法**，立刻搞定。于是家长们会想要迅速地掌控局面，比如用一堆道理劝说、大声呵斥制止等，想让孩子听话。但这样做效果往往不好，孩子该闹还是闹，与家长僵持不下。而且这些被压抑的情绪会一直堵在孩子心里，影响心理健康。
更可行的方法是：沉住气，给孩子的情绪以充足的时间，同时琢磨孩子到底想要干什么。

# 第二步：表达关心，听孩子倾诉表达

情绪是人对外界情境的本能反应，本身并没有对错。孩子可以及时表达情绪很重要。既可以让家长及早了解到孩子的感受，又可以避免情绪的累积、缓解压力。
当孩子宣泄完、心情得以平复后，家长可以发挥同理心，引导并倾听孩子把情绪说出来，让孩子感受到有情绪是正常的，要坦然面对它。

# 第三步：发现情绪背后的力量

负面情绪有不好的一面，但也有正向的力量。

比如：

* 在学校的亲子活动中，家长**看到别的孩子**做手工好，顺便夸了几句，自家的宝贝就嘟着小嘴一脸不开心。

* 当家长捕捉到孩子嫉妒的细节时，要避免责怪，可以引导孩子说出自己的感受。

* 在学校的亲子活动中，家长**看到别的孩子**做手工好，顺便夸了几句，自家的宝贝就嘟着小嘴一脸不开心。

* 当家长捕捉到孩子嫉妒的细节时，要避免责怪，可以引导孩子说出自己的感受。

* 在学校的亲子活动中，家长**看到别的孩子**做手工好，顺便夸了几句，自家的宝贝就嘟着小嘴一脸不开心。

* 当家长捕捉到孩子嫉妒的细节时，要避免责怪，可以引导孩子说出自己的感受。

* 在学校的亲子活动中，家长**看到别的孩子**做手工好，顺便夸了几句，自家的宝贝就嘟着小嘴一脸不开心。

* 当家长捕捉到孩子嫉妒的细节时，要避免责怪，可以引导孩子说出自己的感受。

* 在学校的亲子活动中，家长**看到别的孩子**做手工好，顺便夸了几句，自家的宝贝就嘟着小嘴一脸不开心。

* 当家长捕捉到孩子嫉妒的细节时，要避免责怪，可以引导孩子说出自己的感受。

* 在学校的亲子活动中，家长看到别的孩子做手工好，顺便*夸了几句*，自家的宝贝就嘟着小嘴一脸不开心。当家长捕捉到孩子嫉妒的细节时，要避免责怪，可以引导孩子说出自己的感受。
'''

def md_to_jpg(txt,width,output_filename):
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
            <link rel="stylesheet" href="file:///i:/py/test/my.css">
        </head>
        <body>
            <article class="markdown-body" style="width:{0}px;">
                {1}
            </article>
        </body>
    </html>
    '''

    shutil.rmtree('e:\\temp\\temp_dzxc')  
    os.makedirs('e:\\temp\\temp_dzxc')

    text = markdown(t, output_format='html',extensions=extensions)  # MarkDown转HTML
    # print(text)
    html=html.format(str(width),text)
    # print(html)
    # pdfkit.from_string(html, output_filename, options={'encoding': 'utf-8'})  # HTML转PDF
    # print(html)

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
        pm.writePNG('e:\\temp\\temp_dzxc\\' + str(pg) + ".png")
        # pm.writeJPG('d:\\temp\\' + str(pg) + ".jpg")
    pdf.close()
    os.remove(output_filename)

def crop_and_merge(png_dir='e:\\temp\\temp_dzxc'):
    pics_srcs=[]
    for fn in os.listdir(png_dir):
        if fn[-3:].lower()=='png':
            img=Image.open(os.path.join(png_dir,fn))
            extrema = img.convert("L").getextrema()
            if extrema[0]!=255:
                pics_srcs.append(os.path.join(png_dir,fn))

    crop_top,crop_bottom=35,65
    pics=[]
    for id,pic in enumerate(pics_srcs):       
        if id==0:
            bg=Image.open(pic)
            pics.append(bg)
        else:
            cover=Image.open(pic)
            cover=cover.crop((0,crop_top,cover.size[0],cover.size[1]))
            cover=cover.crop((0,0,cover.size[0],cover.size[1]-crop_bottom))
            pics.append(cover)
    
    total_high=len(pics)*pics[0].size[1]-(crop_top+crop_bottom)*(len(pics)-1)
    new_img=Image.new('RGB',(pics[0].size[0],total_high))
    y_cover=0
    for pic_cover in pics:        
        new_img.paste(pic_cover,(0,y_cover))
        y_cover+=pic_cover.size[1]
    
    print(new_img.size)
    new_img.show()

def crop_margin_xy(img,crop_size=[20,20],page_one='no'):    
    ivt_image = ImageOps.invert(img)
    xy=list(ivt_image.getbbox())
    if page_one=='no':
        xy[0],xy[1],xy[2],xy[3]=0,xy[1]-crop_size[0],img.size[0],xy[3]+crop_size[1]
    else:
        xy[0],xy[1],xy[2],xy[3]=0,0,img.size[0],xy[3]+crop_size[1]
    return xy
        
        
            
        


    

if __name__=='__main__':
    # md_to_jpg(txt=t,width=1024,output_filename=output_filename)
    # crop_and_merge()

    img=Image.open('E:\\temp\\temp_dzxc\\1.png')
    

    print(crop_margin_xy(img,crop_size=[20,20],page_one='no'))