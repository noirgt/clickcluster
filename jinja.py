from inventory_modules.click_inventory import click_inventory
from jinja2 import Template

cluster = {
    1: ("10.102.0.193", "10.102.0.194"),
    2: ("10.102.0.194", "10.102.0.195"),
    3: ("10.102.0.195", "10.102.0.193")
    }

inventory = click_inventory(cluster)
print(inventory)

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
  {{ container }}:
    container_name: {{ container }}
    hostname: {{ container }}
    image: yandex/clickhouse-server:21.12.2.17
    restart: always
    ports:
        - {{ 9000 + loop.index - 1}}:{{ 9000 + loop.index - 1 }}
        - {{ 9009 + loop.index - 1}}:{{ 9009 + loop.index - 1 }}
        - {{ 8123 + loop.index - 1}}:{{ 8123 + loop.index - 1 }}
    volumes:
        - "./conf/{{ container }}:/etc/clickhouse-server"
        - "./database/{{ container }}:/var/lib/clickhouse"
        - "./logs/{{ container }}:/var/log/clickhouse-server"
    extra_hosts:
        {%- for host in extra_hosts %}
        - "{{ host }}"
        {%- endfor %}
    networks:
        - ch_net
{% endfor %}
{%- for container in zoo_containers %}
  {{ container }}:
    container_name: {{ container }}
    image: bitnami/zookeeper:3.7.0
    restart: always
    hostname: {{ container }}
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

print(template.render(
    click_containers=inventory["10.102.0.193"]["click_containers"],
    zoo_containers=inventory["10.102.0.193"]["zoo_containers"],
    zoo_structure=inventory["10.102.0.193"]["zoo_structure"],
    extra_hosts=inventory["10.102.0.193"]["extra_hosts"]
))