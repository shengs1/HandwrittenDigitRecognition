"""Thu thập 600 ảnh nguyên bản, khóa validation/test trước suy luận; không tải model."""
from datetime import datetime, timezone
import hashlib
from io import BytesIO
import json
from pathlib import Path
import shutil
import sys
from urllib.request import Request, urlopen
import zipfile

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
 'bhmsds': ('wblachowski/bhmsds', '07d208e41923b061e338c241e59daacdd2752d53', '5e109303251854908f361e35bf260ebb30248fa9967bd70d2bf3703df11a5274'),
 'bitmap_numbers': ('KentoNishi/Bitmap-Numbers-Dataset', 'b83f099dd981cda1933f27726021594fa6995bb4', 'f5b0d42412d1a2e0d24a333ee6bdbfdf649a90074021a854a2333e6a5273583b'),
 'hwd1000': ('niklashenning/hwd-1000-dataset', '93b3ba9e45624ee557360229a42298eaa6b3a106', 'd59d694dba7df20ef95a28f8dfa6c403e97a103773d67b102840157124e60214')}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def get(url):
    with urlopen(Request(url, headers={'User-Agent': 'HandwrittenDigitRecognition-student-project'}), timeout=60) as response:
        return response.read()


def main():
    dest = ROOT/'data/external_handwriting'
    if (dest/'manifest.csv').exists():
        raise FileExistsError('Manifest đã khóa; không lấy mẫu lại hoặc ghi đè.')
    dest.mkdir(parents=True, exist_ok=True)
    provenance = dest/'provenance'
    provenance.mkdir(exist_ok=True)
    inventory, excluded = [], []
    for source, (repo, commit, expected_sha) in SOURCES.items():
        cache = ROOT/'tmp/handwriting_sources'/source
        cache.mkdir(parents=True, exist_ok=True)
        archive = cache/'source.zip'
        if not archive.exists():
            archive.write_bytes(get(f'https://codeload.github.com/{repo}/zip/{commit}'))
        assert sha(archive.read_bytes()) == expected_sha
        folder = cache/'repo'
        if not folder.exists():
            with zipfile.ZipFile(archive) as z:
                for item in z.infolist():
                    relative = Path(*Path(item.filename).parts[1:])
                    target = (folder/relative).resolve()
                    assert target.is_relative_to(folder.resolve())
                    if item.is_dir():
                        target.mkdir(parents=True, exist_ok=True)
                    else:
                        target.parent.mkdir(parents=True, exist_ok=True)
                        target.write_bytes(z.read(item))
        docs = provenance/source
        docs.mkdir(exist_ok=True)
        for name in ['README.md', 'LICENSE', 'dataset.csv']:
            if (folder/name).is_file():
                shutil.copyfile(folder/name, docs/name)
        if source == 'hwd1000':
            frame = pd.read_csv(folder/'dataset.csv')
            assert frame.image.is_unique and frame.label.isin(range(10)).all()
            candidates = [(str(row.image), int(row.label)) for row in frame.itertuples()]
            assert all(int(Path(path).stem.split('-')[0]) == label for path, label in candidates)
        elif source == 'bhmsds':
            candidates = [(p.relative_to(folder).as_posix(), label) for label in range(10)
                          for p in sorted((folder/'symbols').glob(f'{label}-*.png'))]
        else:
            candidates = [(p.relative_to(folder).as_posix(), label) for label in range(10)
                          for p in sorted((folder/str(label)).glob('*.bmp'))]
        for relative, label in candidates:
            path = folder/relative
            try:
                blob = path.read_bytes()
                with Image.open(BytesIO(blob)) as image:
                    image.verify()
                with Image.open(BytesIO(blob)) as image:
                    rgba = np.asarray(image.convert('RGBA'))
                    assert image.width >= 2 and image.height >= 2
                    if not (rgba[:, :, 3] > 0).any() or (rgba[:, :, :3].max() == rgba[:, :, :3].min()):
                        raise ValueError('Ảnh hằng/trống trước khi suy luận')
                    pixel_sha = sha(str(rgba.shape).encode()+rgba.tobytes())
                    inventory.append({'source': source, 'label': label, 'original_path': relative,
                                      'original_filename': path.name, 'width': image.width, 'height': image.height,
                                      'mode': image.mode, 'sha256': sha(blob), 'pixel_sha256': pixel_sha,
                                      'repository_commit': commit, 'writer_id': '', 'source_group_id': ''})
            except Exception as exc:
                excluded.append({'source': source, 'original_path': relative, 'label': label, 'reason': str(exc)})
        print(source, 'checked', len(candidates), flush=True)
    frame = pd.DataFrame(inventory)
    # Loại ảnh hỏng/trùng theo pixel trước model; giữ bản đầu có nhãn nhất quán.
    conflicts = frame.groupby('pixel_sha256').label.nunique()
    conflict_hashes = set(conflicts[conflicts > 1].index)
    eligible = frame.loc[~frame.pixel_sha256.isin(conflict_hashes)].copy()
    duplicate_mask = eligible.pixel_sha256.duplicated(keep='first')
    duplicate_rows = eligible.loc[duplicate_mask]
    eligible = eligible.loc[~duplicate_mask]
    frame.to_csv(provenance/'inventory.csv', index=False)
    pd.DataFrame(excluded, columns=['source','original_path','label','reason']).to_csv(provenance/'invalid_images.csv', index=False)
    duplicate_rows.to_csv(provenance/'duplicate_images.csv', index=False)
    frame.loc[frame.pixel_sha256.isin(conflict_hashes)].to_csv(provenance/'conflicting_labels.csv', index=False)
    rng = np.random.default_rng(42)
    selected = []
    for source in SOURCES:
        for label in range(10):
            pool = eligible.loc[(eligible.source == source) & (eligible.label == label)].sort_values('original_path')
            assert len(pool) >= 20, (source, label, len(pool))
            indices = rng.choice(len(pool), 20, replace=False)
            for order, index in enumerate(indices):
                row = pool.iloc[int(index)].to_dict()
                split = 'validation' if order < 10 else 'test'
                relative = Path(split)/source/str(label)/row['original_filename']
                target = dest/relative
                target.parent.mkdir(parents=True, exist_ok=True)
                original = ROOT/'tmp/handwriting_sources'/source/'repo'/row['original_path']
                shutil.copyfile(original, target)
                assert sha(target.read_bytes()) == row['sha256']
                selected.append({**row, 'path': relative.as_posix(), 'split': split})
    manifest = pd.DataFrame(selected)
    assert len(manifest) == 600 and manifest.sha256.nunique() == manifest.pixel_sha256.nunique() == 600
    assert manifest.groupby(['split','source','label']).size().eq(10).all()
    manifest.to_csv(dest/'manifest.csv', index=False)
    upstream = provenance/'bitmap_numbers/upstream_numbers'
    upstream.mkdir(exist_ok=True)
    upstream_sha = 'fb1f8fb90eddd4c43b22bbbdff7d146cfafc2d3a'
    for name in ['README.md', 'LICENSE.md']:
        cached = ROOT/'tmp/handwriting_sources/upstream_numbers'/name
        (upstream/name).write_bytes(cached.read_bytes() if cached.exists() else get(f'https://raw.githubusercontent.com/kensanata/numbers/{upstream_sha}/{name}'))
    lock = {'locked_at_utc': datetime.now(timezone.utc).isoformat(), 'seed': 42, 'numpy_version': np.__version__,
            'rule': 'Per source/digit sorted original path; random choice 20 without replacement; first 10 validation, next 10 test; all before model inference.',
            'manifest_sha256': sha((dest/'manifest.csv').read_bytes()), 'samples': 600,
            'per_split': {'validation': 300, 'test': 300}, 'image_bytes_unchanged': True,
            'writer_grouping_available': False,
            'grouping_limit': 'Selected repositories lack a reliable original writer/sheet mapping. Image-level split; identical decoded content excluded globally; writer independence cannot be claimed.',
            'inventory_count': len(frame), 'invalid_count': len(excluded), 'duplicate_count': len(duplicate_rows),
            'conflicting_pixel_hashes': len(conflict_hashes),
            'sources': {source: {'repository': repo, 'commit': commit, 'archive_sha256': digest} for source,(repo,commit,digest) in SOURCES.items()}}
    (dest/'sample_lock.json').write_text(json.dumps(lock, ensure_ascii=False, indent=2), encoding='utf-8')
    # Contact sheets chỉ resize preview; bytes 600 ảnh cấp cho preprocessing giữ nguyên.
    sheets = dest/'contact_sheets'
    sheets.mkdir(exist_ok=True)
    font = ImageFont.load_default(size=14)
    for (split, source), group in manifest.groupby(['split','source']):
        canvas = Image.new('RGB',(1500,1400),'#eeeeee')
        draw = ImageDraw.Draw(canvas)
        for position, row in enumerate(group.sort_values(['label','original_filename']).itertuples()):
            x, y = position%10*150, position//10*140
            image = Image.open(dest/row.path).convert('RGB')
            preview = ImageOps.contain(image,(130,110))
            canvas.paste(preview,(x+(150-preview.width)//2,y+22+(110-preview.height)//2))
            draw.text((x+3,y+2),f'{row.label} | {row.original_filename}',font=font,fill='black')
        canvas.save(sheets/f'{split}_{source}.png')
    print(json.dumps(lock, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
