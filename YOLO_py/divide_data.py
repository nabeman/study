#train,val, testの自動分割
import glob
import os
import random

dataset_dir="original_set5"

#データ一覧
img_list=glob.glob(os.path.join(dataset_dir+"\labels","*.txt"))

#データをシャッフル
random.shuffle(img_list)

#8:1:1に分割
num_data=len(img_list)
num_train=int(num_data*0.8)
num_val=int(num_data*0.1)
num_test=num_data-num_train-num_val

#分割
split_dict={}
split_dict["train"]=img_list[:num_train]
split_dict["valid"]=img_list[num_train:num_train+num_val]
split_dict["test"]=img_list[num_train+num_val:]


for name in ["train","test","valid"]:
    #フォルダ作成
    dir_name=os.path.join(dataset_dir,name)
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    #images,labelsフォルダ作成
    for folder in ["images","labels"]:
        dir_name2=os.path.join(dir_name,folder)
        if not os.path.exists(dir_name2):
            os.mkdir(dir_name2)

        #コピー
        for path in split_dict[name]:
            txt_path=path
            img_path=path.replace("labels","images").replace(".txt",".jpg")
            if dir_name2.find("labels")>0:
                os.system("copy {} {}".format(txt_path,dir_name2))
                print("copy {} {}".format(txt_path,dir_name2))
            else:
                os.system("copy {} {}".format(img_path,dir_name2))