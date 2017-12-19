'''
	Argumentos de entrada:
	    
	    image       - Matriz NDimensional no formato [.npy]
        num_components      - Numero de Componentes Principais Desejados
        output      - Diretorio de saida

    Saida:
        
        image2      - Matriz NDimensional no formato [.npy]
'''

import sys
import os
import numpy as np
from spectral import *

# Numero de argumentos nao suficiente
if len(sys.argv) != 4:
    print "Usage:", sys.argv[0], "<<image[.npy]>> <<num_components>> <<output path>>"
    sys.exit(1)

image			= sys.argv[1]
num_components	= int(sys.argv[2])
output			= sys.argv[3]

# Load arrays de [.npy] array.
data = np.load(image)

print data.shape

# Seleciona o componente principal da imagem HyperSpectral
pc = principal_components(data)

# Numero de principais componentes extraidas
pc_0999 = pc.reduce(num = num_components)
#pc_0999 = pc.reduce(fraction=0.999)

#Projecao dos dados de entrada em N componentes 
img_pc = pc_0999.transform(data)

print img_pc.shape

# Save an array to a binary file in NumPy .npy format
np.save(output+"PC_"+os.path.basename(image), img_pc)

