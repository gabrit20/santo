#!/bin/bash
git add .
git commit -m "*"
git checkout --ours .
git pull origin master
git push -u origin --all
