#!/usr/bin/env bash

python3 -m tests.erika_mock_unittest
python3 -m tests.erika_image_render_unittest
python3 -m tests.cli_unittest
python3 -m tests.util_unittest
python3 -m tests.image_converter_unittest
