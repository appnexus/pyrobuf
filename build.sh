#!/bin/bash

MY_PATH=`dirname "$0"`
DIR=`( cd "$MY_PATH" && pwd )`
pushd $DIR

mkdir -p out

python gen_list.py
python gen_all_messages.py

python setup.py build
sudo python setup.py install

popd
