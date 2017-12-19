# Extended-Morphological-Profile

O código completo está dividido em duas partes, pré-processamento e código principal. 
 
# Pre-processamento 
Na parte de pre-processamento existem dois scripts em python: **convert_HS_to_Array.py e pca.py**.
 
- convert_HS_to_Array.py 
 
O script **convert_HS_to_Array.py** realiza a conversão dos formatos utilizados por imagens hyperspectrais em arrays N­Dimensionais, sendo utilizado da seguinte forma: 
 
**Argumentos de entrada**: 
 
image  - Imagem de entrada N-Dimensional (ENVI extension) [.img] 
header - Cabeçalho da imagem de entrada [.hdr] 
output - Diretório de saída

**Saída**: 

image2 - Matriz N-Dimensional salva no formato [.npz] 
 
**Exemplo de utilização**: 
 
python convert_HS_to_Array.py input/TelopsDatasetCityLWIR_Subset.img 
input/TelopsDatasetCityLWIR_Subset.hdr output/ 
 
- pca.py 
 
O script pca.py realiza a extração das M primeiras principais componentes do método de redução de dimensionalidade PCA. 
 
**Argumentos de entrada**: 
 
image - Matriz N-Dimensional no formato [.npy]. 
num_components - Número de componentes principais desejado. 
output - Diretório de saída

**Saída**: 
 
image2 - Matriz M-Dimensional salva no formato [.npz] 

Exemplo de utilização, para a extração das 3 primeiras componentes do exemplo acima: 
 
python pca.py output/TelopsDatasetCityLWIR_Subset.img.npy 3 output/

# Código Principal

O código principal apresentado não foi modularizado, logo todas as funções e declarações 
utilizadas estão dentro do script emp.py 
 
**Argumentos de entrada**: 
 
data - Matriz N-Dimensional no formato [.npy] 
se_size - Tamanho do elemento estruturante 
se_size_increment - Incremento do tamanho do elemento estruturante 
num_openings_closings(K) - Número de aberturas e fechamentos 
output - Diretório de saída 
 
**Saída**: 
 
image2 - Matriz N*(2*K+1)-Dimensional salva no formato [.npy] 
 
Exemplo de utilização, para a criação do perfil morfologico extendido das 3 componentes principais extraidas anteriormente: 
 
python emp.py  preprocess/output/PC_TelopsDatasetCityLWIR_Subset.img.npy 2 3 5 output/ 
 
 
**BIBLIOTECAS UTILIZADAS**: 
 
 - scikit-image: Image processing in Python
 
Instalação na plataforma linux:
easy_install -U scikit-image 
 
 - NumPy: Fundamental package for scientific computing with Python
 
Instalação na plataforma linux: 
sudo apt-get install python-numpy python-scipy 
 
 - Spectral Python (SPy) is a pure Python module for processing hyperspectral image data.
 
Instalação na plataforma linux: 
easy_install spectral 
