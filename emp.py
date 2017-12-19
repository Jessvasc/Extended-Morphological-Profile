'''
	Argumentos de entrada: 
 
	data				-Matriz N­Dimensional no formato [.npy] 
	se_size 			-Tamanho do elemento estruturante 
	se_size_increment  	 	-Incremento do tamanho do elemento estruturante 
	num_openings_closings(K) ­ 	-Número de aberturas e fechamentos 
	output				-Diretório de saída 
 
	Saída:
 
	image2 ­ Matriz N*(2*K+1)­Dimensional salva no formato [.npy]
'''

import sys
import os
import numpy as np
from spectral import *
from skimage.morphology import disk
from skimage.morphology import reconstruction
from skimage.morphology import erosion
from skimage.morphology import dilation

def imcomplement(image):
	
	### Imagem com valores de intensidade ou RGB
	
	# Pixel de maior valor da imagem
	max_value = np.amax(image)
	
	# Calcula o Complemento da imagem
	im_complement = np.fabs(image - max_value)

	return(im_complement)


def opening_by_reconstruction(image,se):

	image_e = erosion(image,se)
	obr = reconstruction(image_e, image, method='dilation')

	return(obr)


def closing_by_reconstruction(image,se):

	# fechamento por reconstrução
	image_d = dilation(image,se)
	cbr = reconstruction(image_e, image, method='erosion')

	'''
	# abertura por reconstrucao
	image_e = erosion(image,se)
	obr = reconstruction(image_e, image, method='dilation')
	
	# fechamento por reconstrucao
	image_obrc = imcomplement(obr)
	image_obrce = erosion(image_obrc,se)
	cbr = imcomplement(reconstruction(image_obrce,image_obrc,method='dilation'))
	'''
	
	return(cbr)
	
	
def build_morphological_profile(image,se_size,se_size_increment,num_openings_closings):

	# Armazena as dimensões da imagem original e cria duas matrizes n-dimensionais, para guardar os fechamentos (cbr) e as aberturas (obr).
	x, y = np.shape(image)
	cbr = np.zeros((x,y,num_openings_closings)) # cbr = closing by reconstruction
	obr = np.zeros((x,y,num_openings_closings)) # obr = opening by reconstruction

	# Operações de fechamento
	tam = se_size
	for i in xrange(num_openings_closings):
		se = disk(tam)
		temp = closing_by_reconstruction(image,se)
		cbr[:,:,i] = temp[:,:]
		tam = tam + se_size_increment
		
	# Operacoes de abertura
	tam = se_size
	for i in xrange(num_openings_closings):
		se = disk(tam)
		temp = opening_by_reconstruction(image,se)
		obr[:,:,i] = temp[:,:]
		tam = tam + se_size_increment
		
	'''
	# Constroi o perfil morfologico da seguinte forma:
	# Fechamentos + Imagem Original + Aberturas
	# A ordem da concatenação importa, logo devem ser incluidos:
	# as aberturas e fechamentos construidos com os menores elementos 
	# estruturantes o mais perto possivel da imagem original.
	
	# Exemplo:
	# Tamanhos dos elementos estruturantes: 1, 3, 5
	# Possui 3 aberturas: a1,a3,a5
	# Possui 3 fechamentos: b1,b3,b5
	# Imagem original: Image
	#
	# Perfil morfologico: b5,b3,b1,Image,a1,a3,a5
	'''
	
	# Declara o perfil morfologico, vazio inicialmente
	mp = []

	# Adiciona os fechamentos
	for i in xrange(num_openings_closings-1, -1, -1):
		mp.append(cbr[:,:,i])
		
	# Adiciona a imagem original
	mp.append(image[:,:])
	
	# Adiciona as aberturas
	for i in xrange(0,num_openings_closings):
		mp.append(obr[:,:,i])

	return(mp)

###----------------------------------------------------------------------------------------------------Main----------------------------------------------------------------------------------------###

# Verifica os argumentos de entrada
if len(sys.argv) != 6:
    print "Usage:", sys.argv[0], "<<image[.npy]>> <<se_size>> <<se_size_increment>> <<num_openings_closings>> <<output>>"
    sys.exit(1)
    
# Carrega os argumentos
data					= sys.argv[1]
se_size 				= int(sys.argv[2])
se_size_increment 		= int(sys.argv[3])
num_openings_closings 	= int(sys.argv[4])
output					= sys.argv[5]

# Carrega a matriz de saida do PCA no formato .npy
image = np.load(data)

# Dimensao x e y da imagem e o numero de bandas z.
x, y, z = image.shape

# Dimensao do morphological profile
dim_mp = (num_openings_closings * 2) + 1

# Dimensao do extended morphological profile
dim_emp = dim_mp * z

# Declando matriz final do extended morphological profile
emp = []

### Construindo o EMP


for i in xrange(0,z):

	# Constroi o i-esimo perfil morfologico (MP)
	mp_temp = build_morphological_profile(image[:,:,i],se_size,se_size_increment,num_openings_closings)

	# Adiciona o i-esimo perfil morfologico no perfil morfologico extendido (EMP)
	emp.extend(mp_temp)

# Transforma a lista de perfils morfologicos em uma matriz, criando o perfil morfologico extendido
emp = np.array(emp)

# Salva o perfil morfologico extendido
np.save(output+os.path.basename(data), emp)

