#! /usr/bin/env python

import argparse
import numpy as np
import RIFT.misc.samples_utils as samples_utils  # add_field, extract_combination_from_LI(

from RIFT.physics import EOSManager as EOSManager
import lal
import lalsimulation as lalsim



parser = argparse.ArgumentParser()
parser.add_argument("--posterior-file",type=str,help="filename of *.dat file [standard LI output]")
parser.add_argument("--fname-out",type=str,help="filename of *.dat file [standard LI output]")
parser.add_argument("--force-ignore-lambda",action='store_true')
parser.add_argument("--eos",type=str,help="eg. lal:AP4,SLy1,")
parser.add_argument("--ejecta-fit",type=str,help="gwem:CoDi2019, gwem:KrFo2019 to access gwemlightcurves")
opts=  parser.parse_args()

samples=np.genfromtxt(opts.posterior_file,delimiter=' ',names=True)


def make_compactness(mvals,my_eos):
    # should vectorize this
    r=np.array([lalsim.SimNeutronStarRadius(mvals[i]*lal.MSUN_SI, my_eos.eos_fam) for i in range(len(mvals))]) # radius in meters
    compactness=(mvals*lal.MSUN_SI/r)*(lal.G_SI/lal.C_SI**2)
    return compactness
def make_lambda(mvals,my_eos):
    # should vectorize this
    lam=np.array([my_eos.lambda_from_m(mvals[i]*lal.MSUN_SI) for i in range(len(mvals))]) # radius in meters
    return lam


# Annotate with lambda1, lambda2, C1, C2
if opts.eos: # not('lambda1' in samples.dtype.names) and opts.eos:
    #  Get EOS name
    if ':' in opts.eos:
        how,myeosname = opts.eos.split(':')
    else:
        how = 'lal'
        myeosname  = opts.eos
    # Make EOS
    if how == 'lal':
        my_eos = EOSManager.EOSLALSimulation(name=myeosname)
    else:
        print(" Unknown EOS method ", opts.eos)

    # overwrite lambda1, lambda2, compactness1, compactness2
    # note this may make NAN samples, which we should remove as being inconsistent with the EOS
    if not('C1' in samples.dtype.names):
        samples = samples_utils.add_field(samples,[('C1',float),('C2',float)])
    if not('lambda1' in samples.dtype.names):
        samples = samples_utils.add_field(samples,[('lambda1',float),('lambda2',float)])

    samples['C1']  = make_compactness(samples['m1_source'], my_eos)
    samples['C2']  = make_compactness(samples['m2_source'], my_eos)
    
    samples['lambda1'] = make_lambda(samples['m1_source'],my_eos)
    samples['lambda2'] = make_lambda(samples['m2_source'],my_eos)

else:
    print(" lambda1, lambda2 already in samples")
    exit(1)

# Now calculate the ejecta, based on what we have so far
if opts.ejecta_fit:
    #  Get EOS name
    if ':' in opts.ejecta_fit:
        how,ejectaname = opts.ejecta_fit.split(':')
    else:
        how = 'gwem'
        ejectaname  = opts.ejecta_fit
    # Make ejecta model
    if how == 'gwem':
        
        if (ejectaname=="CoDi2019"):
            from gwemlightcurves.EjectaFits.CoDi2019 import calc_meje
            from gwemlightcurves.EjectaFits.CoDi2019 import calc_vej
            m_eje=calc_meje(samples['m1_source'], samples['C1'],samples['m2_source'], samples['C2'], zeta=0.3, split_mej = True)
            v_eje=calc_vej(samples['m1_source'], samples['C1'],samples['m2_source'], samples['C2'])
        elif (ejectaname=="Di2018"):
            from gwemlightcurves.EjectaFits.Di2018 import calc_meje
            from gwemlightcurves.EjectaFits.Di2018 import calc_vej
            m_eje=calc_meje(samples['m1_source'], samples['C1'],samples['m2_source'], samples['C2'])
            v_eje=calc_vej(samples['m1_source'], samples['C1'],samples['m2_source'], samples['C2'])

        # are we adding WIND or DYNAMICAL. Should specify!
        samples = samples_utils.add_field(samples, [('mej_wind',float), ('mej_dyn',float), ('vej_wind',float), ('vej_dyn', float)])
        samples['mej_dyn'] = m_eje[1]
        samples['mej_wind'] = m_eje[2]
        # This is terrible
        samples['vej_wind'] = v_eje
        samples['vej_dyn'] = v_eje


# Now print

# WARNING
#   -lambdat, dlambdat being populated will be inconsistent. Dangerous to do this, unelss we do it at the END

samples = samples_utils.standard_expand_samples(samples)


import pandas
dframe = pandas.DataFrame(samples)
fname_out_ascii= opts.fname_out
dframe.to_csv(fname_out_ascii,sep=' ',header=' # '+' '.join(samples.dtype.names),index=False) # # is not pre-appended...just boolean
