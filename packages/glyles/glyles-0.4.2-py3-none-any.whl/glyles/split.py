import logging

from glyles.converter import convert

glycans = []
known = None

with open("Lectins.fasta", "w") as lec, open("weights.tsv", "w") as weights:
    with open("/scratch/SCRATCH_SAS/roman/rindti/datasets/oracle/raw/all_arrays.csv", "r") as data:
        for i, line in enumerate(data.readlines()):
            print(f"\r{i}", end="")
            parts = line.strip().split(",")

            if i == 0:
                for j, p in enumerate(parts):
                    if convert(p, verbose=logging.FATAL)[0][1] != "":
                        glycans.append(i)
                continue

            lectin = parts[-1]
            if lectin in known:
                print(f">Lec{i:05d}\n{lectin}", file=lec)
                count = sum([len(v) >= 1 for j, v in enumerate(parts[:-1])])
