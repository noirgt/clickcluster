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
   <remote_servers>
        <clickhouse_cluster>
            {%- for structure in distr_structure_list%}
            <shard>
                <internal_replication>true</internal_replication>
                {%- for container in structure%}
                <replica>
                    <host>{{ container[1] }}</host>
                    <port>{{ 9000 + container[0] }}</port>
                    <user>replica_user</user>
                    <password>j8suk0qNW00e0F2FHGy/DaKh</password>
                </replica>
                {%- endfor%}
            </shard>
            {%- endfor%}
        </clickhouse_cluster>
    </remote_servers>
"""
)

print(template.render(
    distr_structure_list=inventory["clickhouse"]["vars"]["distr_structure"]
))
