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


cluster = {
    "10.102.0.193": (1, 2),
    "10.102.0.194": (2, 3),
    "10.102.0.195": (3, 1)
    }

clickcomposer(cluster)