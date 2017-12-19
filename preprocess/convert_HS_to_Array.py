'''
    Argumentos de entrada:
        
	    image       - Imagem de entrada NDimensional [img]
        header      - Cabecalho da imagem de entrada [.hdr]
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
    print "Usage:", sys.argv[0], "<<image[.img, .raw]>> <<image_header[.hdr]>> <<path>>"
    sys.exit(1)

image 		 = sys.argv[1]
image_header = sys.argv[2]
output 		 = sys.argv[3]

### Loading Envi HyperSpectral Image ###

# Leitura do cabecalho para obter o formato de dados
lib = envi.open(image_header)
lib_type = lib.dtype

# Carrega a imagem inteira de acordo com o tipo fornecido pelo cabecalho
image2 = envi.open(image_header, image).load(dtype=lib_type)

### Armazena a informacao do cabecalho original no array criado ###

# Open a file
fo = open(output+"INFO_"+os.path.basename(image)+".txt", "w")

# Salva a informacao
fo.write("Original header of the image\n")
fo.write(str(lib));
fo.write("\n\nActual information in the created array\n")
fo.write(image2.info());

# Close opend file
fo.close()


# Salva um array para um arquivo binario em formato NumPy .npy
np.save(output+os.path.basename(image), image2)
print image2.shape

# Salva um .txt
#np.savetxt('test.out', image2, fmt='%d') 

# Example of Load arrays or pickled objects from .npy, .npz or pickled files.
#fp = np.load(output+"image2.npy")
