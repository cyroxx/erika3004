#!/usr/bin/env bash

pytest -m 'not hardware and not os_specific_dumb'
