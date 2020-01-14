#!/usr/bin/env bash

pytest --cov=erika tests/ --cov-report=html --html=report.html -m 'not hardware'
