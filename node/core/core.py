import multiprocessing
from multiprocessing import Queue
import argparse
import random
import audio_recorder
import time
import yaml
import traceback

"""
The core is responsible for dispatching initial device connections on multiple processes and 
a bridge processes that is responsible for routing data between async processes
The core will maintain status of each process through a heart beat.
"""

"""
Parse yaml configs into a process tree
"""
def generate_process_dependencies(config):
    process_map = {}

    for proc_label in config:
        try:
            proc = {'label': proc_label, 'module': config[proc_label]['module_name']}
            # check if the label has already been created.
            if proc_label in process_map:
                proc = process_map[proc_label]
            
            #initialize input_buffer
            proc['input_buff'] = Queue()

            # If it has no out_putbuff, initialize output_buffer
            if 'output_buff' not in proc:
                proc['output_buff'] = Queue()

            # set the input buffer as the output buffer for the all of its dependencies.
            try:
                for input_source in config[proc_label]['input_sources']:

                    dep = {'label': input_source}
                    # check if the label has already been created.
                    if input_source in process_map:
                        dep = process_map[input_source]

                    dep['output_buff'] = proc['input_buff']

                    process_map[input_source] = dep
            except Exception as e:
                pass
                # print(e)
                
            process_map[proc_label] = proc
        except:
            pass

    return process_map

if __name__ == '__main__':
    cfg = None
    with open("dependency_config.yml", 'r') as stream:
        try:
            cfg = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    # create dependency tree
    process_pool = generate_process_dependencies(cfg)

    for process in process_pool:
        try:
            module = __import__(process_pool[process]['module'])
            proc = multiprocessing.Process(target=module.init, args = (process_pool[process]['input_buff'], process_pool[process]['output_buff'],))
            proc.start()
            process_pool[process]['process'] = proc

        except Exception as e:
            print('Unable to launch process for arguments [{}], {}'.format(process, e))
            traceback.print_exc()


    # print(process_pool)

    #TODO(sathoshi):
        # Continously do heartbeat polling with all the different processes that exist. 
        # The heart beat process should be req and ack from the process.
        # If the heart beat does not respond with an ack, we should kill the process and restart.
