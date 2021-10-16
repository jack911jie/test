import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)),'modules'))
import pics_fill
from PIL import Image,ImageDraw,ImageFont


def draw_gradient_rct(wh,colors,horizontal=(True,True,True),direction='vertical'):
    rct=pics_fill.FillGradient()
    w,h=wh[0],wh[1]
    img=Image.new('RGB',(w,h),'#ffffff')
    img=rct.fill_multi_gradient_rct_rgb(img=img,colors=colors,horizontal=horizontal,direction=direction)
    return img


if __name__=='__main__':
    # p=ColorTransfer()
    # clrs=p.get_multi_colors_by_hsl((255,255,136),(230,180,90),10)
    # rct=FillGradient()
    # # img=rct.draw_gradient_rct_rgb(200,500,'#fffdee','#ffad6a',30,horizontal=(True, True, True),direction='vertical')
    # img=Image.new('RGBA',(600,800),'#ffffff')
    # # img=rct.fill_gradient_rct_rgb(img,'#fffdee','#ffad6a',horizontal=(True, True, True),direction='vertical')
    # img=rct.fill_multi_gradient_rct_rgb(img,('#fffdee','#ffad6a','#fed32a'),horizontal=(True, True, True),direction='vertical')
    # img.show()
    img=draw_gradient_rct(wh=(600,780),colors=('#ffad6a','#ffad6a','#ff00ff'),direction='horizon')
    img.show()