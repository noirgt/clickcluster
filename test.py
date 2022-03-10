   
  
def clickcomposer(click_cluster):
    for id_node, ip_node in enumerate(click_cluster):
        id_node += 1
        replica_list = []
        for id_replica, id_shard in enumerate(click_cluster[ip_node]):
            id_replica += 1
            replica_list.append(f"ch{id_shard}_rep{id_replica}")
        print(
            f"IP-node: {ip_node}, containers: {replica_list}"
        )
   
    for id_node, one_node in enumerate(reversed(full_nodes_list)):
        id_node -= len(full_nodes_list) - 1
        id_node = -id_node
        containers = one_node["containers"]
        for _one_node in full_nodes_list[:id_node]:
            for id_container, one_container in enumerate(containers):
                if one_container in _one_node["containers"]:
                    id_replica = int(one_container[-1])
                    containers[id_container] = f"{one_container[:-1]}{id_replica + 1}"

    print(full_nodes_list)


{'10.102.0.193': {'click_containers': ['ch1_rep1', 'ch3_rep2'], 'zoo_containers': ['zk1'], 'extra_hosts': ['ch1_rep2:10.102.0.194', 'ch2_rep1:10.102.0.194', 'zk2:10.102.0.194', 'ch2_rep2:10.102.0.195', 'ch3_rep1:10.102.0.195', 'zk3:10.102.0.195'], 'zoo_structure': '0.0.0.0:2888:3888,zk2:2888:3888,zk3:2888:3888'}, '10.102.0.194': {'click_containers': ['ch1_rep2', 'ch2_rep1'], 'zoo_containers': ['zk2'], 'extra_hosts': ['ch1_rep1:10.102.0.193', 'ch3_rep2:10.102.0.193', 'zk1:10.102.0.193', 'ch2_rep2:10.102.0.195', 'ch3_rep1:10.102.0.195', 'zk3:10.102.0.195'], 'zoo_structure': 'zk1:2888:3888,0.0.0.0:2888:3888,zk3:2888:3888'}, '10.102.0.195': {'click_containers': ['ch2_rep2', 'ch3_rep1'], 'zoo_containers': ['zk3'], 'extra_hosts': ['ch1_rep1:10.102.0.193', 'ch3_rep2:10.102.0.193', 'zk1:10.102.0.193', 'ch1_rep2:10.102.0.194', 'ch2_rep1:10.102.0.194', 'zk2:10.102.0.194'], 'zoo_structure': 'zk1:2888:3888,zk2:2888:3888,0.0.0.0:2888:3888'}}