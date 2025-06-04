import os
import glob
import shutil
from pathlib import Path
from PIL import Image
from functools import reduce
from concurrent.futures import ThreadPoolExecutor, as_completed
from datasketch import MinHash, MinHashLSH
from tqdm import tqdm

def is_valid_jpg(jpg_file_path):
    if os.path.getsize(jpg_file_path) == 0:
        return False
    elif jpg_file_path.lower().endswith(".jpg"):
        with open(jpg_file_path, "rb") as f:
            f.seek(-2, 2)
            f_end = f.read()
            return f_end == b"\xff\xd9"
    else:
        return False

def avhash(image_path):
    image = Image.open(image_path).resize((8, 8), Image.LANCZOS).convert("L")
    avg = reduce(lambda x, y: x + y, image.getdata()) / 64.0
    hash_val = reduce(
        lambda x, y_z: x | y_z[1] << y_z[0],
        enumerate(map(lambda i: 0 if i < avg else 1, image.getdata())),
        0,
    )
    return hash_val

def hamming(h1, h2):
    x = h1 ^ h2
    return bin(x).count("1")

def avhash_to_set(hash_val):
    return set([str(i) for i in range(64) if (hash_val >> i) & 1 == 1])
def filter_similar_image_lsh(image_dir_path, save_image_dir_path, threshold=5, bucket_bits=16, num_perm=128):
    image_paths = glob.glob(f"{image_dir_path}/**/*.jpg", recursive=True) + \
                  glob.glob(f"{image_dir_path}/**/*.png", recursive=True)
    image_paths = [p for p in image_paths if is_valid_jpg(p)]
    
    # 多线程计算哈希，带进度条
    def calc_hash(p):
        return (p, avhash(p))
    
    image_hashes = []
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(calc_hash, p): p for p in image_paths}
        for f in tqdm(as_completed(futures), total=len(futures), desc="计算图像哈希"):
            image_hashes.append(f.result())
    
    # 分桶
    from collections import defaultdict
    buckets = defaultdict(list)
    for p, h in image_hashes:
        bucket_id = h >> (64 - bucket_bits)
        buckets[bucket_id].append((p, h))
    
    to_remove = set()
    # 桶内用LSH判断，带进度条
    bucket_items = list(buckets.items())
    for bucket_id, items in tqdm(bucket_items, desc="桶内LSH筛选"):
        if len(items) <= 1:
            continue
        
        lsh = MinHashLSH(threshold=1 - threshold / 64, num_perm=num_perm)
        minhashes = {}
        for idx, (p, h) in enumerate(items):
            s = avhash_to_set(h)
            m = MinHash(num_perm=num_perm)
            for d in s:
                m.update(d.encode('utf8'))
            lsh.insert(str(idx), m)
            minhashes[str(idx)] = (m, p)
        
        for idx in minhashes.keys():
            if minhashes[idx][1] in to_remove:
                continue
            results = lsh.query(minhashes[idx][0])
            for r in results:
                if r != idx and minhashes[r][1] not in to_remove:
                    orig_h1 = items[int(idx)][1]
                    orig_h2 = items[int(r)][1]
                    dist = hamming(orig_h1, orig_h2)
                    if dist <= threshold:
                        to_remove.add(minhashes[r][1])
    
    remaining = [p for p, _ in image_hashes if p not in to_remove]
    
    # 复制剩余文件，带进度条
    for p in tqdm(remaining, desc="复制保留图片"):
        save_path = Path(save_image_dir_path) / Path(p).relative_to(image_dir_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(p, save_path)

    print(f"完成：共保留 {len(remaining)} 张图片。")
        
filter_similar_image_lsh(r'D:\project\python\img_analyze\河北告警数据\img\sjz\入侵\入侵提醒事件导出20250423144943附件',r"D:\project\python\img_analyze\河北告警数据\img\sjz\入侵\入侵提醒事件导出20250423144943附件-tmp1")