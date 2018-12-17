import argparse
import os
import re

parser = argparse.ArgumentParser()
parser.add_argument('-trains', help='train input dirs', nargs='+', required=True)
parser.add_argument('-valids', help='valid input dirs', nargs='+', required=True)
parser.add_argument('-audio', default='segment', help='audio directory')
parser.add_argument('-caption', default='caption', help='caption path')

args = parser.parse_args()
prefix = os.path.commonprefix(args.trains + args.valids)

ZH = re.compile('[\u4e00-\u9fa5]|[A-Za-z]|[0-9]')

def tokenize(line):
    return " ".join(ZH.findall(line)) + '\n'

def write(dirs, srcf, tgtf):

    srcf = os.path.join(prefix, srcf)
    tgtf = os.path.join(prefix, tgtf)
    srcf = open(srcf, 'w')
    tgtf = open(tgtf, 'w')
    for _dir in dirs:
        tgt = os.path.join(_dir, args.caption)
        with open(tgt) as f:
            lines = f.readlines()
            lines = [tokenize(line) for line in lines]
        audio_path = os.path.join(_dir, args.audio)
        infix = os.path.relpath(audio_path, prefix)
        files = sorted(os.listdir(audio_path), key=lambda x: int(x.split('.')[0]))
        for f in files:
            num = int(f.split('.')[0])
            print(num)
            srcf.write(os.path.join(infix, f) + '\n')
            tgtf.write(lines[num])
    srcf.close()
    tgtf.close()

write(args.trains, 'src-train.txt', 'tgt-train.txt')
write(args.valids, 'src-val.txt', 'tgt-val.txt')
