__version__ = "0.0.38"
import threading
import argparse
import json
import os.path
import glob
import numpy
import scipy
import scipy.ndimage
import scipy.interpolate
import pandas
import rawpy
import hdbscan
import skimage.transform
import skimage.io
import skimage.util
#import skimage.morphology
import skimage.segmentation


class LimuImage:
  def __init__(self):
    self.metadata = None
    self._data = {}
    self.npz_obj = {}
    self._produce = { # prod lookup
      #'label':self._p_label,
      #'barcode':self.prod_barcode,
      'imageraw':self.prod_imageraw,
      'labels':self.prod_labels,
      'leafprops':self.prod_leafprops,
      'leafraw':self.prod_leafraw,
      'leafrgb':self.prod_leafrgb,
      'lesions':self.prod_lesions,
      'mask':self.prod_mask,
      'norm':self.prod_norm,
      'norminv':self.prod_norminvert,
      'sampleprops':self.prod_sampleprops,
      #'separation':self.prod_separation,
      'segmentation':self.prod_segmentation,
      'stain':self.prod_stain,
      'white':self.prod_white,
      'white_small':self.prod_whitesmall,
      }
    self._keeps = [ 
      'leafraw',
      'mask',
      'white_small',
      'labels',
      'leafprops',
      'lesions',
      'sampleprops',  
       ]
    self.name = 'name not set'
    self.kwargs = {}

  def clean(self):
    del self._data
    del self.npz_obj

  @staticmethod
  def get_biggest_label(labels):
    # return the label with biggest area
    # zero label is excluded
    # labels must be non-negative int
    counts = numpy.bincount(labels.ravel())
    score = list(numpy.argsort(counts))
    candidate = score.pop()
    if candidate > 0:
      return candidate
    return score.pop()
    

  @staticmethod
  def get_disk(r):
    d= skimage.morphology.disk(r)
    pw = (2*numpy.pi* r**2)**.5 - r
    d= numpy.pad( d,int(numpy.round(pw,0)),mode='constant')*1.0
    d /= d.sum()
    d =  d-d.mean()
    return d

  def has_data(self, key):
    if key in self._data.keys():
      return True
    if key in self.npz_obj.keys():
      return True
    return False

  def get_data(self, key, remake=False):
    if remake:
      self._produce[key](key)
    if key in self._data.keys():
      return self._data[key]
    if key in self.npz_obj.keys():
      self._data[key] = self.npz_obj[key]
      return self._data[key]
    print(key,)
    self._produce[key](key)
    return self._data[key] 

  @staticmethod
  def get_mask_adv(array):
    # returns a more advanced mask from boolean mask    
    # regular mask
    adv = array.astype(numpy.uint8) | 128 # bit 1, 128 just for convinient printing
    # with holes filled
    adv = adv | scipy.ndimage.binary_fill_holes(
        array).astype(numpy.uint8) << 1 # bit 2
    # outer background
    adv =  adv | ( 0b10 & ~adv) << 5  # bit 7 
    # holes 
    adv += ( ( adv >> 1) & ( ~adv & 0b1 ) ) <<  5 # bit 6
    # outer edge
    adv += skimage.segmentation.find_boundaries(0b10 & adv, mode='inner').astype(numpy.uint8) << 3 # bit 4
    # "center line" # very innacurate but anyway...
    idxs =  scipy.ndimage.distance_transform_edt(0b10 & adv).argmax(1)
    rs = numpy.arange(idxs.shape[0])
    adv[rs , idxs] += (adv[rs , idxs] & 1) << 4 # bit 5
    return( adv )

  def needprocess(self):
    for layer in self._keeps:
      if not self.has_data(layer):
        return True
    return False

    
  def process(self,remake=[]):
    change = False
    for layer in remake:
      void = self.get_data(layer,remake=True)
      change = True

    for layer in self._keeps:
      if self.has_data(layer):
        continue
      try:
        void = self.get_data(layer)
        change = True
      except IndexError:
        return False 
    if change:
      self.savez()  
    return True
  
  """
  def prod_barcode(self, key):
     
    #try:
    #  out = self.kwargs['barcodes'][self.name]
    #except:
    #  out = "2018 SLU EM EX 00"
    #self._data[key] = out
    
    out = self.name
    self._data[key] = out
  """
  
  def prod_imageraw(self, key):
    raw = self._load_raw() 
    self._data[key] = raw

  def prod_labels(self, key):
    seg=self.get_data('segmentation')
    out = skimage.measure.label(seg)
    self._data[key] = out

  def prod_leafraw(self, key):
    dscale = float(16)
    imgraw = self.get_data('imageraw')
    ds = skimage.transform.rescale(imgraw , 1/dscale)
    ds -= ds.min()
    ds /= ds.max()
    dk = numpy.hstack((numpy.argwhere(ds>-1)*0.001, 2**ds.reshape(-1,1)))
    clusterer = hdbscan.HDBSCAN(min_cluster_size=100)  
    pred = clusterer.fit_predict(dk).reshape(ds.shape)
    label_sum = 0
    for label in numpy.unique(pred):
      lsum = ds[pred==label].sum()
      if lsum > label_sum:
         bg_label = label
         label_sum = lsum 

    # relabel and find biggest
    bg = skimage.measure.label(pred==bg_label)
    bg_label = self.get_biggest_label(bg)

    # get objets inside background
    bg = bg == bg_label
    holes = numpy.logical_xor(scipy.ndimage.binary_fill_holes(bg),bg)
    objects = skimage.measure.label(holes)
    
    props = skimage.measure.regionprops(objects)
    
    # the best guess is bigger than 1000
    # if smaller than 6000
      # pick upper object
    candidate = [None, None]
    
    for prop in props:
      #print prop.label, prop.area
      if prop.area < 1000:
        #print 'area < 1000'
        continue

      if candidate[0] is None:
        #print 'no prop.. setting'
        candidate = [prop.label, prop]
        continue
      
      if prop.area > 5000:
          candidate = [prop.label, prop]
          continue

      if candidate[1].bbox[0] > prop.bbox[2]:        
        candidate = [prop.label, prop]
        continue
    bbox = (numpy.array(candidate[1].bbox)*dscale).astype(int)
    pad = 128
    self._data[key] = imgraw[bbox[0]-pad:bbox[2]+pad,bbox[1]-pad:bbox[3]+pad]

  def prod_leafrgb(self, key):
    rawleaf = self.get_data('leafraw')
    leafrgb = numpy.zeros(list(rawleaf.shape)+[3],dtype=float)
    demosaic_linear(rawleaf, leafrgb,bit_depth=14)
    self._data[key] = leafrgb 

  def prod_leafprops(self, key):
    props = {} 
    mask = self.get_data('mask')
    labels = self.get_data('labels')
    stain = self.get_data('stain')
    skprops = skimage.measure.regionprops(
          mask.astype(int), intensity_image=stain)[0]
    useprops = ['area','bbox','centroid','eccentricity','euler_number','extent','equivalent_diameter','perimeter','orientation']
    for prpkey in useprops:    
      props['rp_'+prpkey] = skprops[prpkey]
    props['b_height'], props['b_width'] = numpy.diff(
          numpy.array(props['rp_bbox']).reshape(2,2).T)[:,0]
    props['b_lesions_no'] = numpy.unique(labels).shape[0]-1
    props['b_lesions_area'] = (labels>0).sum()
    props['c_stain_max'] = stain.max()
    props['c_stain_min'] = stain.min()
    props['c_stain_mean'] = stain.mean()
    self._data[key] = numpy.array(props)

  def prod_lesions(self, key):
    lesions = {}
    labels = self.get_data('labels')    
    stain = self.get_data('stain')
    # 

    polar = rgb2pol(self.get_data('norminv'))
    # polar[~mask] = [0,0,0]
    blue = polar[:,:,1]
    dark = polar[:,:,2]
    mask = self.get_data('mask')
    advmask = self.get_mask_adv(mask)
    leafprops = self.get_data('leafprops')[()]
    leafbox = leafprops['rp_bbox']
    leafbase = leafbox[2]

    # distance from outer edge
    dst_oedge = scipy.ndimage.distance_transform_edt(advmask & 0b10)
    
    # distance from any edge
    dst_edge = scipy.ndimage.distance_transform_edt(advmask & 0b1)

    # distance from center line
    dst_cline = scipy.ndimage.distance_transform_edt(~advmask & 0b10000)
    
    dst = numpy.dstack((dst_oedge,dst_edge,dst_cline ))
    regprops = skimage.measure.regionprops(
          labels, intensity_image=blue)
    for prop in regprops:
      pd = {}
      if prop.label < 1:
        continue
      pmask = labels == prop.label
      
      useprops = ['label','area','bbox','centroid','eccentricity','euler_number','extent','equivalent_diameter','perimeter','orientation']
      for prpkey in useprops:    
        pd['rp_'+prpkey] = prop[prpkey]
      f = dst[pmask].astype(int)
      fs= blue[pmask]
      fs2= dark[pmask]
      pd['dst_oedge_max'], pd['dst_edge_max'], pd['dst_cline_max'] = f.max(0)
      pd['dst_oedge_min'], pd['dst_edge_min'], pd['dst_cline_min'] = f.min(0)
      pd['dst_oedge_mean'], pd['dst_edge_mean'], pd['dst_cline_mean'] = f.mean(0).astype(int)
      pd['c_blue_max'],pd['c_blue_min'], pd['c_blue_mean'] = fs.max(), fs.min(), fs.mean()
      pd['c_dark_max'],pd['c_dark_min'], pd['c_dark_mean'] = fs2.max(), fs2.min(), fs2.mean()
      pd['d_class_log10'] =  int(numpy.log10(pd['rp_area']))
      pd['b_ypos'] =  leafbase- pd['rp_centroid'][0]
      pd['b_height'], pd['b_width'] = numpy.diff(
          numpy.array(pd['rp_bbox']).reshape(2,2).T)[:,0]   
      for k, v in pd.items():
        if not k in lesions.keys():
          lesions[k] = []
        lesions[k].append(v)
    self._data[key] = numpy.array(lesions)  

  def prod_mask(self, key):
    norminv = self.get_data('norminv')
    pol = rgb2pol(norminv)
    d= skimage.morphology.disk(5)
    blue = pol[:,:,1]
    bmax = skimage.filters.rank.maximum(skimage.util.img_as_ubyte(blue),d )
    lum = pol[:,:,2]
    thresh = skimage.filters.threshold_otsu(lum)
    objects = skimage.measure.label(lum>thresh)
    leaf = self.get_biggest_label(objects)==objects
    holes = numpy.logical_xor(leaf, scipy.ndimage.binary_fill_holes(leaf))
    labels = skimage.measure.label(holes)
    nokeep = numpy.unique(labels[bmax < 180])
    for label in nokeep:
      if label:
        leaf[labels==label]= True
    self._data[key] = leaf

  def prod_norminvert(self,key):
    norm = self.get_data('norm')  
    ds = -numpy.log10(norm)
    ds -= ds.min() 
    ds += .0001
    ds /= ds.max()
    self._data[key] = ds

  def prod_white(self, key):
    white_small = self.get_data('white_small')
    self._data[key] = skimage.transform.rescale(white_small , 4,channel_axis=-1)

  def prod_whitesmall(self, key):
    rgb = self.get_data('leafrgb')
    rgb_ds = skimage.transform.rescale(rgb , 1/4.,channel_axis=-1)
    ds = rgb_ds - rgb_ds.min(axis=(0,1), keepdims=True)
    ds /= ds.max(axis=(0,1), keepdims=True)
    print(rgb_ds.shape)
    dk = numpy.hstack((numpy.argwhere(ds[:,:,0]>-1)*0.01, 2**ds.reshape(-1,3)))
    clusterer = hdbscan.HDBSCAN(min_cluster_size=100)  
    pred = clusterer.fit_predict(dk).reshape(ds.shape[0],ds.shape[1])
    areas = []
    pred += 1 # donbt exclude label 0 (background... likely)
    for prop in skimage.measure.regionprops(pred):
      areas.append([prop.bbox_area, prop.label])
    bg = sorted(areas)[-1][1]
    objects = skimage.measure.label(~(pred==bg))
    leaf = self.get_biggest_label(objects)
    bg = ~scipy.ndimage.binary_dilation(objects==leaf,skimage.morphology.disk(3))
    guess_image( rgb_ds, bg)
    self._data[key] = guess_image( rgb_ds, bg)

  def prod_norm(self, key):
    rgb = self.get_data('leafrgb')
    white = self.get_data('white')
    norm = ( rgb * 0.999) / white
    norm[norm > 1] = 1
    self._data[key] = norm 

  def prod_sampleprops(self, key):
    sample_dic={}
    sample_dic['name'] = self.name
    #print(self.name)
    if self.metadata is not None:
      
      rec = self.metadata[self.metadata.FILENAME==self.file_raw]
      #print(rec)
      sample_dic['treatment'] = rec.iloc[0].TREATMENT
      sample_dic['id'] =   rec.iloc[0].ID
   
    
    sd = {}
    for k, val in sample_dic.items():
      sd['a_'+k] = val
    self._data[key] = numpy.array(sd)
  """
  def old_prod_sampleprops(self, key):
    sample_dic={}
    bc = self.get_data('barcode')
    #print bc
    bc=str(bc).split() 
    #print '-------',bc
    try:
      sample_dic['species']=bc[3]
      if sample_dic['species'] == 'NC':
        treat = 'NC'
        rep= 0
      elif sample_dic['species'] == 'PT':
        treat = 'PC'
        rep = 0
      else:  
        treat = bc[5]
        rep = bc[6]
      nr = bc[-1]
      sample_dic['name'] = self.name
      sample_dic['treatment'] = treat
      sample_dic['repetition'] = rep
      sample_dic['img_no'] = nr
    except:
      sample_dic['name'] = self.name
      sample_dic['species'] ='Unknown'
      sample_dic['treatment'] = 'special'
      sample_dic['repetition'] = 0
      sample_dic['img_no'] = 0
    sd = {}
    for k, val in sample_dic.items():
      sd['a_'+k] = val
    self._data[key] = numpy.array(sd)
  """

  def prod_segmentation(self, key):
    stain = self.get_data('stain').copy()
    mask = self.get_data('mask')
    rads = [13,10,9,7,6,5,4,3,2,1]
    out = numpy.zeros(stain.shape, dtype=bool)
    stain[~mask] = stain[mask].min() # set outside to min
    for i in rads:
      print('c',i)
      cc= numpy.zeros(out.shape, dtype=int)
      disk = self.get_disk(i)
      
      tmp = scipy.ndimage.convolve(stain,disk)
      mp = tmp > (tmp.max()*0.1)
      mp = scipy.ndimage.binary_dilation(mp)
      mp = scipy.ndimage.binary_fill_holes(mp)
      mp = numpy.logical_or(mp, out)
      labels = skimage.measure.label(mp)
      labelnumbers = numpy.unique(labels)
     
      for label in labelnumbers:
        selection = labels==label
        selection[~mask] = False
        q = stain[selection]
        z = numpy.linspace(q.min(),q.max(),11)
        if (z[6]-z[0])<(0.001*selection.sum()**.5):
          #print 'weak leasion'
          continue
        ar = stain[selection]>z[6]
        cc[selection] += ar
      out = numpy.logical_or(out,cc)
    self._data[key] = out

  def prod_stain(self, key):
    nip = rgb2pol(self.get_data('norminv'))
    mask = self.get_data('mask')
    nip[~mask] = 0
    q = nip[:,:,1:].prod(2)
    self._data[key] = q
   
  @classmethod
  def load_raw(self, fname, args, metadata = None):
     
    abspath = os.path.abspath(fname)
    assert os.path.isfile(abspath)
    basename = os.path.basename(abspath)
    name = basename.split('.')[0] # basename.split('.')[0].split('_')[-1]
    datadir = args['datafiles']
    datadir = os.path.abspath(datadir)
    assert os.path.isdir(datadir)
    obj = self()  
    if metadata is not None:
      obj.metadata = metadata 
    obj.name = name
    obj.args = args 
    #obj._data['px_per_cm2'] = kwargs['px_per_cm2']
    obj.file_raw = abspath
    obj.file_npz = "{}/{}.npz".format(datadir, name)    
    if os.path.isfile(obj.file_npz):
      print('found npz!!!!!!')
      obj._load_npz()
    else:
      print( '***. ', obj.file_npz)
    return( obj )

  @classmethod  
  def load_npz(self, fname, args,metadata = None):
    abspath = os.path.abspath(fname)
    basename = os.path.basename(abspath)
    name = basename.split('.')[0]
    obj = self()   
    if metadata is not None:
      obj.metadata = metadata  
    obj.name = name
    obj.args = args
    obj.file_raw = None
    obj.file_npz = abspath
    if os.path.isfile(obj.file_npz):
      obj._load_npz()
    return( obj )
 
  def _load_npz(self):
    self.npz_obj = numpy.load(self.file_npz, allow_pickle=True)

  def _load_raw(self):
    """
    with rawkit.raw.Raw(filename=self.file_raw) as rawy:
      return numpy.array(rawy.raw_image(include_margin=True)) 
    """
    with rawpy.imread(self.file_raw) as rawy:
      bayer = rawy.raw_image.copy()
      print(bayer.max())
    return bayer    

  def _save_npz(self):
    dout = {}

    fname = self.file_npz #'data6/{}.npz'.format(self.name)
    print('saving {}'.format(fname))
    for key, val in self._data.items():
      if key in self._keeps:
        dout[key]  = val
    numpy.savez_compressed(fname, **dout)   
 

  def savez(self):
    for layer in self._keeps:
      if self.has_data(layer):
        void = self.get_data(layer)
    self._save_npz()

