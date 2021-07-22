import os
import pdfkit
from markdown import markdown
import fitz
# import pyMuPdf

# input_filename = 'test.md'
output_filename = 'd:\\temp\\testdddddd.pdf'

# with open(input_filename, encoding='utf-8') as f:
#     text = f.read()

t='''
# 第一步：允许合理宣泄

当孩子闹情绪的时候，很多家长的内心诉求是：**赶紧想个办法**，立刻搞定。于是家长们会想要迅速地掌控局面，比如用一堆道理劝说、大声呵斥制止等，想让孩子听话。但这样做效果往往不好，孩子该闹还是闹，与家长僵持不下。而且这些被压抑的情绪会一直堵在孩子心里，影响心理健康。
更可行的方法是：沉住气，给孩子的情绪以充足的时间，同时琢磨孩子到底想要干什么。

# 第二步：表达关心，听孩子倾诉表达

情绪是人对外界情境的本能反应，本身并没有对错。孩子可以及时表达情绪很重要。既可以让家长及早了解到孩子的感受，又可以避免情绪的累积、缓解压力。
当孩子宣泄完、心情得以平复后，家长可以发挥同理心，引导并倾听孩子把情绪说出来，让孩子感受到有情绪是正常的，要坦然面对它。

# 第三步：发现情绪背后的力量并引导

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
        <link rel="stylesheet" href="file:///d:/py/test/my.css">
    </head>
    <body>
        <article class="markdown-body">
            {}
        </article>
    </body>
</html>
'''


text = markdown(t, output_format='html',extensions=extensions)  # MarkDown转HTML
# print(text)
html=html.format(text)
# print(html)
# pdfkit.from_string(html, output_filename, options={'encoding': 'utf-8'})  # HTML转PDF

wkhtmltopdf = r'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'  # 指定wkhtmltopdf
configuration = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf)


options = {
    'encoding': 'utf-8',
    'enable-local-file-access': None
}
# pdfkit.from_string(html, output_filename, configuration=configuration, options=options)  # HTML转PDF
# pdfkit.from_file('test_h.html',output_filename, configuration=configuration, options=options)
# os.startfile(output_filename)

pdf=fitz.open('d:\\temp\\testdddddd.pdf')
for pg in range(0, pdf.pageCount):
    page = pdf[pg]
    # 设置缩放和旋转系数
    trans = fitz.Matrix(1.3, 1.3).preRotate(0)
    pm = page.getPixmap(matrix=trans, alpha=False)
    # 开始写图像
    pm.writePNG('d:\\temp\\' + str(pg) + ".png")
    # pm.writeJPG('d:\\temp\\' + str(pg) + ".jpg")
pdf.close()