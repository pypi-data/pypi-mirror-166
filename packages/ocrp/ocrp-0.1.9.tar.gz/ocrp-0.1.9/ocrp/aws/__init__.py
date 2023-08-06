#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 16:24:59 2022

@author: ross
"""
from ocrp.aws import trp
#from ocrp.aws import trp_utils
from ocrp.aws.call_textract import textract
from ocrp.aws.paragraph_detector import get_bounding_boxes, group_boundingBox_by_proximity, get_lines_in_boundingBox