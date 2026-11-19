"""Fixture tổng hợp chỉ kiểm hợp đồng ảnh; không phải dữ liệu đo accuracy thực tế."""
from io import BytesIO
from pathlib import Path
import hashlib
import json
import sys
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageOps
from sklearn.pipeline import Pipeline
from streamlit.testing.v1 import AppTest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from external_preprocessing import VARIANTS, preprocess_external_image
import app


def encode(image):
    buffer=BytesIO(); image.save(buffer,format='PNG'); return buffer.getvalue()


class NewPreprocessingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.image=Image.new('RGB',(100,120),'white')
        ImageDraw.Draw(cls.image).line([(20,15),(70,15),(35,105)],fill='black',width=9)

    def test_each_variant_domain_and_no_fit(self):
        with patch.object(Pipeline,'fit',side_effect=AssertionError('No fit')):
            for variant in [*VARIANTS,'mnist28']:
                pixels=preprocess_external_image(encode(self.image),variant=variant)[1]
                expected=(28,28) if variant=='mnist28' else (8,8)
                self.assertEqual(pixels.shape,expected)
                self.assertTrue(np.isfinite(pixels).all())
                self.assertGreaterEqual(pixels.min(),0)
                self.assertLessEqual(pixels.max(),255 if variant=='mnist28' else 16)
                if variant.startswith('binary'):
                    np.testing.assert_array_equal(pixels,np.floor(pixels))

    def test_binary_blocks_count_known_rectangle(self):
        image=Image.new('L',(50,50),255)
        ImageDraw.Draw(image).rectangle((10,10,21,33),fill=0)
        expected=np.zeros((8,8)); expected[:,2:6]=16
        for variant in ['binary35','binary50','gray_com']:
            np.testing.assert_allclose(preprocess_external_image(encode(image),variant=variant)[1],expected)

    def test_light_dark_and_alpha_equivalence(self):
        transparent=[]
        for color in ['black','white']:
            image=Image.new('RGBA',(100,120),(0,0,0,0))
            ImageDraw.Draw(image).line([(20,15),(70,15),(35,105)],fill=color,width=9)
            transparent.append(image)
        for variant in ['gray_bbox','gray_com','binary35','mnist28']:
            original=preprocess_external_image(encode(self.image),variant=variant)[1]
            for image in [ImageOps.invert(self.image),*transparent]:
                np.testing.assert_array_equal(preprocess_external_image(encode(image),variant=variant)[1],original)

    def test_large_padding_translation_and_stroke_width(self):
        for width in [2,14]:
            glyph=Image.new('L',(60,90),255)
            ImageDraw.Draw(glyph).line([(8,8),(50,8),(20,80)],fill=0,width=width)
            a=Image.new('L',(120,140),255); a.paste(glyph,(10,20))
            b=Image.new('L',(300,300),255); b.paste(glyph,(210,180))
            for variant in ['gray_bbox','gray_com','binary35','mnist28']:
                left=preprocess_external_image(encode(a),variant=variant)[1]
                right=preprocess_external_image(encode(b),variant=variant)[1]
                np.testing.assert_array_equal(left,right)

    def test_invalid_blank_low_contrast_and_limits(self):
        low=Image.new('L',(50,50),255); ImageDraw.Draw(low).line((10,10,40,40),fill=240,width=4)
        cases=[b'',b'broken',encode(Image.new('L',(50,50),255)),encode(Image.new('RGBA',(50,50),(0,0,0,0))),encode(low)]
        for data in cases:
            with self.assertRaises(ValueError):preprocess_external_image(data,variant='mnist28')
        with self.assertRaises(ValueError):preprocess_external_image(b'x'*(10*1024*1024+1),variant='gray_com')
        with self.assertRaises(ValueError):preprocess_external_image(encode(self.image),background='unknown',variant='gray_com')
        with self.assertRaises(ValueError):preprocess_external_image(encode(self.image),variant='unknown')


class CollectedDataTests(unittest.TestCase):
    def test_manifest_balance_integrity_and_no_cross_split_duplicates(self):
        folder=ROOT/'data/external_handwriting'
        frame=pd.read_csv(folder/'manifest.csv')
        lock=json.loads((folder/'sample_lock.json').read_text())
        self.assertEqual(hashlib.sha256((folder/'manifest.csv').read_bytes()).hexdigest(),lock['manifest_sha256'])
        self.assertEqual(len(frame),600)
        self.assertTrue(frame.groupby(['split','source','label']).size().eq(10).all())
        self.assertEqual(frame.sha256.nunique(),600)
        self.assertEqual(frame.pixel_sha256.nunique(),600)
        for item in frame.itertuples():
            self.assertEqual(hashlib.sha256((folder/item.path).read_bytes()).hexdigest(),item.sha256)


class ExternalIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config=app.read_external_registry()
        cls.out=ROOT/'outputs'/cls.config['optimization_run']
        cls.image=Image.new('RGB',(100,120),'white')
        ImageDraw.Draw(cls.image).line([(20,15),(70,15),(35,105)],fill='black',width=9)

    def test_specialist_shape_probabilities_and_no_double_scale(self):
        entry=self.config['specialist']
        path=ROOT/'models'/entry['path']; stat=path.stat()
        with patch.object(Pipeline,'fit',side_effect=AssertionError('No fit')):
            pipeline=app.load_saved_pipeline(str(path),entry['sha256'],stat.st_mtime_ns,stat.st_size,784)
            pixels=preprocess_external_image(encode(self.image),variant='mnist28')[1]
            prediction,probabilities=app.predict_digit(pipeline,pixels)
            X=pixels.reshape(1,784)
            self.assertEqual(prediction,int(pipeline.predict(X)[0]))
            np.testing.assert_allclose(probabilities['Xác suất'],pipeline.predict_proba(X)[0],atol=1e-7)
            self.assertEqual(probabilities.index.tolist(),list(map(str,range(10))))
            with self.assertRaises(ValueError):app.predict_digit(pipeline,np.zeros((8,8)))
            with self.assertRaises(ValueError):app.predict_digit(pipeline,np.full((28,28),256))

    def test_specialist_is_upload_only_and_switch_clears_result(self):
        path=ROOT/'data/external_handwriting/validation/hwd1000/7/7-007.png'
        script=('from io import BytesIO\nfrom pathlib import Path\nfrom unittest.mock import patch\nimport app\n'
                f'data=Path({str(path)!r}).read_bytes()\n'
                "with patch.object(app.st,'file_uploader',return_value=BytesIO(data)):\n    app.main()")
        with patch.object(Pipeline,'fit',side_effect=AssertionError('No fit')):
            at=AppTest.from_string(script,default_timeout=30).run()
            self.assertNotIn(app.EXTERNAL_MODEL_NAME,at.selectbox(key='model').options)
            at.selectbox(key='source').select('Tải ảnh từ máy').run()
            self.assertIn(app.EXTERNAL_MODEL_NAME,at.selectbox(key='model').options)
            at.selectbox(key='model').select('mlp_mnist').run()
            at.button(key='predict').click().run()
            self.assertFalse(at.exception)
            self.assertEqual(at.session_state['prediction_result']['model'],'mlp_mnist')
            rendered='\n'.join(item.value for item in at.markdown)
            self.assertIn('28 × 28 pixel · 0–255',rendered)
            self.assertIn('Sau tiền xử lý · 28×28',rendered)
            technical=next(item.proto.body for item in at.get('html') if '<div class="technical-info">' in item.proto.body)
            for text in ['MNIST train','54.000','784','MinMaxScaler','128 → 64']:
                self.assertIn(text,technical)
            self.assertIn('bộ dữ liệu MNIST train',technical)
            self.assertIn('96,67%',rendered)  # Thẻ Digits chính thức giữ nguyên.
            at.selectbox(key='model').select('knn').run()
            self.assertNotIn('prediction_result',at.session_state)
            at.button(key='predict').click().run()
            self.assertFalse(at.exception)
            at.selectbox(key='source').select('Ảnh test Digits').run()
            self.assertNotIn(app.EXTERNAL_MODEL_NAME,at.selectbox(key='model').options)
            self.assertNotIn('prediction_result',at.session_state)

    def test_current_app_matches_locked_external_test_predictions(self):
        # Chỉ replay sau khóa, không chọn lại preprocessing/mô hình từ test.
        lock=json.loads((self.out/'selection_lock.json').read_text())
        self.assertEqual(self.config['shared_variant'],lock['shared_variant'])
        frame=pd.read_csv(ROOT/'data/external_handwriting/manifest.csv')
        chosen=frame[frame.split.eq('test')].iloc[0]
        data=(ROOT/'data/external_handwriting'/chosen.path).read_bytes()
        for model in ['knn','logreg_raw','mlp','mlp_mnist']:
            variant='mnist28' if model=='mlp_mnist' else lock['shared_variant']
            entry=self.config['specialist'] if model=='mlp_mnist' else app.read_model_registry()['models'][model]
            path=ROOT/'models'/entry['path']; stat=path.stat()
            count=784 if model=='mlp_mnist' else 64
            pipeline=app.load_saved_pipeline(str(path),entry['sha256'],stat.st_mtime_ns,stat.st_size,count)
            pixels=app.preprocess_upload_for_model(data,'Tự động',model,self.config)[1]
            predicted,_=app.predict_digit(pipeline,pixels)
            stored=pd.read_csv(self.out/f'final_test/handwriting_test__{model}--{variant}__predictions.csv')
            self.assertEqual(predicted,int(stored.loc[stored.sample_id.eq(chosen.path),'predicted_label'].item()))

    def test_external_registry_cannot_substitute_model_outside_selection_lock(self):
        config=json.loads(json.dumps(self.config))
        config['specialist']['sha256']='0'*64
        with tempfile.TemporaryDirectory(dir=ROOT/'tmp') as directory:
            path=Path(directory)
            (path/'external_registry.json').write_text(json.dumps(config),encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'artifact đã khóa'):
                app.read_external_registry(path)


if __name__=='__main__':
    unittest.main()
