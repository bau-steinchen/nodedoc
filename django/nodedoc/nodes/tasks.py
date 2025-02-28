from celery import shared_task
import nmap
from django.utils.timezone import now
from .models import Node

@shared_task
def scan_network(subnet="172.16.192.0/24"):
    nm = nmap.PortScanner()
    nm.scan(hosts=subnet, arguments='-sn')  # Ping-Scan
    
    found_nodes = set()
    updated_nodes = []

    for host in nm.all_hosts():
        mac = nm[host]['addresses'].get('mac', None)
        hostname = nm[host].get('hostnames', [{}])[0].get('name', '')

        node, created = Node.objects.update_or_create(
            ip_address=host,
            defaults={"hostname": hostname, "mac_address": mac, "last_seen": now(), "online": True}
        )

        if created or not node.online:
            updated_nodes.append(node)

        found_nodes.add(host)

        # Geräte, die nicht gefunden wurden, offline setzen
        offline_nodes = Node.objects.filter(online=True).exclude(ip_address__in=found_nodes)
        for node in offline_nodes:
            node.online = False
            node.save()
            updated_nodes.append(node)

        # Falls es Änderungen gibt, sende nur die geänderten Geräte
        if updated_nodes:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "nodes",
                {
                    "type": "send_node_update",
                    "nodess": serialize('json', updated_nodes)  # Sende nur geänderte Geräte
                }
            )

    # Setze nicht mehr gefundene Geräte auf offline
    Node.objects.filter(online=True).exclude(ip_address__in=found_nodes).update(online=False)