def rgb2pol(arr):
  #print arr.max(0).max(0)
  r = ((arr**2).sum(2))**0.5
  theta = numpy.arccos(arr[:,:,2]/r) / numpy.pi
  phi = numpy.arctan2(arr[:,:,1],arr[:,:,0]) / numpy.pi
  #print theta.min(), phi.min(), r.max()
  return numpy.dstack((2*phi,2*theta , r/(3**.5)))
  
def guess_image( arr, mask, use_border=True ):
  # make an educated guess about the image
  # use data where mask is true
  # useful for white balancing... 
  array = arr.copy()
  bwidth = 5
  array[~mask,:] = 0
  disk = skimage.morphology.disk(bwidth)
  bleaf = scipy.ndimage.binary_dilation(~mask,disk)
  border = numpy.logical_xor(bleaf, ~mask)
  q=numpy.array(numpy.where(border)).T  
  q = q[numpy.random.choice(q.shape[0], 1000),:].reshape(1000,1,2)
  t=numpy.array(numpy.where(~mask)).T 
  t = t[numpy.random.choice(t.shape[0], 1100),:].reshape(1,1100,2)
  dst= 1./((q-t)**2).sum(2)**2
  dst /= dst.sum(0).reshape(1,-1)
  vals = array[q[:,0,0],q[:,0,1]]
  nw = (numpy.atleast_3d(dst)*vals.reshape(-1,1,3)).sum(0)
  array[t[0,:,0],t[0,:,1],:] = nw
  nmask = ~bleaf
  nmask[q[:,0,0],q[:,0,1]] = True
  nmask[t[0,:,0],t[0,:,1]] = True
  idx_r, idx_c = numpy.where(nmask)
  xi_idx_r, xi_idx_c = numpy.where(~nmask)
  #linear interpolated
  intp= scipy.interpolate.griddata((idx_r,idx_c), 
            array[idx_r,idx_c],
            (xi_idx_r, xi_idx_c),
            method='linear')
  # nearest interpolation to fill where linear fails
  up = scipy.interpolate.griddata((idx_r,idx_c),
           array[idx_r,idx_c],
           (xi_idx_r, xi_idx_c),
           method='nearest')        
  nonfinite = ~numpy.isfinite(intp)
  intp[nonfinite] = up[nonfinite]
  array[xi_idx_r, xi_idx_c] = intp  

  return array

