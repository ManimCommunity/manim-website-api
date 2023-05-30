#!/bin/bash
set -e

mkdir -p public/
cp requirements.txt public/requirements.txt
cp -r api/ public/
