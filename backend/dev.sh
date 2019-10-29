#!/usr/bin/env bash

./env/bin/gunicorn app:app --reload --timeout 10000