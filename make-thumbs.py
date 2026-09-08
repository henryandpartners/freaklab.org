#!/usr/bin/env python3
"""Generate compressed 500px thumbnails for all card images, upload to R2 under thumbs/ prefix.

Uses sips (macOS) for resize+recompress. Keeps full-res originals untouched.
Reads card keys from /tmp/card-keys.txt. Writes a manifest /tmp/thumb-map.tsv (key -> thumb key).
"""
import os, subprocess, sys, boto3
from botocore.config import Config

R2 = 'https://pub-6509346c2fdc47328b748c024f30f006.r2.dev/'
BUCKET = 'freak-lab'
TMP = '/tmp/thumbgen'
os.makedirs(TMP, exist_ok=True)

keys = [k.strip() for k in open('/tmp/card-keys.txt') if k.strip()]
print(f"{len(keys)} card keys", flush=True)

s3 = boto3.client('s3',
    endpoint_url=os.environ['CF_R2_ENDPOINT'],
    aws_access_key_id=os.environ['CF_R2_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['CF_R2_SECRET_ACCESS_KEY'],
    region_name='auto', config=Config(connect_timeout=15, read_timeout=120, retries={'max_attempts':3}))

def thumb_key(k):
    base, ext = os.path.splitext(k)
    return f"thumbs/{base}.jpg"

manifest = open('/tmp/thumb-map.tsv','w')
done = fail = skip = 0
for i, k in enumerate(keys):
    tk = thumb_key(k)
    # skip if already uploaded (check HEAD via list? use get_object catch)
    try:
        s3.head_object(Bucket=BUCKET, Key=tk)
        skip += 1
        manifest.write(f"{k}\t{tk}\n")
        continue
    except Exception:
        pass
    src = os.path.join(TMP, os.path.basename(k))
    dst = os.path.join(TMP, 'th_' + os.path.basename(k).rsplit('.',1)[0] + '.jpg')
    try:
        s3.download_file(BUCKET, k, src)
    except Exception as e:
        fail += 1
        print("DLFAIL", k, str(e)[:80], flush=True)
        continue
    try:
        subprocess.run(['sips','-Z','500','-s','format','jpeg','-s','formatOptions','72', src, '--out', dst],
                       capture_output=True, timeout=60)
        if not os.path.exists(dst) or os.path.getsize(dst) < 500:
            raise RuntimeError('sips produced no output')
    except Exception as e:
        fail += 1
        print("SIPSFAIL", k, str(e)[:80], flush=True)
        continue
    try:
        s3.upload_file(dst, BUCKET, tk, ExtraArgs={'ContentType':'image/jpeg','CacheControl':'public,max-age=31536000'})
        manifest.write(f"{k}\t{tk}\n")
        done += 1
    except Exception as e:
        fail += 1
        print("UPFAIL", k, str(e)[:80], flush=True)
        continue
    os.remove(src); os.remove(dst)
    if (i+1) % 20 == 0: print(f"progress {i+1}/{len(keys)} done={done} fail={fail} skip={skip}", flush=True)

manifest.close()
print(f"DONE ok={done} fail={fail} skip={skip}", flush=True)
