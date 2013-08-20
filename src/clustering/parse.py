import nibabel as nb
import numpy as np
import pickle
import sys
import surfer.io as surf
from variables import freesurferdir

inputFile = sys.argv[1]
flag = 'found cluster!!'
rowflag = 'rows=,['
hemi = 'lh'

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

[vertices,colortable,names] = surf.read_annot(freesurferdir+'/fsaverage4/label/'+hemi[-2:]+'.aparc.a2009s.annot', orig_ids=True)
surface = np.zeros_like(vertices)

clusters = []
with open(inputFile,'rb') as openfile:
	for line in openfile:
		if line[:len(flag)] == flag:
			clusters.append(line)

for index, cluster in enumerate(clusters):
    startIndex = cluster.rfind(rowflag)
    stopIndex = cluster.rfind(']')-1
    for x in cluster[startIndex:stopIndex].split(','):
        vertex = x.lstrip()
        if vertex.isdigit():
            surface[int(x)] = 1
        if vertex.endswith(']'):
            surface[int(x[:-1])] = 1
    savefile = inputFile.split('.')[0]+'_cluster'+str(index)
    newImage = nb.nifti1.Nifti1Image(surface, None)
    nb.save(newImage, savefile)
    #with open(savefile,'wb') as openfile:
    #pickle.dump(numbers, openfile)


