#!/bin/bash
while true;
do
  python3.7 pihub.py && break;
  echo Error. 30 sec timeout
  sleep 30
done
