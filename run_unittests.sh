#!/usr/bin/env bash

pytest --cov=erika tests/ -m 'not hardware and not os_specific_dumb'
