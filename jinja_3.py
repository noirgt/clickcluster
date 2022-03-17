from inventory_modules.click_inventory import click_inventory
from jinja2 import Template

cluster = {
    1: ("10.102.0.193", "10.102.0.194"),
    2: ("10.102.0.194", "10.102.0.195"),
    3: ("10.102.0.195", "10.102.0.193")
    }

inventory = click_inventory(cluster)

template = Template(
"""
    <zookeeper>
    {%- for structure in zoo_structure%}
        <node index="{{ structure[0] }}">
            <host>{{ structure[1] }}</host>
            <port>2181</port>
        </node>
    {%- endfor%} 
    </zookeeper>
"""
)

print(template.render(
    zoo_structure=inventory["clickhouse"]["vars"]["zoo_structure"]
))