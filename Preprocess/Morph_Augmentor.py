import numpy as np
import random
import math
import manage 
import coloraugmentation as CN




def Augmentation_from_Folder(FolderPath, target_w,target_h, p_flip=0.5, p_rotate=0.5,
                             samples = 0, sigma=0.05,spatial_sample=False,
                             GPU_num=4, oversample = False, png=False):
    '''
    put one patient's folder in, output 4d array with augmentations
    :param FolderPath:
    :param ColorAugmentation:
    :param samples: when samples are 0, random sample all the patches in the folder, when sample is and int, fix sample number
    :return: 4d array
    '''
    alpha0 = np.random.uniform(1 - sigma, 1 + sigma)
    beta0 = np.random.uniform(-sigma, sigma)
    alpha1 = np.random.uniform(1 - sigma, 1 + sigma)
    beta1 = np.random.uniform(-sigma, sigma)
    alpha2 = np.random.uniform(1 - sigma, 1 + sigma)
    beta2 = np.random.uniform(-sigma, sigma)

    if png:
        path = manage.list_png(FolderPath)
    else:
        path = manage.list_npy(FolderPath)

    n_img = len(path)
    if samples==0:
        samples = math.ceil(n_img/GPU_num)*GPU_num
    if samples>n_img:
        if oversample:
            path = random.choices(path, k=samples)  
        else:
            path = path
    else:
        path = random.sample(path, k=samples)
        
    n_img = len(path)
    out = np.zeros((n_img, target_h, target_w, 3))
    for i in range(n_img):
        if png:
            img = Image.open(path[i])
            img = np.array(img)[...,:3]
        else:
            img = np.load(path[i])
        if target_h<img.shape[0] or target_h<img.shape[1]:
            if spatial_sample:
                img = img_crop(img,target_w=target_w,target_h=target_h)
            else:
                img = img[:target_h,:target_w,:]
        if np.random.uniform(0,1)>p_flip:
            img = img_flip(img)
        if np.random.uniform(0,1)>p_rotate:
            img = img_rotate(img)
        #augmentation
        img = CN.color_augmentation(img,alpha0=alpha0, beta0=beta0,
                                            alpha1=alpha1, beta1=beta1,
                                            alpha2=alpha2, beta2=beta2)
        out[i,...] = img
    return out



def rotate90(array):
    return np.rot90(array)

def rotate180(array):
    return np.rot90(np.rot90(array))

def rotate270(array):
    return np.rot90(np.rot90(np.rot90(array)))

def img_rotate(array):
    ind = random.sample(range(3),1)[0]
    if ind == 0:
        out_array = rotate90(array)
    elif ind == 1:
        out_array = rotate180(array)
    else:
        out_array = rotate270(array)
    return out_array

def img_flip(array):
    ind = random.sample(range(2),1)[0]
    out_array = np.flip(array,axis=ind)
    return out_array

def img_crop(array,target_w,target_h):
    w, h, _ = array.shape
    x = random.randint(0,int(w - target_w))
    y = random.randint(0,int(h - target_h))
    out_array = array[x:x+target_w,y:y+target_h,:]
    return out_array