def demosaic_linear(bayer_array, out, bit_depth=8 ):
    # Simple linear debayering, I think...
    # !!! modifies "out" in place  
    # assumes RGGB layout
    # easy to do others

    # convert input to float for rggb 
    arr = bayer_array / float(2**bit_depth)
    #print(arr.max())
    # bggr 
    # just switch c ints

    # grbg (flip source array horiz before and output after) 
    
    # gbrg (flip and switch output layers   

    # red

    c = 0
    out[::2,::2,c] = arr[::2,::2] # direct from bayer
    out[::2,1:-2:2,c]= (arr[::2,:-3:2] + arr[::2,2::2] )/2.  # G1 pixels
    out[1:-1:2,:,c] = (out[:-2:2,:,c ] + out[2::2,:,c ])/ 2. # row average  
    out[-1,:,c] = out[-2,:,c] # copy second last row
    out[:,-1,c] = out[:,-2,c] # copy second last column

    # green
    c = 1

    out[::2,1::2,c]=  arr[::2,1::2] # direct from bayer
    out[1::2,::2,c]= arr[1::2,::2] # direct from bayer
    out[2::2,2::2,c] = (arr[1:-1:2,2::2] + arr[3::2,2::2]+ arr[2::2,1:-1:2]+ arr[2::2,3::2])/4.
    out[1:-1:2,1:-1:2,c]= ( arr[1:-1:2,2::2] + arr[1:-2:2,0:-2:2]+arr[2::2,1:-1:2] +arr[:-2:2,1:-1:2])/4. 
    out[0,2::2,c] = ( arr[0,1:-1:2] +arr[0,3::2]+arr[1,2::2])/3. # top missing
    out[-1,1:-1:2 ,c] =  (arr[-1,2::2]+arr[-1,:-2:2]+arr[-2,1:-1:2])/3.# bottom missing
    out[2::2,0 ,c] = (arr[1:-1:2,0]+arr[3::2,0]+arr[2::2,1])/3. # left missing
    out[1:-1:2,-1 ,c] = (arr[:-2:2,-1]+arr[2::2,-1]+arr[1:-1:2,-2])/3. # right missing
    out[0,0,c] = (arr[0,1]+arr[1,0])/2. # upper left
    out[-1,-1,c] = (arr[-1,-2]+arr[-2,-1])/2. # lower right

    # blue 
    c = 2
    out[1::2,1::2,c] = arr[1::2,1::2] # direct from bayer
    out[1::2,2::2,c] = (arr[1::2,1:-2:2]+arr[1::2,3::2])/2. # G2 pixels
    out[2::2,:,c] = (out[1:-2:2,:,c ] + out[3::2,:,c ])/ 2. # row average
    out[0,:,c] = out[1,:,c] # copy second row
    out[:,0,c] = out[:,1,c] # copy second column
    





