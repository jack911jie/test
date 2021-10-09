import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)),'modules'))
import pics_modify
import re
import json
from PIL import Image,ImageFont,ImageDraw
import logging
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(funcName)s-%(lineno)d - %(message)s')
logger = logging.getLogger(__name__)


class TxtFormat:
    def char_len(self,txt):
        len_s=len(txt)
        len_u=len(txt.encode('utf-8'))
        ziShu_z=(len_u-len_s)/2
        ziShu_e=len_s-ziShu_z
        total=ziShu_z+ziShu_e*0.5
        return total

    def fonts(self,font_name,font_size,font_config='e:/temp/test/fonts_list.config'):
        with open(font_config,'r',encoding='utf-8') as f:
            lines=f.readlines()
            _line=''
            for line in lines:
                newLine=line.strip('\n')
                _line=_line+newLine
            fontList=json.loads(_line)
        
        return ImageFont.truetype(fontList['fontList'][font_name],font_size)

    def split_txt_Chn_eng(self,wid,font_size,txt_input,Indent='no'):
        
        def put_words(txts,zi_per_line):    
            txtGrp=[]
            wd_lng=0
            pre_txt=''
            for c,t in enumerate(txts):
                if res.match(t):
                    if wd_lng+1>zi_per_line:
                        txtGrp.append(pre_txt)
                        pre_txt=t
                        wd_lng=1
                    else:
                        pre_txt=pre_txt+t
                        wd_lng=wd_lng+1
                else:
                    if t in ['”','’','，','。','！','：','；','.',',','!']:
                        pre_txt=pre_txt+' '+t
                        wd_lng=wd_lng+self.char_len(t)
                        
                    else:
                        if wd_lng+self.char_len(t)>zi_per_line: #先判断是这个英文单词+原有拼接的字符串长度是否>每行字符数
                            txtGrp.append(pre_txt) #大于，则保持原有的拼接字符串，不再加入该英文单词
                            pre_txt=' '+t #新的英文单词另起一行
                            wd_lng=self.char_len(t) #拼接字符串长度清零重计
                        else:                    
                            pre_txt=pre_txt+' '+t
                            wd_lng=wd_lng+self.char_len(t)
                       
                
                if wd_lng>zi_per_line:
                    wd_lng=0                
                    txtGrp.append(pre_txt)
                    pre_txt=''                
                else:
                    if c==len(txts)-1:
                        wd_lng=0                
                        txtGrp.append(pre_txt)
                        pre_txt='' 
                        
                    
            logging.info(txtGrp)
            return txtGrp
        
        txts=txt_input.splitlines()
        logging.info(txts)    
        
        if Indent=='yes':
            for i,t in enumerate(txts):
                txts[i]=chr(12288)+chr(12288)+t
        
        # print('composing line 82:', txts)
        
        res = re.compile(r'([\u4e00-\u9fa5])')   
        singleTxts=[]
        for t in txts:
            _t=res.split(t)
            _t_no_empty=list(filter(None,_t))      
            singleTxts.append(_t_no_empty)        
        
        split_txt=[]
        for singleTxt in singleTxts:
            grp=[]
            for st in singleTxt:
                if res.match(st):
                    grp.append(st)
                else:
                    grp.extend(st.split(' '))
            split_txt.append(grp)
            
        logging.info(split_txt)
            
        
        total_num=0
        for r in split_txt:
            total_num=total_num+len(r)
            
        zi_per_line=int(wid//font_size)
            
        outTxt=[]
        for r,split_t in enumerate(split_txt):
            outTxt.append(put_words(split_t,zi_per_line))
            
        para_num=0
        for tt in outTxt:
            for t in tt:
                para_num+=1

        return {'txt':outTxt,'para_num':para_num}

    def put_txt_img(self,draw,tt,total_dis,xy,dis_line,fill,font_name,font_size,addSPC='None'):
            
        fontInput=self.fonts(font_name,font_size)            
        if addSPC=='add_2spaces': 
            Indent='yes'
        else:
            Indent='no'
            
        # txt=self.split_txt(total_dis,font_size,t,Indent='no')
        txt=self.split_txt_Chn_eng(wid=total_dis,font_size=font_size,txt_input=tt,Indent=Indent)['txt']
        # font_sig = self.fonts('丁永康硬笔楷书',40)
        num=len(txt)   
        # draw=ImageDraw.Draw(img)

        logging.info(txt)
        n=0
        for t in txt:              
            m=0
            for tt in t:                  
                x,y=xy[0],xy[1]+(font_size+dis_line)*n
                if addSPC=='add_2spaces':   #首行缩进
                    if m==0:    
                        # tt='  '+tt #首先前面加上两个空格
                        logging.info('字数：'+str(len(tt))+'，坐标：'+str(x)+','+str(y))
                        logging.info(tt)
                        draw.text((x+font_size*0.2,y), tt, fill = fill,font=fontInput) 
                    else:                       
                        logging.info('字数：'+str(len(tt))+'，坐标：'+str(x)+','+str(y))
                        logging.info(tt)
                        draw.text((x,y), tt, fill = fill,font=fontInput)  
                else:
                    # logging.info('字数：'+str(len(tt))+'，坐标：'+str(x)+','+str(y))
                    # logging.info(tt)
                    draw.text((x,y), tt, fill = fill,font=fontInput)  

                m+=1
                n+=1

    def char_len(self,txt):
        len_s=len(txt)
        len_u=len(txt.encode('utf-8'))
        ziShu_z=(len_u-len_s)/2
        ziShu_e=len_s-ziShu_z
        total=ziShu_z+ziShu_e*0.5    
        return total

class Block(TxtFormat):
    def __init__(self):
        pass

    def draw_rct(self,w=720,h=300,color='#ffffff',radii=0,alpha=1):
        img=Image.new('RGB',(w,h),color)
        if radii>0:
            img=self.circle_corner(img,radii=radii)
        if alpha<1:
            img_bld=Image.new('RGBA',(img.size[0],img.size[1]))
            img=Image.blend(img_bld,img,alpha)
        # img.show()
        return img

    def draw_txt_block(self,txt,wid=600,total_dis=200,y_add=0,color='#ffffff',radii=0,alpha=1,font_size=30,dis_line=30,indent='yes'):
        txt_to_put=self.split_txt_Chn_eng(wid=total_dis,font_size=font_size,txt_input=txt,Indent=indent)
        # print(font_size,dis_line,txt_to_put)
        txts_para_num=txt_to_put['para_num']
        line_para=font_size if dis_line<= font_size else dis_line
        # h_block=int((txts_para_num*font_size+txts_para_num*line_para)*1.3)
        h_block=int((font_size+dis_line)*txts_para_num)
        # print(h_block)
        img=self.draw_rct(w=wid,h=h_block+y_add,color=color,radii=radii,alpha=alpha)
        return img

    def put_txt_to_img(self,box_wid=300,bg='#ffffff',radii=0,alpha=1,txt='测试',total_dis=250,xy=[10,10],dis_line=30,fill='#333333',font_name='楷体',font_size=30,addSPC='None'):
        if addSPC=='None':
            indent_draw='no'
        else:
            indent_draw='yes'
        img=self.draw_txt_block(txt=txt,wid=box_wid,total_dis=total_dis,y_add=xy[1],color=bg,radii=radii,alpha=alpha,font_size=font_size,dis_line=dis_line,indent=indent_draw)
        draw=ImageDraw.Draw(img)
        self.put_txt_img(draw,tt=txt,total_dis=total_dis,xy=xy,dis_line=dis_line,fill=fill,font_name=font_name,font_size=font_size,addSPC=addSPC)
        return img

    def circle_corner(self,img,radii=150):
        radii=int(img.size[0]*radii/4032)
        # 画圆（用于分离4个角）  
        circle = Image.new('L', (radii * 2, radii * 2), 0)  # 创建黑色方形
        # circle.save('1.jpg','JPEG',qulity=100)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, radii * 2, radii * 2), fill=255)  # 黑色方形内切白色圆形
        # circle.save('2.jpg','JPEG',qulity=100)

        # 原图转为带有alpha通道（表示透明程度）
        img = img.convert("RGBA")
        w, h = img.size

        # 画4个角（将整圆分离为4个部分）
        alpha = Image.new('L', img.size, 255)	#与img同大小的白色矩形，L 表示黑白图
        # alpha.save('3.jpg','JPEG',qulity=100)
        alpha.paste(circle.crop((0, 0, radii, radii)), (0, 0))  # 左上角
        alpha.paste(circle.crop((radii, 0, radii * 2, radii)), (w - radii, 0))  # 右上角
        alpha.paste(circle.crop((radii, radii, radii * 2, radii * 2)), (w - radii, h - radii))  # 右下角
        alpha.paste(circle.crop((0, radii, radii, radii * 2)), (0, h - radii))  # 左下角
        # alpha.save('4.jpg','JPEG',qulity=100)

        img.putalpha(alpha)		# 白色区域透明可见，黑色区域不可见
        # img.save('e:\\temp\\5555.png','PNG',qulity=100)

        # img.show()
        # img=img.convert('RGBA')
        return img



def tt(w,h,ft,ft_sz):
    foo=TxtFormat()
    font=foo.fonts(ft,ft_sz)
    img=Image.new('RGB',(w,h),'#ffffff')
    draw=ImageDraw.Draw(img)
    draw.text((0,0),'地','#003366',font)
    img.show()

if __name__=='__main__':
    pic=Block()
    # rct=pic.draw_rct(w=200,h=700,color='#33ee99',radii=190,alpha=1)
    # rct.show()
    txt=r'   观自在菩萨，行深般若波罗蜜多时，照见五蕴皆空，度一切苦厄。舍利子，色不异空，空不异色，色即是空，空即是色，受想行识，亦复如是。舍利子，是诸法空相，不生不灭，不垢不净，不增不减。是故空中无色，无受想行识，无眼耳鼻舌身意，无色声香味触法，无眼界，乃至无意识界，无无明，亦无无明尽，乃至无老死，亦无老死尽。无苦集灭道，无智亦无得。以无所得故。菩提萨埵，依般若波罗蜜多故，心无挂碍。无挂碍故，无有恐怖，远离颠倒梦想，究竟涅盘。三世诸佛，依般若波罗蜜多故，得阿耨多罗三藐三菩提。故知般若波罗蜜多，是大神咒，是大明咒，是无上咒，是无等等咒，能除一切苦，真实不虚。故说般若波罗蜜多咒，即说咒曰：揭谛揭谛，波罗揭谛，波罗僧揭谛，菩提萨婆诃。'
    # rct=pic.draw_txt_block(txt=txt,wid=600,color='#ffffff',radii=0,alpha=1,font_size=30,dis_line=30,indent='yes')
    # rct.show()
    blk=pic.put_txt_to_img(box_wid=440,bg='#ffffff',radii=0,alpha=1,txt=txt,total_dis=340,xy=(25,30),dis_line=60,fill='#222222',font_name='楷体',font_size=30,addSPC='None')
    blk.show()


    # tt(200,200,'优设标题',200)