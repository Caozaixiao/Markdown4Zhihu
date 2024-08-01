

# Usage: This program aims to transfer your markdown file into a way zhihu.com can recognize correctly.
#        It will mainly deal with your local images and the formulas inside.

import os
import re
import argparse
import subprocess
import chardet
import functools
import os.path as op

from PIL import Image
from pathlib2 import Path
from shutil import copyfile

###############################################################################################################
## Please change the GITHUB_REPO_PREFIX value according to your own GitHub user name and relative directory. ##
###############################################################################################################
# GITHUB_REPO_PREFIX = Path("https://raw.githubusercontent.com/`YourUserName`/`YourRepoName`/master/Data/")
# Your image folder remote link
GITHUB_REPO_PREFIX = "https://raw.githubusercontent.com/Caozaixiao/Markdown4Zhihu/master/Data/"
COMPRESS_THRESHOLD = 5e5  # The threshold of compression

# The main function for this program


def process_for_zhihu():
    # 如果args.encoding为空，则打开输入文件，读取文件内容，使用chardet库检测文件编码，并将编码赋值给args.encoding
    if args.encoding is None:
        with open(str(args.input), 'rb') as f:
            s = f.read()
            chatest = chardet.detect(s)
            args.encoding = chatest['encoding']
        print(chatest)
    # 打开输入文件，读取文件内容，使用args.encoding编码
    with open(str(args.input), "r", encoding=args.encoding) as f:
        lines = f.read()
        # 对文件内容进行图片处理
        lines = image_ops(lines)
        # 对文件内容进行公式处理
        lines = formula_ops(lines)
        # 对文件内容进行表格处理
        lines = table_ops(lines)
        # 将处理后的文件内容写入新的文件中
        with open(op.join(args.current_script_data_path, args.input.stem+"_for_zhihu.md"), "w+", encoding=args.encoding) as fw:
            fw.write(lines)
        # 清理图片文件夹
        cleanup_image_folder()
        # 执行git操作
        git_ops()

# Deal with the formula and change them into Zhihu original format


# 定义一个函数，用于处理公式
def formula_ops(_lines):
    # 使用正则表达式替换公式
    _lines = re.sub('((.*?)\$\$)(\s*)?([\s\S]*?)(\$\$)\n',
                    '\n<img src="https://www.zhihu.com/equation?tex=\\4" alt="\\4" class="ee_img tr_noresize" eeimg="1">\n', _lines)
    # 使用正则表达式替换公式
    _lines = re.sub('(\$)(?!\$)(.*?)(\$)',
                    ' <img src="https://www.zhihu.com/equation?tex=\\2" alt="\\2" class="ee_img tr_noresize" eeimg="1"> ', _lines)
    # 返回处理后的字符串
    return _lines

# The support function for image_ops. It will take in a matched object and make sure they are competible


def rename_image_ref(m, original=True):
    # global image_folder_path
    # 如果original为True，则取m.group(2)，否则取m.group(1)
    ori_path = m.group(2) if original else m.group(1)

    try:
        if op.exists(ori_path):  # 如果ori_path存在
            full_img_path = ori_path  # 将full_img_path设置为ori_path
            img_stem = Path(full_img_path).stem  # 获取文件名
            img_suffix = Path(full_img_path).suffix  # 获取文件后缀
            img_name = img_stem+img_suffix  # 获取文件名和后缀
            img_name_new = img_name  # 将img_name_new设置为img_name
            # 如果img_name_new在image_folder_path中存在
            if op.exists(op.join(args.image_folder_path, img_name_new)):
                i = 1  # 设置计数器i为1
                # 如果img_name_new在image_folder_path中存在
                while op.exists(op.join(args.image_folder_path, img_name_new)):
                    # 将img_name_new设置为img_stem+"_"+str(i)+img_suffix
                    img_name_new = img_stem+"_"+str(i)+img_suffix
                    i += 1  # 计数器i加1

            copyfile(full_img_path, op.join(  # 将full_img_path复制到image_folder_path中
                args.image_folder_path, img_name_new))
            # 将full_img_path设置为image_folder_path中的img_name_new
            full_img_path = op.join(args.image_folder_path, img_name_new)

        else:
            # 将full_img_path设置为file_parent中的ori_path
            full_img_path = op.join(args.file_parent, ori_path)
            img_stem = Path(full_img_path).stem  # 获取文件名
            if not op.exists(full_img_path):  # 如果full_img_path不存在
                return m.group(0)  # 返回m.group(0)
    except OSError:  # 如果发生OSError
        return m.group(0)  # 返回m.group(0)

    # 如果full_img_path的大小大于COMPRESS_THRESHOLD且compress为True
    if op.getsize(full_img_path) > COMPRESS_THRESHOLD and args.compress:
        full_img_path = reduce_single_image_size(
            full_img_path)  # 将full_img_path的大小减小

    image_ref_name = Path(full_img_path).name  # 获取文件名
    args.used_images.append(image_ref_name)  # 将文件名添加到used_images中

    print('full_img_path', full_img_path)  # 打印full_img_path
    print('image_ref_name', image_ref_name)  # 打印image_ref_name
    if original:
        return "!["+m.group(1)+"]("+GITHUB_REPO_PREFIX+args.input.stem + "/" + image_ref_name+")"
    else:
        return '<img src="'+GITHUB_REPO_PREFIX+args.input.stem+"/" + image_ref_name + '"'


