from json import dumps as convert_to_json

def click_inventory(click_cluster):
    shards_dict = {}
    zoo_structure_list = []
    distr_structure_list = []
    full_distr_cluster = {}

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

    # Added zoo_structure for docker-compose and config-file
    for ip_addr_id, ip_addr in enumerate(list(shards_dict.keys())):
        len_click_containers =  len(shards_dict[ip_addr]["click_containers"])
        shards_dict[ip_addr]["zoo_containers"].append(
            (ip_addr_id + 1, f"zk{ip_addr_id + 1}")
        )
        zoo_structure_list.append(
            (ip_addr_id + 1, f"zk{ip_addr_id + 1}")
        )

        if len_click_containers > 2:
            shards_dict[ip_addr]["zoo_containers"].append(
                (ip_addr_id + 1, f"zk{ip_addr_id + 1}_2")
            )
            zoo_structure_list.append(
                (ip_addr_id + 1, f"zk{ip_addr_id + 1}_2")
            )

    # Added extra_hosts for docker-compose
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

    # Added zoo_servers for docker-compose
    for ip_addr in shards_dict.keys():
        zk_name = shards_dict[ip_addr]["zoo_containers"][0][1]
        shards_dict[ip_addr]["zoo_servers"] = []
        
        for zk_name in shards_dict[ip_addr]["zoo_containers"]:
            zoo_servers = ""
            for zoo_container in zoo_structure_list:
                zoo_container = zoo_container[1]
                if zoo_container == zk_name[1]:
                    zoo_container = "0.0.0.0"
                zoo_servers += f"{zoo_container}:2888:3888,"
            zoo_servers = zoo_servers.rstrip(',')
            shards_dict[ip_addr]["zoo_servers"].append(zoo_servers)

    # Added distr_structure for docker-compose
    for ip_addr in shards_dict.keys():
        one_shard_list = []
        for host in shards_dict[ip_addr]["click_containers"]:
            one_shard_list.append(host)
        distr_structure_list.append(one_shard_list)

    # Added full_distr_cluster for config-file
    for structure in distr_structure_list:
        for replica in structure:
            if not full_distr_cluster.get(replica[0], False):
                full_distr_cluster[replica[0]] = []
            full_distr_cluster[replica[0]].append(replica[1])

    inventory = {
        "clickhouse": {
            "hosts": list(shards_dict.keys()),
            "vars": {
                "distr_structure": distr_structure_list,
                "zoo_structure": zoo_structure_list,
                "full_distr_cluster": full_distr_cluster
            }
        },
        "_meta": {
            "hostvars": shards_dict
        }
    }

    print(convert_to_json(inventory))
