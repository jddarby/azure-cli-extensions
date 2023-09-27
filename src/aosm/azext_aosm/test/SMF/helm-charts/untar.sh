#!/bin/bash
# for tarfile in *.tgz; do
#     tar -xzf $tarfile
# done

for mydir in fed*; do
    cd $mydir
    cp values.yaml "../${mydir}-mapping-values.yaml"
    cd ..
done
