from json import dumps as convert_to_json

from tenacity import retry_if_exception

def click_inventory(click_cluster):
    shards_dict = {}
    zoo_structure_list = []
    distr_structure_list = []

    # Added click_containers
    for id_shard in click_cluster:
        for ip_addr_id, ip_addr in enumerate(click_cluster[id_shard]):
            
            if not shards_dict.get(ip_addr, False):
                shards_dict[ip_addr] = {
                    "click_containers": [],
                    "zoo_containers": [],
                    "extra_hosts": []
                    }

            shards_dict[ip_addr]["click_containers"].append(
                (id_shard, f"ch{id_shard}_rep{ip_addr_id + 1}")
                )

    # Added zoo_containers
    for ip_addr_id, ip_addr in enumerate(click_cluster.values()):
        shards_dict[ip_addr[0]]["zoo_containers"].append(
            (ip_addr_id + 1, f"zk{ip_addr_id + 1}")
        )
        zoo_structure_list.append(
            (ip_addr_id + 1, f"zk{ip_addr_id + 1}")
        )

    # Added extra_hosts
    for ip_addr in shards_dict.keys():
        for ip_addr_other in shards_dict.keys():
            if ip_addr == ip_addr_other:
                continue
    
            for host in shards_dict[ip_addr_other]["click_containers"]:
                shards_dict[ip_addr]["extra_hosts"].append(
                    (f"{host[1]}:{ip_addr_other}")
                )

            for host in shards_dict[ip_addr_other]["zoo_containers"]:
                shards_dict[ip_addr]["extra_hosts"].append(
                    (f"{host[1]}:{ip_addr_other}")
                )

    # Added zoo_servers
    for ip_addr in shards_dict.keys():
        zk_name = shards_dict[ip_addr]["zoo_containers"][0][1]
        shards_dict[ip_addr]["zoo_servers"] = ""
        
        for zoo_container in zoo_structure_list:
            zoo_container = zoo_container[1]
            if zoo_container == zk_name:
                zoo_container = "0.0.0.0"
            shards_dict[ip_addr]["zoo_servers"] += f"{zoo_container}:2888:3888,"
        
        shards_dict[ip_addr]["zoo_servers"] = shards_dict[ip_addr]["zoo_servers"].rstrip(',')

    # Added distr_structure
    for ip_addr in shards_dict.keys():
        one_shard_list = []
        for host in shards_dict[ip_addr]["click_containers"]:
            one_shard_list.append(host)
        distr_structure_list.append(one_shard_list)

    inventory = {
        "clickhouse": {
            "hosts": list(shards_dict.keys()),
            "vars": {
                "distr_structure": distr_structure_list,
                "zoo_structure": zoo_structure_list
            }
        },
        "_meta": {
            "hostvars": shards_dict
        }
    }

    #return(zoo_structure_list)
    #return(distr_structure_list)
    #return(shards_dict)
    print(convert_to_json(inventory))
    #return(inventory)