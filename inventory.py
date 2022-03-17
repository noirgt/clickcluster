#!/usr/bin/python3
from inventory_modules.click_inventory import click_inventory
            
cluster = {
    1: ("10.102.3.11", "10.102.3.13"),
    2: ("10.102.3.12", "10.102.3.11"),
    3: ("10.102.3.13", "10.102.3.12")
    }

click_inventory(cluster)
