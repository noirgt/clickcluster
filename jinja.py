from inventory_modules.click_inventory import click_inventory
from jinja2 import Template

cluster = {
    1: ("10.102.0.193", "10.102.0.194"),
    2: ("10.102.0.194", "10.102.0.195"),
    3: ("10.102.0.195", "10.102.0.193")
    }

inventory = click_inventory(cluster)

template = Template(
"""version: '3.7'
networks:
  ch_net:
    name: ch_net
    driver: bridge
    driver_opts:
       com.docker.monwork.enable_ipv6: 'false'
    ipam:
       driver: default
       config:
          - subnet: 172.31.0.0/16

services:
{%- for container in click_containers %}
  {{ container[1] }}:
    container_name: {{ container[1] }}
    hostname: {{ container[1] }}
    image: yandex/clickhouse-server:21.12.2.17
    restart: always
    ports:
        - {{ 9000 + container[0] }}:{{ 9000 + container[0] }}
        - {{ 9009 + container[0] }}:{{ 9009 + container[0] }}
        - {{ 8123 + container[0] }}:{{ 8123 + container[0] }}
        - {{ 9363 + container[0] }}:{{ 9363 + container[0] }}
    volumes:
        - "./conf/{{ container[1] }}:/etc/clickhouse-server"
        - "./database/{{ container[1] }}:/var/lib/clickhouse"
        - "./logs/{{ container[1] }}:/var/log/clickhouse-server"
    extra_hosts:
        {%- for host in extra_hosts %}
        - "{{ host }}"
        {%- endfor %}
    networks:
        - ch_net
{% endfor %}
{%- for container in zoo_containers %}
  {{ container[1] }}:
    container_name: {{ container[1] }}
    image: bitnami/zookeeper:3.7.0
    restart: always
    hostname: {{ container[1] }}
    environment:
        - ZOO_SERVER_ID=3
        - ZOO_SERVERS={{ zoo_structure }}
        - ALLOW_ANONYMOUS_LOGIN=no
        - ZOO_ENABLE_AUTH=yes
        - ZOO_CLIENT_USER=clickhouse_zoo
        - ZOO_CLIENT_PASSWORD_FILE=/opt/bitnami/zookeeper/.zoo-client-password
    ports:
        - 2181:2181
        - 2888:2888
        - 3888:3888
    volumes:
        - "data:/bitnami"
        - "./.zoo-client-password:/opt/bitnami/zookeeper/.zoo-client-password"
    extra_hosts:
        {%- for host in extra_hosts %}
        - "{{ host }}"
        {%- endfor %}
    networks:
        - ch_net
{% endfor %}
"""
)
 
for host in inventory["clickhouse"]["_meta"]["hostvars"]:
    print(template.render(
        click_containers=inventory["clickhouse"]["_meta"]["hostvars"][host]["click_containers"],
        zoo_containers=inventory["clickhouse"]["_meta"]["hostvars"][host]["zoo_containers"],
        zoo_structure=inventory["clickhouse"]["_meta"]["hostvars"][host]["zoo_structure"],
        extra_hosts=inventory["clickhouse"]["_meta"]["hostvars"][host]["extra_hosts"]
    ))
 