#! /usr/bin/env python

# USAGE
#   python annotate_samples_with_predicted_results.py --em-model demo_model.json --em-cache demo.emcache  --em-out-dir em_out
# WHAT IT DOES
#   Uses the emcache option to create TARGETED TIMES AND BANDS to evaluate
#   Output file LOOKS LIKE a set of EM output files (per band, etc) ... t t_err mag mag_err
#   ...but the mag is the mean predicted mag, and mag_error is the standard deviation, averaging over predictions.

import json
import numpy as np
import argparse
from numpy.lib import recfunctions as rfn

import RIFT.misc.samples_utils as samples_utils


import EMObservations as emo
import EMModel as emm
import EMModelFromEMPE as emm_empe
import EMModelSurrogateKNE as emm_skne
import copy


# Should be ported to class, and we should have all classes wrapped in one
def create_em_model_from_dict(my_dict):
    my_model=None
    model_group  = my_dict['model_group']
    model_name  = my_dict['model_name']
    if model_group == 'em_pe':
        my_model = emm_empe.EMPEModel(empe_model_type=model_name)
    elif model_group == 'constant':
        my_model = emm.EMConstantModel(fiducial_values=my_dict['fiducial_values'])
    elif model_group == 'skne':
        my_model = emm_skne.EMModelSKNE()
    else:
        raise(" create_em_model_from_dict: Unknown model type ")
    return my_model
    



parser = argparse.ArgumentParser()
parser.add_argument("--posterior-file",type=str,help="filename of *.dat file [standard LI output], including ejecta names. Default is to assume ejecta parameters are all defined, and that correct field names already exist")
parser.add_argument("--em-out-dir",type=str,help="filename for directory to create to hold EM output")
parser.add_argument("--n-max",type=int,default=3000,help="Maximum number of samples to process")
parser.add_argument("--em-cache",type=str,help="directory name for EM observations.  (Should make a 'cache' file)")
parser.add_argument("--em-time-unit",type=str,help="Time unit for em INPUT data.  If not specified, the code assumes *second*; pass.'day' to use days.  Note the OUTPUT will hav ethe same units as the INPUT, to make life easier for everyone")
parser.add_argument("--em-model",type=str,default='samples_with_EM',help="filename of *.dat file [standard LI output]")
parser.add_argument("--posterior-field-rename",action='append',default=None,help="a=B means field B is converted to field a when processed internally.  a must be a field name for the model specified")
parser.add_argument("--fix-field-value",action='append',default=None,help='a=x sets field a to x.  Useful if the posterior samples lack all the fields needed for the model')
parser.add_argument("--verbose",action='store_true')
opts=  parser.parse_args()


# Import EM observations 
emobs = emo.EMObservations(name='obs')
emobs.populate_observations_from_cache(opts.em_cache,time_unit_str=opts.em_time_unit)
if opts.verbose:
    print(" ------ INPUT ---- ")
    emobs.print_observations()

# Instantiate model
my_json = {}
with open(opts.em_model,'r') as f:
    my_json  = json.load(f)
em_model = create_em_model_from_dict(my_json)
em_model.t_bounds_days = [np.min([np.min(emobs.times[band]) for band in emobs.band_names]), np.max([np.max(emobs.times[band]) for band in emobs.band_names])]
em_model.print_model()
param_names = em_model.param_names
#print(" EM model param names ", param_names())

# Import posterior file
samples = np.genfromtxt(opts.posterior_file,names=True)
# Truncate file length as requested 
name0 = samples.dtype.names[0]
if len(samples[name0]) > opts.n_max:
    samples=samples[:opts.n_max]


## remap field names as needed
if opts.posterior_field_rename:
    remap_rules ={}
    for my_rule in opts.posterior_field_rename:
        a,b = my_rule.split('=')
        remap_rules[a] = b
    #samples.rename_fields(samples, remap_rules)
    samples = np.lib.recfunctions.rename_fields(samples, remap_rules)

## import fixing rules
fixing_assignments= {}
if opts.fix_field_value:
    for my_rule in opts.fix_field_value:
        a,b = my_rule.split('=')
        fixing_assignments[a] = b
    
    
## test if all param name fields are present
is_ok = True
for name in param_names():
    if name in fixing_assignments:
        continue
    if not(name in samples.dtype.names):
        is_ok=False
        raise Exception(" Posterior samples file does not contain required argument {} ".format(name))

## truncate file 

## pull out specific fields into new recordarray
name0 = samples.dtype.names[0]
npts = len(samples[name0])

## ASSUME the fields are all present

dtype_distilled = np.dtype([ (x,float) for x in param_names()])
distilled_samples = np.recarray( npts, dtype=dtype_distilled)
for name in param_names():
    if name in fixing_assignments:
        distilled_samples[name] = fixing_assignments[name]
        continue
    distilled_samples[name] = samples[name]

# Instantiate prediction functions,  given model.  Arguments are vector 
bandfuncs ={}
for band in emobs.band_names:
    bandfuncs[band] = em_model.return_predict_band(emobs,band)
em_out = copy.deepcopy(emobs)  # deep clone
em_out.name = 'prediction_distribution'
for band in emobs.band_names:
    vals = bandfuncs[band](distilled_samples)
#    print(band,vals)
    em_out.times[band] = emobs.times[band]
    em_out.em_observations[band] = np.mean(vals,axis=0)
    em_out.em_observations_errors[band] = np.std(vals,axis=0)
#    print(band,em_out.em_observations[band].shape)
if opts.verbose:
    print(" ------ OUTPUT ---- ")
    em_out.print_observations()

em_out.write_observations_to_dir_txt(opts.em_out_dir,time_unit_str=opts.em_time_unit)
