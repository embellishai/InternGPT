import os
import sys
import wget

from .grit_src.image_dense_captions import image_caption_api, init_demo, dense_pred_to_caption, dense_pred_to_caption_only_name
from detectron2.data.detection_utils import read_image

class DenseCaptioning():
    def __init__(self, device,e_mode):
        self.device = device
        self.demo =  None
        self.e_mode = e_mode
        self.model_checkpoint_path = "model_zoo/grit_b_densecap_objectdet.pth"
        self.download_parameters()

    def initialize_model(self):
        if self.e_mode is True:
            self.demo = init_demo("cpu")
        else:
            self.demo = init_demo(self.device)

    def image_dense_caption_debug(self, image_src):
        dense_caption = """
        1. the broccoli is green, [0, 0, 333, 325]; 
        2. a piece of broccoli, [0, 147, 143, 324]; 
        3. silver fork on plate, [4, 547, 252, 612];
        """
        return dense_caption

    def download_parameters(self):
       url = "https://huggingface.co/spaces/OpenGVLab/InternGPT/resolve/main/model_zoo/grit_b_densecap_objectdet.pth?download=true"
       if not os.path.exists(self.model_checkpoint_path):
          wget.download(url, out=self.model_checkpoint_path)

    def image_dense_caption(self, image_src):
        dense_caption = image_caption_api(image_src, self.device)
        print('\033[1;35m' + '*' * 100 + '\033[0m')
        print("Step2, Dense Caption:\n")
        print(dense_caption)
        print('\033[1;35m' + '*' * 100 + '\033[0m')
        return dense_caption
    
    def run_caption_api(self,image_src):
        if self.e_mode:
            self.demo.predictor.model.to(self.device)
        img = read_image(image_src, format="BGR")
        print(img.shape)
        predictions, visualized_output = self.demo.run_on_image(img,self.device)
        new_caption = dense_pred_to_caption_only_name(predictions)
        if self.e_mode:
            self.demo.predictor.model.to("cpu")
        return new_caption

    def run_caption_tensor(self,img):
        # img = read_image(image_src, format="BGR")
        # print(img.shape)
        predictions, visualized_output = self.demo.run_on_image(img,self.device)
        new_caption = dense_pred_to_caption_only_name(predictions)
        return new_caption
    

