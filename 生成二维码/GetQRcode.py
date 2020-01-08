from PIL import Image
from MyQR import myqr
from lib import GetOSPath as GOP
import qrcode

def create_qrcode(url, qrcodename=None, logopic=None, dir=None,style=1):
    """
    二维码生成
    :param url:URL地址或文本内容（style=1时，不支持中文）
    :param qrcodename:生成的二维码图片的保存名称
    :param logopic:传入的图标（.jpg， .png ，.bmp ，.gif）
    :param dir:生成的二维码保存的路径
    :param style:生成方式，默认=1普通生成方式，url内容不支持中文，图片为二维码的背景图（支持动态图片）；=2 url支持中文，图片为中心小图标
    :return:
    """
    # 生成的二维码保存的路径
    if dir:  # 如果dir传值了，则取dir
        savedir = dir
    elif logopic:
        savedir,_ = GOP.get_dir_name(logopic)  # dir没传值logopic传值了则取logopic的路径
    else:
        savedir = GOP.get_desk_path()  # 都没传值则取系统桌面位置
    savedir = str(savedir)
    print(savedir)

    # 生成的二维码图片的保存名称
    if qrcodename: # 如果qrcodename传值了，则取qrcodename
        pass
    else: # 如果未传值
        qrcodename = 'rq_'+GOP.get_dir_name(logopic)[-1] if logopic else 'rqcode.png'  # 如果传入了图片，则根据图片名称取值，否则取默认值


    if style == 1:
        myqr.run(
            words=url,# 在命令后输入链接或者句子作为参数，然后在程序的当前目录中产生相应的二维码图片文件，默认命名为” qrcode.png“
            version=4, # 设置容错率为最高默认边长是取决于你输入的信息的长度和使用的纠错等级；而默认纠错等级是最高级的H
            level='H', # 控制纠错水平，范围是L、M、Q、H，从左到右依次升高
            picture=logopic, # 用来将QR二维码图像与一张同目录下的图片相结合，产生一张黑白图片
            colorized=True,  # 可以使产生的图片由黑白(False)变为彩色(True)的(jpg格式的图片不支持彩色）
            contrast=1.0, # 用以调节图片的对比度，1.0 表示原始图片，更小的值表示更低对比度，更大反之。默认为1.0。
            brightness=1.0, # 用来调节图片的亮度，其余用法和取值与 -con 相同
            save_name=qrcodename, # 控制文件名，格式可以是 .jpg， .png ，.bmp ，.gif ；
            save_dir= savedir  # 生成的二维码后保存的位置。
            )
    else:
        qr = qrcode.QRCode(
            version=4,  # 设置容错率为最高  值越大，二维码上的黑点越密集
            error_correction=qrcode.ERROR_CORRECT_H,  # 用于控制二维码的错误纠正程度
            box_size=10,  # 控制二维码中每个格子的像素数，默认为10  值越大，图片越大文件大小越大
            border=1,  # 二维码四周留白，包含的格子数，默认为4  值越大，整个二维码四周的空白越大
            # image_factory=None,  保存在模块根目录的image文件夹下
            # mask_pattern=None
            )
        qr.add_data(url)  # QRCode.add_data(data)函数添加数据
        qr.make(fit=True)  # QRCode.make(fit=True)函数生成二维码图片
        img = qr.make_image()
        img = img.convert("RGBA")  # 二维码设为彩色 如果没有此行代码，二维码图片中的logo图片将会变成黑白色的
        # img = qr.make_image(fill_color='black',back_color='white') # 设置二维码图片填充色和背景色
        if logopic: # 当传入logo图片时，对logo图片进行以下操作
            logosize = Image.open(logopic)  # 打开logo文件（传gif生成的二维码也是没有动态效果的）
            img_w, img_h = img.size # 计算生成的二维码图片的尺寸
            logo_w, logo_h = logosize.size     # 传入的logo图片的尺寸
            factor = 4  # 默认logo最大设为图片的四分之一
            # 计算二维码上中间logo的标准大小
            s_w = int(img_w / factor)
            s_h = int(img_h / factor)
            print(s_w,s_h)
            # 重新设置logo图片大小
            # 1、最终图片为正方形（会拉伸或压缩）
            # if logo_w > s_w or logo_h > s_h:  #传入的logo图片任何一边大于标准大小，都将图片拉伸/压缩成标准大小
            #     logo_w = s_w
            #     logo_h = s_h
            # 2、最终图片为实际图形等比例的缩放（最大边不大于logo的标准大小）
            # if logo_w == logo_h:
            #     logo_w=logo_h=s_w
            # else:
            logomaxsize = logo_w if logo_w > logo_h else logo_h
            smaxsize = s_w if s_w>s_h else s_h
            ab = (smaxsize / logomaxsize) # 计算缩放比例
            logo_w,logo_h = int(ab * logo_w),int(ab * logo_h)

            logosize = logosize.resize((logo_w, logo_h), Image.ANTIALIAS)

            # 计算logo图片在二维码中的位置
            l_w = int((img_w - logo_w) / 2)
            l_h = int((img_h - logo_h) / 2)
            logosize = logosize.convert("RGBA")
            img.paste(logosize, (l_w, l_h), logosize)
        # img.show()  # 展示二维码
        img.save(GOP.get_makeup_name(savedir,qrcodename), quality=100)  # 保存二维码
    return savedir

if __name__ == '__main__':
    # def create_qrcode(url, qrcodename, logopic=None, dir=None,style = 1):
    logopic =r'C:\Users\admin\Desktop\test.png'
    dir = r'C:\Users\admin\Desktop'
    qrcodename = '3_jianshu.png'
    create_qrcode('https://github.com/hasen2/PubWithPython', logopic=logopic, dir=dir,style=1)

