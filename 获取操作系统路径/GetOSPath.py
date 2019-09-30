import os

def get_desk_path():
    """
    :return: 返回当前系统桌面的路径
    """
    return os.path.join(os.path.expanduser("~"), 'Desktop')


def get_now_path():
    """
    :return: 返回当前路径
    """
    return os.getcwd()


def get_dir_name(filepath):
    """
    分割文件名及路径
    :filepath: 传入文件的绝对路径
    :return: 返回传入文件的路径及文件名
    """
    return os.path.split(filepath)


def get_makeup_name(dir,name):
    """
    合并路径及文件名
    :param dir:
    :param name:
    :return:
    """
    return os.path.join(dir,name)


if __name__=='__main__':
    print(get_desk_path())
    print(get_now_path())
    print(get_dir_name(r'C:\Users\admin\Desktop\test.xls'))
    print(get_makeup_name(r'C:\Users\admin\Desktop', 'test.xls'))

