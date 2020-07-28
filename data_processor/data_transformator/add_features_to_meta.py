import glob
import json


import torch
from mmcv import Config
from mmcv.runner import load_checkpoint

from mmfashion.models import build_landmark_detector
from mmfashion.utils import get_img_tensor   



def add_landmarks(config, queried_images_path, checkpoint, use_cuda=True):
    seed = 0
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

    cfg = Config.fromfile(config)   

    # build model and load checkpoint
    model = build_landmark_detector(cfg.model)
    print('model built')
    load_checkpoint(model, checkpoint)
    print('load checkpoint from: {}'.format(checkpoint))

    if use_cuda:
        model.cuda()

    # detect landmark
    model.eval()

    images = glob.glob(queried_images_path+"/*.jpg")

    for image in images:

        image_id = image.split('/')[-1].split('.')[0]    

        img_tensor, w, h = get_img_tensor(image, use_cuda, get_size=True)
        pred_vis, pred_lm = model(img_tensor, return_loss=False)
        pred_lm = pred_lm.data.cpu().numpy()
        vis_lms = {'landmarks':[]}
        
        for i, vis in enumerate(pred_vis):
            if vis >= 0.5:
                print('detected landmarks: {} {} for image {}'.format(
                    pred_lm[i][0] * (w / 224.), pred_lm[i][1] * (h / 224.), image_id))
                vis_lms['landmarks'].append(pred_lm[i].tolist())
            if vis_lms['landmarks']:                
                json.dump(vis_lms, open(queried_images_path+'/'+str(image_id)+'.json', 'w'))
                
    return queried_images_path





