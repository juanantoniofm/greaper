#!/bin/bash

nosetests test_*py --with-coverage3 --cover3-exclude=mock,*strptime,*xml.dom*,argparse
