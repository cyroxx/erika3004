#!/usr/bin/env bash

pytest --cov=erika tests/ --cov-report=html -m 'not hardware'
