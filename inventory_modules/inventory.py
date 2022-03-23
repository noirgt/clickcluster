#!/usr/bin/python3
from click_inventory import click_inventory
import os
import yaml

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

with open(os.path.join(__location__, '../config.yml')) as conf_file:
    cluster = yaml.full_load(conf_file)

click_inventory(cluster)
