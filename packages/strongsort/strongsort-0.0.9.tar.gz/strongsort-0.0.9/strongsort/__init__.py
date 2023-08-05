from strongsort.utils import *
from strongsort.configs import *
from strongsort.sort import *
from strongsort import *
from strongsort.strong_sort import *

__all__ = ['StrongSORT', 'build_tracker']
__version__ = '0.0.9'

def build_tracker(cfg, use_cuda):
    return StrongSORT(cfg.STRONGSORT.REID_CKPT, 
                max_dist=cfg.STRONGSORT.MAX_DIST, min_confidence=cfg.STRONGSORT.MIN_CONFIDENCE, 
                nms_max_overlap=cfg.STRONGSORT.NMS_MAX_OVERLAP, max_iou_distance=cfg.STRONGSORT.MAX_IOU_DISTANCE, 
                max_age=cfg.STRONGSORT.MAX_AGE, n_init=cfg.STRONGSORT.N_INIT, nn_budget=cfg.STRONGSORT.NN_BUDGET, use_cuda=use_cuda)
