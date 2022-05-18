#Se inicia la conexión (lectura de la imagen) con el sistema de archivos
try:
	sistema = open('fiunamfs.img') #Importante especificar y trabajar con codififación ASCII
#Si el archivo no se encuentra, se le indica al usuario
except FileNotFoundError:
	print("\n¡Algo salio mal!\n")
	print("Error: El sistema de archivos no fue encontrado.")
	print("-> Por favor, comprueba que el programa y el sistema de archivos"
		+ " se encuentran en el mismo directorio e intenta de nuevo.")
	print("-> Verifique que el sistema de archivos tenga por nombre 'fiunamfs.img'.")
	exit()
#Si el usuario no cuenta con permisos, se le indica
except PermissionError:
	print("\n¡Algo salio mal!\n")
	print("Error: No cuenta con los permisos necesarios para acceder al sistema de archivos.")
	exit()
	

#Clase SuperBloque que mantendrá seguros y globales los datos del primer cluster
class SuperBloque:
	
	def __init__(self,
				nombre,
				version,
				et_volumen,
				tam_cluster,
				num_clusters_dir,
				num_clusters_uni):

		self.nombre = nombre
		self.version = version
		self.et_volumen = et_volumen
		self.tam_cluster = tam_cluster #Tamaño en bytes
		self.num_clusters_dir = num_clusters_dir
		self.num_clusters_uni = num_clusters_uni


#Método que permite leer los datos del superbloque y asignarlos a un objeto de este tipo
def crear_super_bloque():
	#En este método ocuparemos las funciones seek y read para archivos
	#Seek se encarga de establecer un cursor en la posición dada por parametro
	#Read se encarga de leer la cantidad de datos especificados como parametro

	#Leemos el nombre del sistema de archivos en las posiciones 0-8 de la imagen
	sistema.seek(0)
	nombre = sistema.read(8)

	if (nombre != "FiUnamFS"):
		raise Exception(
				"\n¡Algo salio mal!\n" +
				"Error: El sistema de archivos no es de tipo FiUnamFS."
			)
		exit()

	#Leemos la versión de implementación en las posiciones 10-13
	sistema.seek(10)
	version = sistema.read(3)

	#Leemos la etiqueta del volumen en las posiciones 20-35
	sistema.seek(20)
	et_volumen = sistema.read(15)

	#Leemos el tamaño del cluster (en bytes) en las posiciones 40-45
	sistema.seek(40)
	tam_cluster = int(sistema.read(5))

	#Leemos el número de clusters que mide el directorio en las posiciones 47-49
	sistema.seek(47)
	num_clusters_dir = int(sistema.read(2))

	#Leemos el número de clusters que mide la unidad completa en las posiciones 52-60
	sistema.seek(52)
	num_clusters_uni = int(sistema.read(8))

	

	return SuperBloque(nombre,
					version,
					et_volumen,
					tam_cluster,
					num_clusters_dir,
					num_clusters_uni)


#Método que permite mostrar el contenido del directorio
def mostrar_directorio(info_sistema):
	tam_entrada = 64 #Tamaño de cada entrada del directorio
	num_entradas_cluster = int(info_sistema.tam_cluster/tam_entrada) #Número de entradas por cluster

	#Formateamos el encabezado del listado
	print("{:<20}".format("Nombre"),end='')
	print("{:<20}".format("Tamaño"),end='')
	print("{:<10}".format("Cluster"),end='')
	print("{:<20}".format("Creación:"),end='')
	print("{:<20}".format("Última modificación:"))

	#Mostramos las entradas en los 4 diferentes clusters
	for i in range(4):
		#Obtenemos la dirección de cada cluster a partir de su tamaño y número
		direccion_cluster = info_sistema.tam_cluster*(i+1)

		#Dirijimos el cursor hacia la direccion previamente obtenida
		sistema.seek(direccion_cluster)

		for i in range(num_entradas_cluster):
			nombre = sistema.read(15)
			sistema.read(1)
			
			tamanio = sistema.read(24-16)
			sistema.read(1)
			
			num_cluster = sistema.read(30-25)
			sistema.read(1)

			creacion = sistema.read(45-31)
			sistema.read(1)

			modificacion = sistema.read(60-46)
			sistema.read(65-61)

			#Si el nombre corresponde con una entrada no utilizada pasamos a la siguiente
			if(nombre == "..............."):
				continue

			print("{:<20}".format(nombre),end='')
			print("{:<20}".format(tamanio),end='')
			print("{:<10}".format(num_cluster),end='')
			print("{:<20}".format(creacion),end='')
			print("{:<20}".format(modificacion))


		

info_sistema = crear_super_bloque()
mostrar_directorio(info_sistema)

