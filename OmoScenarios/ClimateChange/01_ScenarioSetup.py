'''
Sarah Jordan
05/24/2021

Set up all climate change scenarios for SWAT and DPS policies 
'''

### PACKAGES ####################################################
import os


### FUNCTIONS ##################################################
def mkdir_p(path):
    '''
    https://www.tutorialspoint.com/How-can-I-create-a-directory-if-it-does-not-exist-using-Python
    '''
    if not os.path.exists(path):
        os.makedirs(path)


### MAKE DIRECTORIES ##########################################
# path to SWAT weather files created from downscaling and debiasing projections 
swat_inp = '/scratch/smj5vup/OmoProjDownscaleDebias/Debias/cmip6_swat_input'

for file in os.listdir(swat_inp):
    parts = os.path.basename(file).split('.')
    proj = parts[1]
    rcp = parts[2]
    fname = proj + '.' + rcp
    fpath_dps = '../DPS/' + fname
    fpath_swat = '../SWAT/' + fname
    print(fname)
    mkdir_p(fpath_dps)
    mkdir_p(fpath_swat)

    # directory for pcp and tmp file
    wpath_dps = fpath_dps + "/Weather"
    wpath_swat = fpath_swat + "/Weather"
    mkdir_p(wpath_dps)
    mkdir_p(wpath_swat)

    # os.system("cp -r DPS/SWATfiles %s" % fpath_dps) # copy SWATfiles to DPS folder 
    # os.system("cp -r SWAT/SWATfiles %s" % fpath_swat) # copy SWATfiles to SWAT folder 

    # os.system("cp %s/%s/* %s/SWATfiles" % (swat_inp, file, fpath_dps)) # copy pcp and tmp files to dps folder
    # os.system("cp %s/%s/* %s/SWATfiles" % (swat_inp, file, fpath_swat)) # copy pcp and tmp files to swat folder 

    os.system("cp %s/%s/* %s/Weather" % (swat_inp, file, fpath_dps)) # copy pcp and tmp files to dps folder
    os.system("cp %s/%s/* %s/Weather" % (swat_inp, file, fpath_swat)) # copy pcp and tmp files to swat folder 