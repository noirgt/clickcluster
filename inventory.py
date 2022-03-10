from inventory_modules.click_inventory import click_inventory
            
cluster = {
    1: ("10.102.0.193", "10.102.0.194"),
    2: ("10.102.0.194", "10.102.0.195"),
    3: ("10.102.0.195", "10.102.0.193")
    }

click_inventory(cluster)
