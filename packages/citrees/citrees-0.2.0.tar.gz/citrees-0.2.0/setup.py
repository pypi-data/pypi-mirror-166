#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: Robert Milletich(rmill040)
# Mail: rmill040@gmail.com
# Created Time: 2022-9-7 10:17:34
#############################################


from setuptools import setup, find_packages

setup(
  name = "citrees",
  version = "0.2.0",
  keywords = ("pip", "citree","", "regression", "classification"),
  description = "conditional inference tree",
  long_description = "Bayesian conditional inference trees and forests in Python",
  license = "MIT Licence",

  url = "https://github.com/rmill040/citrees",
  author = "Robert Milletich(rmill040)",
  author_email = "rmill040@gmail.com",

  packages = find_packages(),
  include_package_data = True,
  platforms = "any",
  install_requires = []
)
