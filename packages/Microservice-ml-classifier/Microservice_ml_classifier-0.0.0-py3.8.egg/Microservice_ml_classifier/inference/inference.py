import numpy as np
from numpy import ndarray
import PIL
from PIL import Image
import torch
import logging

from Microservice_ml_classifier.network.classifier import Net
from Microservice_ml_classifier.dataset.dataloader import TRANSFORM, CLASSES

DEFAULT_CKPT_PATH = '/media/victor/851aa2dd-6b93-4a57-8100-b5253aa4eedd/side_projects/deployment_image_classifier/model_weigts/epoch=37-step=475000.ckpt'

class Inferece(object):
    '''
    Class that performs inference from a trained model
    '''
    def __init__(self, ckpt_path:str=DEFAULT_CKPT_PATH, device:str='cuda'):
        self._ckpt_path = ckpt_path
        if device not in ['cuda', 'cpu']:
            raise ValueError('Device not recognised. Device must be cpu or cuda')
        self._device = torch.device(device)
        self.model = self._load_model()
    def _load_model(self):
        model = Net()
        state_dict_pl = torch.load(self._ckpt_path)['state_dict']
        new_state_dict = self._adapt_stat_dict(state_dict_pl)
        model.load_state_dict(new_state_dict)
        model.eval()
        model.to(self._device)
        return model
    @staticmethod
    def _adapt_stat_dict(state_dict_pl:dict) ->dict:
        new_state_dict = {}
        for k, v in state_dict_pl.items():
            new_k = k[11:]
            new_state_dict[new_k] = v
        return new_state_dict
    def run_inference(self, img:PIL):
        pre_input = self.preprocess_input(img)
        output = self._inference(pre_input)
        post_out = self.postprocess_output(output)
        return post_out

    def __call__(self, img:PIL):
        try:
            result = self.run_inference(img)
            msg = 'Processing ok!'
            dct_out = {'result': result, 'msg': msg}
            return dct_out
        except Exception as e:
            result = None
            msg = str(e)
            dct_out = {'result': result, 'msg': msg}
            return dct_out

    def _inference(self, pre_input:torch.Tensor):
        with torch.no_grad():
            try:
                return self.model(pre_input)
            except RuntimeError as e:
                logging.error(e)
                return None

    def preprocess_input(self, img:PIL) -> torch.Tensor:
        if isinstance(img, ndarray):
            img = Image.fromarray(img.astype('uint8'), 'RGB')
        trf_input = TRANSFORM(img)
        pre_input = torch.unsqueeze(trf_input, dim=0)
        input = pre_input.to(self._device)
        return input
    @staticmethod
    def postprocess_output(output:torch.Tensor):
        idx_output = torch.argmax(output, dim=1)
        post_out = CLASSES[idx_output]
        return post_out


if __name__ == '__main__':
    img_path = '/media/victor/851aa2dd-6b93-4a57-8100-b5253aa4eedd/side_projects/deployment_image_classifier/dataset/cifar-10-batches-py/images_cifar10/abandoned_ship_s_000004.png'
    ckpt_path = '/media/victor/851aa2dd-6b93-4a57-8100-b5253aa4eedd/side_projects/deployment_image_classifier/model_weigts/epoch=37-step=475000.ckpt'
    device = 'cuda'
    model_inference = Inferece(ckpt_path=ckpt_path, device=device)
    #img = Image.open(img_path)
    dummy_img = np.zeros((32, 32, 3), dtype=np.uint8)
    dct_out = model_inference(dummy_img)
    pass