def findfile( path, suffixes, args):
  # finds files recursively with supplied file suffix
  l = []
  if os.path.isdir(path):
    for fname in  glob.glob(path+'/*'):
      if args.verbose:
        print('found file {}'.format(fname))
      l.extend( findfile( fname ,suffixes, args) )
  else:
    if os.path.basename( path ).split( '.' )[-1] in  suffixes:
      l.append(path)
    
    #else:
    #  if args.verbose:
    #    print('wrong suffix', os.path.basename( path ).split( '.' )[-1], suffixes)
  return( l ) 

def tidypath(path):
  return os.path.abspath(os.path.expanduser(path))

def ask_project_dir(args):
  while True:  
    print ('Enter project directory: <q quits> ')
    project =  input('path:')
    if project == 'q':
      print('Quitting')
      raise SystemExit 
    return project

def ask_project_indir(args):
  while True:  
    print ('Enter location of input images: <q quits> ')
    indir =  input('path:')
    if indir == 'q':
      print('Quitting')
      raise SystemExit
    return indir

def main(args):
  if args.project is None:
    cfile = tidypath('limu.conf')
    if os.path.isfile(cfile ):
      args.project = os.path.dirname(cfile)
    else:     
      args.project = ask_project_dir(args)
  args.project = tidypath(args.project)
  if not os.path.isdir(args.project): 
    os.mkdir(args.project)

  args.conf_file= tidypath("{}/limu.conf".format(args.project))

 
  if os.path.isfile(args.conf_file):
    with open(args.conf_file, 'r') as fobj:
      conf_dict = json.load(fobj)
    for key, value in conf_dict.items():
      if key in args.__dict__.keys():
        if (args.__dict__[key] is None) or (args.__dict__[key] == False):
          args.__dict__[key] = value
      else:
        args.__dict__[key] = value
 
  else:
    if args.indir is None:
      args.indir = ask_project_indir(args)

    for sdir in ['datafiles','figures','imagesteps','outdata']:
      tmp = "{}/{}".format(args.project, sdir)
      args.__dict__[sdir] = tmp
      if not os.path.isdir(tmp):
        os.mkdir(tmp)

    with open(args.conf_file, 'w') as fobj:
      json.dump(args.__dict__, fobj, indent=4)
  
  # look for files 
  filesuffixes = ['cr2',] # canon raw
               #  'jpg','jpeg',
               #  'png',
               #  'tif','tiff',
               #   ] TODO implement non CR2
  uppercase = [suffix.upper() for suffix in filesuffixes]
  filesuffixes.extend(uppercase)
  infiles = findfile(args.indir,filesuffixes,args)
  metafile = '{}/{}'.format(args.project,'metadata.csv')
  if os.path.isfile(metafile):
    metadata = pandas.read_csv(metafile)
  else:
    print('building metadata file')
    metadata = pandas.DataFrame(columns=['FILENAME', 'ID','USE','PROCESSED', 'TREATMENT'])
  changed = False
  for i, fname in enumerate(infiles):
    
    if not (metadata.FILENAME == fname).any():
      print('adding record')
      if not changed:
        changed = True
      newrec = pandas.DataFrame({'FILENAME':[fname],'ID':[None], 'USE':[True],'PROCESSED':[False], 'TREATMENT':[None]})
      metadata = metadata.append(newrec, ignore_index = True) 
  print(metadata.head())
  if changed:
    metadata.to_csv(metafile, index=False)
  for idx, record in metadata.iterrows():
    if not record.PROCESSED:
      lim = LimuImage.load_raw(record.FILENAME, vars(args), metadata=metadata)
      if not lim.needprocess():
        metadata.loc[idx,'PROCESSED'] = True
        print('processed, updating table')
        changed = True
      else:
        print('Need work')
        if not record.USE:
          print('blacklisted')
        else:
          result = lim.process()
          if result:
            metadata.loc[idx,'PROCESSED'] = True
            step1name = '{}/{}_s1.png'.format(args.imagesteps, lim.name)
            if os.path.isfile(step1name):
              continue
            norm = lim.get_data('norm')
            mask = lim.get_data('mask')
            labels = skimage.color.label2rgb(lim.get_data('labels'))
            labels[mask < 1] = 0
            out = numpy.hstack((norm,labels))
            skimage.io.imsave(step1name, skimage.util.img_as_ubyte(out))
          else:
            metadata.loc[idx,'USE'] = False
          changed = True
        continue
    else:
      print('processed')
  
  if changed: 
    metadata.to_csv(metafile, index=False)
  else:
    print('no change')  
    
   
  #leafdatafile = '{}/{}'.format(args.outdata,'leafdata.csv') 
  lesionfile =  '{}/{}'.format(args.outdata,'lesiondata.csv') 
  print(f'looking for assembled data ({lesionfile})')
  assembledata = False
   
  if os.path.isfile(lesionfile) and not changed:
    print('found, reading')
    #leafdata = pandas.read_csv(leafdatafile)
    lesiondata = pandas.read_csv(lesionfile)
    
    z=numpy.unique(lesiondata['a_name'])
    for idx, record in metadata.iterrows():
      if record.USE:
        name = os.path.basename(record.FILENAME).split('.')[0]
        if name not in z:
          print(f'{name} NOT ok, new?')
          assembledata = True
          break
  else:
    lesiondata = None        
    
  if assembledata:
    print('not found or need update')
    #lesiondata = None # possibly dont reset but use exisitng and only add.... LATER
    lesiondatalist = []
    #"cnt = 0
    for idx, record in metadata.iterrows():
      #if cnt > 10 : break
      #cnt += 1
      
      print(f'checking {record.FILENAME}')
      if record.USE:
        
        lim = LimuImage.load_raw(record.FILENAME, vars(args), metadata=metadata)
        lesions = pandas.DataFrame(lim.get_data('lesions')[()])
        #print(lesions.rp_area)
        nrows = lesions.shape[0]
  
        # just to make sure, grap metadata from metadatafile
        for key, val in lim.get_data('sampleprops',remake=True)[()].items():     
          #print(key)   
          lesions.loc[:,key] = pandas.Series([val]*nrows, index=lesions.index)
        
          
        for key, val in lim.get_data('leafprops')[()].items():
          
          lesions.loc[:,'leaf_'+key] = pandas.Series([val]*nrows, index=lesions.index)
        
        
        lesions.sort_index(axis=1, inplace=True)
        lesiondatalist.append(lesions)
 
      else:
        print('dont add') 
    print(f'saving lesion data {lesionfile}')
    lesiondata= pandas.concat(lesiondatalist)
  
  # clustering
  if lesiondata is not None:
   if not 'z_clusterclass' in lesiondata.columns:    
      print('Clustering:')
      print('-compile data')
      data = []
      data.append(lesiondata['c_blue_max'])
      data.append(lesiondata['c_blue_max']-lesiondata['c_blue_min'])
      data.append(lesiondata['c_dark_max'])
      data.append(lesiondata['c_dark_max']-lesiondata['c_dark_min'])
      data.append(numpy.log10((lesiondata['rp_area']**.5)+.1))
      data.append(lesiondata['rp_eccentricity'])
      data = numpy.column_stack(data)
      print('-scaling data')
      from sklearn.preprocessing import StandardScaler as Scaler
      scaler = Scaler()      
      data = scaler.fit_transform(data)
      
      print('-clustering data')
      from sklearn.cluster import MiniBatchKMeans as Clusterer
      clusterer = Clusterer(n_clusters=30,verbose=True)
      classes = clusterer.fit_predict(data)
      
      print('-adding classes to data')
      lesiondata['z_clusterclass'] = pandas.Series(classes, index=lesiondata.index)
      
      
      print('save results')
      lesiondata.to_csv(lesionfile)
    
  print('Cluster plotting:')
  
  figures = args.figures
  if os.path.isfile('{}/cluster-00.png'.format(figures)):
    print('skip step')
  else:
      layout = numpy.array((15, 15)) # cols, rows
      res = 100
      images = {}
      count = layout.prod()
      selection = None
      print('selecting lesions')
      for classnumber in numpy.unique(lesiondata['z_clusterclass']):
        images[classnumber] = []
        subselection =    lesiondata.loc[lesiondata['z_clusterclass']==classnumber]
        if len(subselection) > count:
          rindex = numpy.random.choice(subselection.index.values, count)
          #print(rindex)
          subselection = subselection.loc[rindex]
        print(f'subselection is of size {subselection.shape}')
        if selection is None:
          selection = subselection
        else:
          selection= selection.append(subselection, ignore_index=True)
      selection = selection.sort_values(['a_name'])
      print('grabbing lesions')
      datadir = args.datafiles
      for name in numpy.unique(selection['a_name']):
        print(name)
        subselection = selection.loc[selection['a_name']==name]
        fname = '{}/{}.npz'.format(datadir,name)
          
        img = LimuImage.load_npz(fname,vars(args))
        for index, row in subselection.iterrows():
          label = row['rp_label']
          labels = img.get_data('labels')
          norm = img.get_data('norm')          
          sel = (labels == label)
          props = skimage.measure.regionprops(sel.astype(int))[0]
          box = numpy.array(props.bbox, dtype=int).reshape(2,2)
          pad = 10
          box += numpy.array([[-pad,-pad],[pad,pad]])
          size = numpy.diff(box,axis=0)
          ddi = size[0,0] - size[0,1]
          corr = numpy.zeros((2,2), dtype=int)
          cf = abs(ddi/2.)
          if ddi > 0:
            corr[:,1] = [-numpy.floor(cf),numpy.ceil(cf)]
          elif ddi < 0:
            corr[:,0] = [-numpy.floor(cf),numpy.ceil(cf)]
          box += corr
          size = numpy.diff(box,axis=0).sum(0)
          im = norm[box[0,0]:box[1,0],box[0,1]:box[1,1],:]
          sbox = sel[box[0,0]:box[1,0],box[0,1]:box[1,1]]
          imb = skimage.segmentation.mark_boundaries(im, sbox,color=(0,1,0))
          im = (imb+im)/2.
          try:
           im = skimage.transform.resize(im,output_shape=(res,res)).copy()
          except:
           im = numpy.zeros((res,res,3))
          images[row['z_clusterclass']].append(im)
          clnr = row['z_clusterclass']
          lcnt = len(images[row['z_clusterclass']])
          
          print(f'cluster {clnr} lesion {lcnt} of {count}')
        del img
           
      for classnumber in images.keys():
        image = None
        row = None
        for idx, im in enumerate(images[classnumber]):
          print(idx)
          if row is None:
            row = im
          else:
            row = numpy.hstack((row, im))
          if not ((idx+1) % layout[0]):
            if image is None:
              image = row
            else:
              image = numpy.vstack((image, row))
            row = None
        fname = '{}/cluster-{:02}.png'.format(figures, classnumber)  
        skimage.io.imsave(fname, image)       
  """
    if 'PROCESSED' in record:
      if record.PROCESSED:
        print('Processed')
      else:
        print('Not processed, but have db entry')
        
    else:
      metadata.loc[idx,'PROCESSED'] = False
      print('Not processed')
  metadata.to_csv(metafile, index=False)
  """
