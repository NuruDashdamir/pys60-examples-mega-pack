import os, e32
aif_path, aif_name = 'E:\\System\\Apps\\RscEditor\\Aif\\', '\\RscEditor.aif'
ld = os.listdir(aif_path)
for i in range(len(ld)):
    if os.listdir(aif_path+ld[i]) == []:
        e32.file_copy(aif_path+ld[i]+aif_name, aif_path[:-5]+aif_name)
        os.remove(aif_path[:-5]+aif_name)
        e32.ao_sleep(7)
        e32.file_copy(aif_path[:-5]+aif_name, aif_path+ld[i-1]+aif_name)
        os.remove(aif_path+ld[i-1]+aif_name)
        break