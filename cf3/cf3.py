#!/usr/bin/env python3
# extract features from web pages for further classification
import binascii
import hashlib
import math
import os
import sys

from collections import defaultdict
from math import e, log

from lxml import html

#from skbio.diversity import alpha_diversity
#import numpy as np

"""
Fields for the hash:

mc: meta count
sc: script count
ts: title size
tl: len of tag vector
ti: tag vector int
hs: head size (rounded)
bs: body size (rounded)
sz: total size(rounded)
"""

def parse_file(f:"str", verbose=False):
    c = get_content(f)
    parse_raw(c, verbose)

def parse_raw(c:"str", verbose=False):
    try:
        t = get_tree(c)
    except Exception:
        print("ERROR parsing")
        raise
    try:
        calculate_hash(c, t, verbose)
    except Exception:
        print("ERROR hashing")
        raise

def get_content(f:"str") -> "unicode":
    with open(f, 'rb') as ff:
        return ff.read()

def get_tree(c:"str"):
    return html.fromstring(c)

def get_tag_vector(tree) -> "list":
    return [node.tag for node in tree.iter('*')]

def get_tag_count(tag:"str", tv:"list") -> "int":
    return len([x for x in tv if x == tag])

def get_tag_vector_int(tv:"list") -> "int":
    s = ','.join(tv)
    hs = binascii.hexlify(s[:500].encode('utf-8'))
    return int(hs, 16) % 100

def get_title_size(tree):
    title = tree.find(".//title")
    if title is None:
        return 0
    return len(title.text) if title.text is not None else 0

def get_head_size(tree):
    try:
        return len(tree.head.text_content())
    except IndexError:
        return 0

def get_body_size(tree):
    try:
        return len(tree.body.text_content())
    except IndexError:
        return 0

def get_fingerprint(mc, sc, ts, tl, ti, hs, bs, sz):
    return f"{mc}-{sc}-{ts}-{tl}-{ti}-{hs}-{bs}-{sz}"

def get_hash(s:"str") -> "str":
    return hashlib.md5(s.encode("utf-8")).hexdigest()

def calculate_hash(c, t, verbose=False) -> "str":
    tv = get_tag_vector(t)
    ts = get_title_size(t)
    mc = get_tag_count("meta", tv)
    sc = get_tag_count("script", tv)
    tl = len(tv)
    ti = get_tag_vector_int(tv)
    hs = next_power_of_2(get_head_size(t))
    bs = next_power_of_2(get_body_size(t))
    sz = next_power_of_2(len(c))
    fpr = get_fingerprint(ts, mc, sc, tl, ti, hs, bs, sz)
    cf3 = get_hash(fpr)

    if verbose:
        print("title size:", ts)
        print("meta:",  mc)
        print("script:", sc)
        print("head size:", hs)
        print("body size:", bs)
        print("total size:", sz)
        print("tag vector summary:", ti)
        print("tag vector:", ','.join(tv))
        print()
        print("CF3:", fpr)
        print("md5:", cf3)
    else:
        print(cf3)

    return cf3


def next_power_of_2(x):
    return 1 if x == 0 else 2**(x - 1).bit_length()


# not used in current spec, for further research -----
def roundup(x):
    return int(math.ceil(x / 25.0)) * 25

def calculate_entropy(f:"str"):
    tv = get_tag_vector(get_tree(get_content(f)))
    c = get_counts(tv)
    a = get_alpha('simpson', c)
    print("%d" % int(round(100 * float(a))))


def entropy(labels: "list", base=None):
    val, counts = np.unique(labels, return_counts=True)
    norm_counts = counts / counts.sum()
    base = e if base is None else base
    return -(norm_counts * np.log(norm_counts)/np.log(base)).sum()

def get_alpha(metric:"str", counts:"list") -> "float":
    return alpha_diversity(metric, counts)

def get_counts(l: "list") -> "list":
    cnt = defaultdict(int)
    for item in l:
        cnt[item] += 1
    return list(cnt.values())
# ---------------------------------------------------

def run():
    if len(sys.argv) == 1: # and os.isatty(sys.stdin.fileno()):
        raw = sys.stdin.read()
        parse_raw(raw)

    elif len(sys.argv) == 2:
        f = sys.argv[1]
        parse_file(f, verbose=True)

    elif len(sys.argv) == 3:
        cmd = sys.argv[2]
        if cmd == "hash":
            parse_file(f)
        elif cmd == "entropy":
            calculate_entropy(f)

if __name__ == "__main__":
    run()

