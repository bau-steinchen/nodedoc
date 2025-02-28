from django.shortcuts import render

# Create your views here.
from .models import Node

def nodes_list(request):
    nodes = Node.objects.all() or []
    print("Nodes QuerySet:", nodes)  # Debugging-Ausgabe
    #return render(request, 'nodes/node_list.html', {'nodes': nodes})
    return render(request, 'nodes/index.html', {'nodes': nodes})