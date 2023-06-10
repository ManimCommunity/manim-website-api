#!/bin/bash
set -e

poetry export -f requirements.txt --without-hashes -o requirements.txt

mkdir -p public/
cp requirements.txt public/requirements.txt
cp -r api/ public/
