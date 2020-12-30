# AUTOGENERATED! DO NOT EDIT! File to edit: nbs|nbs/course2020/nbs/course2020/05_Inference_Server.ipynb (unless otherwise specified).

__all__ = ['get_learner', 'make_datasets', 'save_im', 'inference']

# Cell
from fastai.vision.all import *

# Cell
from .style_transfer import *

# Cell
def get_learner(fn, cpu=False):
  return load_learner(fn, cpu=cpu)

# Cell
def make_datasets(learn, fns, bs=1):
  cuda = next(learn.model.parameters()).is_cuda
  dset = Datasets(fns, tfms=[PILImage.create])
  if cuda:
    after_batch = [IntToFloatTensor(), Normalize.from_stats(*imagenet_stats)]
    dl = dset.dataloaders(after_item=[ToTensor()], after_batch=after_batch, bs=1)
  else:
    after_batch = [Normalize.from_stats(*imagenet_stats, cuda=False)]
    dl = dset.dataloaders(after_item=[ToTensor()], after_batch=after_batch, bs=1, device='cpu')
  return dl

# Cell
from torchvision.utils import save_image

# Cell
def save_im(imgs:list, path):
  "Save a n*c*w*h `Tensor` into seperate images"
  [save_image(im, f'{path}/{i}.png') for i, im in enumerate(imgs)]

# Cell
def inference(pkl_name, fnames:list, path:Path, cpu:bool=True):
  "Grab inference on a model, filenames, and a path to save it to"
  path = path/'results'
  path.mkdir(parents=True, exist_ok=True)
  learn = get_learner(pkl_name, cpu)
  if len(fnames) > 1:
    dls = []
    for fname in fnames:
      dls.append(make_datasets(learn, fnames, 1))
  else:
    dls = [make_datasets(learn, fnames, 1)]
  res = []
  for b in dls:
    t_im = b.one_batch()[0]
    with torch.no_grad():
      out = learn.model(t_im)
    res.append(out)
  save_im(res, path)