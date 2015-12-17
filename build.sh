#!/bin/bash

MY_PATH=`dirname "$0"`
DIR=`( cd "$MY_PATH" && pwd )`
pushd $DIR

mkdir -p out

python2.7 gen_list.py
python2.7 gen_all_messages.py

python2.7 setup.py build
sudo python2.7 setup.py install

popd
