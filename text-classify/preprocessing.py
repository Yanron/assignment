import os
import jieba.posseg as  pseg
import jieba
import  codecs
import myIO
def load_stopwords():
    # 读取停用词表
    f = open('C:/lyr/DM/stop_words_ch.txt')
    sw = [line.strip() for line in f]
    return sw
        
def cut_words(label, file_list, file_path, cut_dir):
    print('Run task (%s)...' % (os.getpid()))
    for j, file_name in enumerate(file_list):
        fullpath = file_path + file_name
        content = myIO.readfile(fullpath)
        content = content.replace('\r\n'.encode('utf-8'),''.encode('utf-8')).strip()
        content = content.replace(' '.encode('utf-8'),''.encode('utf-8')).strip()
        content_seg = pseg.cut(content)
        _write_noun(file_name, content_seg, cut_dir)
 
 
def _write_noun(file_name, content_seg, cut_words_path):
    # 这里也许可以试试set然后用pickle来存python对象
    fullpath = cut_words_path + file_name
    stop_words = load_stopwords()
    result_seg=''
    noun = ['n', 'ns', 'nt', 'nz', 'nx']  
    for word, flag in content_seg:
        if word in stop_words:
                continue       
        if flag in noun:
                result_seg=result_seg+word+' '
    myIO.savefile(fullpath, result_seg.encode('utf-8')) 

def gen_save_words(source_path, cut_path):
    path_list = os.listdir(source_path)
    for i, mydir in enumerate(path_list):
        print(mydir)
        file_path = source_path + mydir + '/'
        cut_dir = cut_path + mydir + '/'
        if not os.path.exists(cut_dir):
            os.makedirs(cut_dir)
        file_list = os.listdir(file_path)
        # 进行分词
        cut_words(mydir, file_list, file_path, cut_dir)


source_path='C:/lyr/DM/trainData/'
cut_path='C:/lyr/DM/train_cut/'
gen_save_words(source_path,cut_path)