def cleanup_image_folder():
    # 获取image_folder_path路径下的所有文件路径
    actual_image_paths = [op.join(args.image_folder_path, i) for i in os.listdir(
        args.image_folder_path) if op.isfile(op.join(args.image_folder_path, i))]
    # 遍历所有文件路径
    for image_path in actual_image_paths:
        # 如果文件名不在used_images列表中
        if Path(image_path).name not in args.used_images:
            # 打印提示信息
            print("File "+str(image_path) +
                  " is not used in the markdown file, so it will be deleted.")
            # 删除文件
            os.remove(str(image_path))

# Search for the image links which appear in the markdown file. It can handle two types: ![]() and <img src="LINK" alt="CAPTION" style="zoom:40%;" />.
# The second type is mainly for those images which have been zoomed.


# 定义一个函数image_ops，用于处理图片操作
def image_ops(_lines):
    # 使用正则表达式替换图片引用，original参数为True
    _lines = re.sub(r"\!\[(.*?)\]\((.*?)\)",
                    functools.partial(rename_image_ref, original=True), _lines)
    # 使用正则表达式替换图片引用，original参数为False
    _lines = re.sub(r'<img src="(.*?)"',
                    functools.partial(rename_image_ref, original=False), _lines)
    # 返回处理后的_lines
    return _lines

# Deal with table. Just add a extra \n to each original table line


def table_ops(_lines):
    return re.sub("\|\n", r"|\n\n", _lines)


def reduce_single_image_size(image_path):
    # The output file path suffix must be jpg
    output_path = Path(image_path).parent/(Path(image_path).stem+".jpg")
    if op.exists(image_path):
        img = Image.open(image_path)
        # 如果图片的宽度大于高度且宽度大于1920，则将图片宽度调整为1920，高度按比例缩放
        if (img.size[0] > img.size[1] and img.size[0] > 1920):
            img = img.resize(
                (1920, int(1920*img.size[1]/img.size[0])), Image.ANTIALIAS)
        # 如果图片的高度大于宽度且高度大于1080，则将图片高度调整为1080，宽度按比例缩放
        elif (img.size[1] > img.size[0] and img.size[1] > 1080):
            img = img.resize(
                (int(1080*img.size[0]/img.size[1]), 1080), Image.ANTIALIAS)
        # 将图片转换为RGB模式，并保存到output_path，优化为True，质量为85
        img.convert('RGB').save(output_path, optimize=True, quality=85)
    return output_path

# Push your new change to github remote end


# 定义一个函数，用于执行git操作
def git_ops():
    # 执行git add命令，将所有文件添加到暂存区
    subprocess.run(["git", "add", "-A"])
    # 执行git commit命令，提交更改，并添加提交信息
    subprocess.run(["git", "commit", "-m", "update file "+args.input.stem])
    # 执行git push命令，将更改推送到远程仓库的master分支
    subprocess.run(["git", "push", "-u", "origin", "master"])


if __name__ == "__main__":
    # 创建一个ArgumentParser对象，用于解析命令行参数
    parser = argparse.ArgumentParser(
        'Please input the file path you want to transfer using --input=""')
    # 添加一个参数，用于指定是否压缩图片
    parser.add_argument('--compress', action='store_true',
                        help='Compress the image which is too large')
    # 添加一个参数，用于指定要传输的文件的路径
    parser.add_argument('-i', '--input', type=str,
                        help='Path to the file you want to transfer.')
    # 添加一个参数，用于指定输入文件的编码
    parser.add_argument('-e', '--encoding', type=str,
                        help='Encoding of the input file')

    # 解析命令行参数
    args = parser.parse_args()
    # 初始化一个空列表，用于存储使用的图片
    args.used_images = []
    # 如果没有输入文件路径，则抛出异常
    if args.input is None:
        raise FileNotFoundError("Please input the file's path to start!")
    else:
        # 将输入文件路径转换为Path对象
        args.input = Path(args.input)
        # 获取输入文件的父目录
        args.file_parent = str(args.input.parent)

        # 获取当前脚本的Data目录路径
        args.current_script_data_path = str(
            Path(__file__).absolute().parent / 'Data')
        # 获取图片文件夹路径
        args.image_folder_path = op.join(
            args.current_script_data_path, args.input.stem)
        # 如果图片文件夹不存在，则创建
        if not op.exists(args.image_folder_path):
            os.makedirs(args.image_folder_path)

        # 打印图片文件夹路径
        print(args.image_folder_path)
        # 调用process_for_zhihu函数
        process_for_zhihu()
