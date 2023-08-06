#!/usr/bin/env python
# coding: utf-8

# In[47]:


def install_dependencies():
    get_ipython().system(' pip install --upgrade pip')
    get_ipython().system(' pip install dscribe')
    get_ipython().system(' pip install --upgrade --user ase')
    get_ipython().system(' pip install natsort')
    get_ipython().system(' pip install pandas')
    get_ipython().system(' pip install numpy')
    get_ipython().system(' pip install -U scikit-learn')
    get_ipython().system(' pip install tensorflow')
    get_ipython().system(' pip install seaborn')
    get_ipython().system(' pip install qml --user -U')
    get_ipython().system(' pip install -U matplotlib')
    get_ipython().system(' pip install qrcode[pil]')


# In[48]:


def define_modules():
    import glob
    import numpy as np
    import pandas as pd
    import seaborn as sns
    import tensorflow as tf
    import matplotlib.pyplot as plt
    from pyscf import scf,gto,lo
    from natsort import natsorted
    from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
    from sklearn import tree
    from sklearn.preprocessing import StandardScaler
    from sklearn.decomposition import PCA
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics.pairwise import cosine_similarity
    np.set_printoptions(precision=3, suppress=True)


# In[49]:


def create_soap(path,rcut_i=8,processors=1):
    '''
    ***
    
    Description:
    
    SOAP generation function by specifying the absolute path (path), cuttoff radius (rcut_i), and the number of processors (processors).
    
    ***
    '''
    import os
    import glob
    from ase.io import read
    from natsort import natsorted
    from dscribe.descriptors import SOAP
    structures=[]
    species = set()
    for file in natsorted(glob.glob(path)):
            structures.append(read(file))
            species.update(read(file).get_chemical_symbols())
    soap = SOAP(species=species, periodic=False, rcut=rcut_i, nmax=8, lmax=8, average="outer", sparse=False)
    feature_vectors_soap = soap.create(structures, n_jobs=processors)
    return feature_vectors_soap
    print("SOAP are stored in the variable 'feature_vector_soap'")


# In[50]:


def create_cm(path, processors=1):
    '''
    ***
    
    Description:
    
    CM generation function by specifying the absolute path (path), and the number of processors (processors).
    
    ***
    '''
    import os
    import glob
    from ase.io import read
    from natsort import natsorted
    from dscribe.descriptors import CoulombMatrix
    structures=[]
    size=[]
    species = set()
    for file in natsorted(glob.glob(path)):
            structures.append(read(file))
            species.update(read(file).get_chemical_symbols())
            size.append(len(open(file).readlines()[2:]))
    cm = CoulombMatrix(n_atoms_max=max(size),sparse=False,flatten=True,permutation='sorted_l2')
    feature_vectors_CM = cm.create(structures, n_jobs=processors)
    return feature_vectors_CM
    print("CM are stored in the variable 'feature_vector'")


# In[51]:


def create_slatm(path):
    '''
    ***
    
    Description:
    
    The Spectrum of London and Axillrod-Teller-Muto potential representation generation function by specifying the absolute path (path), and the number of processors (processors).
    
    ***
    '''
    import os
    import glob
    from natsort import natsorted
    from qml.representations import generate_slatm
    from qml.representations import get_slatm_mbtypes
    import qml
    feature_vectors_slatm=[]
    size=[]
    for file in natsorted(glob.glob(path)):
        mol=qml.Compound(xyz=file)
        mbtypes = get_slatm_mbtypes([mol.nuclear_charges])
        mol.generate_slatm(mbtypes)
        feature_vectors_slatm.append(mol.representation)
    return feature_vectors_slatm
    print("SLATM are stored in the variable 'feature_vector_slatm'")


# In[52]:


def create_MIBOC (path,basis_set='def2-TZVP', charge=0, spin=0):
    '''
    ***
    
    Description:
    
    Creates the new MIBOC molecular representation by specifying the absolute path of the file (path), the basis set (basis set), 
    molecular charge (charge), and spin (N alpha-N beta). 
    
    ***
    '''
    from pyscf import scf,gto,lo
    import glob
    from natsort import natsorted
    lo_oc=[]
    for file in natsorted(glob.glob(path)):
        lo_oc.append(lo.orth_ao(scf.RHF(gto.M(atom = file, basis = basis_set,charge=charge,spin=spin)), 'Intrinsic bond orbitals').flatten())
    return lo_oc
    print("IBORep are stored in the variable 'lo_oc'")


# In[53]:


def create_qr(array,path):
    '''
    ***
    
    Description:
    
    Creates the molecular QR representation using the SPAHM representation. 
    
    ***
    '''
    import qrcode
    import os
    for i in range(len(array)):
        os.chdir(path)
        img=qrcode.make(array[i])
        type(img)
        img.save(str(i)+".png")


# In[54]:


def dim_red(data,nr_dim=2):
    '''
    ***
    
    Description:
    
    Performes a Principal Component Analysis by specifying the number of final dimensions (nr_comp) and the data to be reduced (data). 
    
    ***
    '''
    import pandas as pd
    import numpy as np
    from sklearn.decomposition import PCA
    columns=['PC1','PC2']
    if nr_dim==3:
            columns=['PC1','PC2','PV3']
    pca = PCA(n_components=nr_dim)
    principalComponents = pca.fit_transform(data)
    print(f'PC1 carries {round(pca.explained_variance_ratio_[0]*100)}% of the data')
    print(f'PC2 carries {round(pca.explained_variance_ratio_[1]*100)}% of the data')
    if nr_dim==3:
        print(f'PC3 carries {round(pca.explained_variance_ratio_[2]*100)}% of the data')
    PCA = pd.DataFrame(principalComponents, columns=columns)
    return PCA


# In[55]:


def zero_pad_inner(array):
    '''
    ***
    
    Description:
    
    Function for performing array (array) zero padding. 
    
    ***
    '''
    import numpy as np
    sz=[]
    for i in array:
        sz.append(i.size)
    padded=[]
    for a in array:
        padded.append(np.pad(a,(0,max(sz)-a.size)))
    return padded
    print("The padded array is stored under the variable named 'padded' ")


# In[56]:


def zero_pad_two_ndarrays(big_array,small_array):
    '''
    ***
    
    Description:
    
    Function for performing array zero padding. 
    
    ***
    '''
    import numpy as np
    array=[]
    for i in small_array:
        array.append(np.pad(i,(0,np.array(big_array).shape[1]-i.size)))
    return array
    print("The padded ex-small_array is stored under the variable named 'array' ")


# In[57]:


def cosine_similarity(array_one,array_two):
    '''
    ***
    
    Description:
    
    Gives the cosine similaritty between two arrays. 
    
    ***
    '''
    similarity=[]
    for i in range(len(array_one)):
        for m in range(len(array_two)):
            similarity.append(cosine_similarity(array_one[i].reshape(1,-1), array_two[m].reshape(1,-1)))  
    similarity = np.array(np.array_split(similarity, len(array_one))).squeeze()
    return similarity
    print("The is stored under the variable named 'similarity' ")