#  selection = metadata.query('USE == True and PROCESSED == False' )
#  for idx, record in selection.iterrows():
    
#    workload.append((str(record.FILENAME),vars(args).copy()))

#  import random
#  random.shuffle(workload)
#  for fname, args  in workload: 
#    print(process_multi(fname, args)) 
"""
  print(workload)
  pool = threading.Pool(processes=2)
  res = pool.starmap_async(process_multi, workload)
  pool.close()
  pool.join()
  print(res)
"""  
#  for fname, args in workload:
 #   process_multi(fname,args)

def process_multi(fname, args):
#  fname, args = bundle
   print(fname,args)
#    return True
   try:
  #if True:
    print('Try open!')
    lim = LimuImage.load_raw(fname,args)  
    print('Open OK!')
    changed = lim.process()
    if changed:
      norm = lim.get_data('norm')
      mask = skimage.color.label2rgb(lim.get_data('mask')) 
      labels = skimage.color.label2rgb(lim.get_data('labels'))    
      step1name = '{}/{}_s1.png'.format(args['imagesteps'], lim.name)
      labels[mask < 0] = 0
      out = numpy.hstack((norm,labels))
      skimage.io.imsave(step1name, skimage.util.img_as_ubyte(out))
      return 1
    else:
      return 0
   
   except:
    return -1
  
def cli():
  parser = argparse.ArgumentParser(
      prog='limu' ,
      description="""
        Tool to analyse images of cleared 
        and troptophan stained leaves to 
        assess leaf damage.
        """,
      epilog="Good luck analysing!")

  parser.add_argument(
    '-p', '--project', required=False, 
      type=str, 
      dest='project',
      help='path to projects directory, if not supplied one will be requested interactively. If limu.conf file found in current working directory, this will be used')
  parser.add_argument(
    '-i', '--input-dir', required=False, 
      type=str, 
      dest='indir', 
      help='path to infile root directory')

  parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        dest='verbose',
        help='Print more stuff'
    )
  parser.add_argument(
        '-r', '--recalculate',
        dest='recalculate',
        action='store_true',
        help='Force recalculation, NOT IMPLEMENTED'
    )
    

  args = parser.parse_args()
  main(args)
 
if __name__ == '__main__':
  cli()
    
