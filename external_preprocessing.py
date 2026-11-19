"""Các biến thể nhỏ để đánh giá ảnh ngoài; không thay API baseline của app.

Block32 gần cách đếm 4×4 của UCI nhưng không tái hiện toàn bộ chuẩn hóa NIST.
Tham số là cố định theo protocol; không chọn theo nhãn/xác suất của từng ảnh.
"""
from io import BytesIO
import warnings

import numpy as np
from PIL import Image, ImageFilter, ImageOps, UnidentifiedImageError

VARIANTS = ['baseline', 'gray_bbox', 'gray_com', 'binary35', 'binary50', 'binary35_thick', 'gray_wide']


def read_ink(data, background='Tự động'):
    if not data:
        raise ValueError('File ảnh rỗng.')
    if len(data) > 10*1024*1024:
        raise ValueError('Ảnh vượt 10 MB.')
    if background not in ['Tự động','Nền sáng, nét tối','Nền tối, nét sáng']:
        raise ValueError('Chế độ màu nền không hợp lệ.')
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('error', Image.DecompressionBombWarning)
            with Image.open(BytesIO(data)) as opened:
                if opened.format not in {'PNG','JPEG','BMP','WEBP'}:
                    raise ValueError('Chỉ hỗ trợ PNG, JPEG, BMP và WebP.')
                if opened.width*opened.height > 16_000_000:
                    raise ValueError('Ảnh quá lớn (tối đa 16 triệu pixel).')
                rgba = ImageOps.exif_transpose(opened).convert('RGBA')
    except (OSError, UnidentifiedImageError, Image.DecompressionBombError, Image.DecompressionBombWarning) as exc:
        raise ValueError('Không đọc được file ảnh hợp lệ.') from exc
    alpha = np.asarray(rgba)[:,:,3]
    visible = alpha > 64
    if not visible.any():
        raise ValueError('Ảnh trong suốt hoặc trống.')
    border_alpha = np.concatenate([alpha[0],alpha[-1],alpha[:,0],alpha[:,-1]])
    visible_gray = np.asarray(rgba.convert('L'))[visible]
    matte = 0 if border_alpha.mean()<128 and np.median(visible_gray)>=128 else 255
    composite = Image.new('RGBA',rgba.size,(matte,matte,matte,255))
    composite.alpha_composite(rgba)
    original = composite.convert('RGB')
    gray = np.asarray(original.convert('L'), dtype=np.float32)
    border = np.concatenate([gray[0],gray[-1],gray[:,0],gray[:,-1]])
    bg = float(np.median(border))
    light = bg>=127.5 if background=='Tự động' else background=='Nền sáng, nét tối'
    ink = np.maximum(bg-gray if light else gray-bg,0)
    contrast = float(ink.max())
    if contrast<25:
        raise ValueError('Ảnh trống hoặc tương phản quá thấp.')
    mask = ink>=max(12,0.2*contrast)
    if mask.sum()<3:
        raise ValueError('Không đủ nét chữ để nhận dạng.')
    # Chuẩn hóa đỉnh theo tương phản trước resize, không phải StandardScaler.
    ink = np.where(mask,ink*255/contrast,0).clip(0,255).astype(np.uint8)
    ys,xs = np.where(mask)
    box = (int(xs.min()),int(ys.min()),int(xs.max())+1,int(ys.max())+1)
    return original, Image.fromarray(ink).crop(box), {
        'background':'Nền sáng → đảo nét' if light else 'Nền tối → giữ nét sáng',
        'original_size':list(original.size),'crop_box':list(box)}


def centered_canvas(crop, side, max_width, max_height, center_mass):
    factor = min(max_width/crop.width,max_height/crop.height)
    size = (max(1,round(crop.width*factor)),max(1,round(crop.height*factor)))
    glyph = crop.resize(size,Image.Resampling.BILINEAR)
    canvas = Image.new('L',(side,side),0)
    canvas.paste(glyph,((side-size[0])//2,(side-size[1])//2))
    if center_mass:
        array = np.asarray(canvas,dtype=float)
        ys,xs = np.indices(array.shape)
        occupied_y,occupied_x = np.where(array>0)
        dx = int(np.clip(round((side-1)/2-(xs*array).sum()/array.sum()),-occupied_x.min(),side-1-occupied_x.max()))
        dy = int(np.clip(round((side-1)/2-(ys*array).sum()/array.sum()),-occupied_y.min(),side-1-occupied_y.max()))
        canvas = canvas.transform((side,side),Image.Transform.AFFINE,(1,0,-dx,0,1,-dy),resample=Image.Resampling.NEAREST,fillcolor=0)
    return canvas


def preprocess_external_image(data, background='Tự động', variant='gray_com'):
    if variant=='baseline':
        # Import muộn tránh vòng import khi app gọi preprocessing mới cho upload.
        from app import preprocess_uploaded_image
        return preprocess_uploaded_image(data,background)
    if variant not in VARIANTS and variant!='mnist28':
        raise ValueError('Biến thể preprocessing không hợp lệ.')
    original,crop,info = read_ink(data,background)
    if variant=='mnist28':
        canvas = centered_canvas(crop,28,20,20,True)
        pixels = np.asarray(canvas,dtype=np.float32)
    else:
        width = 28 if variant=='gray_wide' else 24
        canvas = centered_canvas(crop,32,width,32,variant!='gray_bbox')
        values = np.asarray(canvas,dtype=np.float32)/255
        if variant.startswith('binary'):
            threshold = .5 if variant=='binary50' else .35
            values = (values>=threshold).astype(np.float32)
            if variant=='binary35_thick':
                values = np.asarray(Image.fromarray(np.uint8(values*255)).filter(ImageFilter.MaxFilter(3)),dtype=np.float32)/255
        pixels = values.reshape(8,4,8,4).sum(axis=(1,3)).astype(np.float64)
    if not np.isfinite(pixels).all() or np.count_nonzero(pixels)<3:
        raise ValueError('Ảnh sau xử lý không còn đủ nét chữ.')
    info.update({'variant':variant,'pixel_min':float(pixels.min()),'pixel_max':float(pixels.max())})
    return original,pixels,info
