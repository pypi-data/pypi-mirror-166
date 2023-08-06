import os
import torch
import numpy as np
import matplotlib.pyplot as plt
from brainspy.utils.pytorch import TorchUtils
from brainspy.utils.waveform import WaveformManager
from itertools import cycle
import pickle

def generate_inputs(ranges, data_input_indices, waveform_mgr: WaveformManager):
    ranges = TorchUtils.format(ranges).double()
    result = torch.zeros_like(ranges).double()
    result[data_input_indices] = ranges[data_input_indices].clone()
    result = waveform_mgr.points_to_waveform(result.T)
    mask = TorchUtils.to_numpy(waveform_mgr.generate_mask(result.shape[0]))
    return TorchUtils.to_numpy(result), mask
    
def plot_inputs(inputs, save_dir):
    plt.figure()
    for i in range(inputs.shape[1]):
        plt.plot(inputs[:, i], label=f'Electrode {i}', alpha=0.5)
    plt.legend()
    plt.title('Inputs to the device')
    plt.savefig(os.path.join(save_dir, 'inputs.png'))
    plt.close()

def plot_outputs(outputs, frequencies, data_dir=None, mask=None):
    plt.figure()
    color_cycle = cycle(['g', 'b', 'c', 'm', 'y', 'k'])
    for key in outputs:
        color = next(color_cycle)
        if mask is None:
            mean = outputs[key].mean(axis=0)
            std = outputs[key].std(axis=0)
           
        else:
            mean = outputs[key].T[mask].T.mean(axis=0)
            std = outputs[key].T[mask].T.std(axis=0)
            #plt.plot(outputs[i][mask], label=f'Frequency {frequencies[i]} Hz', alpha=0.5)
        plt.plot(mean, label=f'Frequency {key} Hz', c=color)
        plt.plot(mean - std, alpha=0.5, linestyle='dashed', c=color)
        plt.plot(mean + std, label=f'Std {key} Hz', alpha=0.5, linestyle='dashed', c=color)
        plt.legend()
    if mask is None:
        plt.title('Outputs in different frequencies')
        if data_dir is None:
            plt.show()
        else:
            plt.savefig(os.path.join(data_dir, 'outputs.png'))
    else:
        plt.title('Outputs in different frequencies (masked ramps)')
        if data_dir is None:
            plt.show()
        else:
            plt.savefig(os.path.join(data_dir, 'outputs_masked.png'))

def plot_results(results_dir):
    results = np.load(os.path.join(results_dir, 'results.npz'))
    plot_inputs(results['inputs'])
    plot_outputs(results['outputs'], results['frequencies'], mask=results['mask'])

if __name__ == '__main__':
    from brainspy.utils.io import load_configs, create_directory_timestamp
    from brainspy.utils.manager import get_driver
    from brainspy.utils.waveform import WaveformManager
    
    configs = load_configs('configs/utils/spike_configs_template_cdaq_to_cdaq.yaml')
    
    waveform_mgr = WaveformManager(configs['waveform'])
    

    data_dir = create_directory_timestamp(configs['save_dir'], configs['test_name'])

    inputs, mask = generate_inputs(configs['driver']['instruments_setup']['activation_voltage_ranges'], configs['data_input_indices'], waveform_mgr)
    
    plot_inputs(inputs, data_dir)
    max_shape = inputs.shape[0] * int(configs['driver']['instruments_setup']['readout_sampling_frequency'] / min(configs['frequencies']))
    all_outputs = np.zeros((configs['repetitions'], len(configs['frequencies']), max_shape))

    for i in range(len(configs['frequencies'])):
        waveform_correction = WaveformManager({"slope_length" : 0, "plateau_length" : int( max_shape /( inputs.shape[0] *  int(configs['driver']['instruments_setup']['readout_sampling_frequency'] / configs['frequencies'][i])))})
        for j in range(configs['repetitions']):
            print('Repetition: '+ str(j))
            configs['driver']['instruments_setup']['activation_sampling_frequency'] = configs['frequencies'][i]
            driver = get_driver(configs["driver"])
            output = driver.forward_numpy(inputs)
            driver.close_tasks()
            all_outputs[j, i] = TorchUtils.to_numpy(waveform_correction.points_to_plateaus(TorchUtils.format(output[:, 0].copy())))  # It should be changed for allowing multiple outputs
        # print('')
        
    np.savez(os.path.join(data_dir, 'results'), inputs=inputs, outputs=all_outputs, mask=mask, frequencies=configs['frequencies'])
    plot_outputs(all_outputs, configs['frequencies'], data_dir)
    #plot_outputs(all_outputs, configs['frequencies'], data_dir, mask=mask)
    plt.show()
    plt.close()
    print("Plots saved in: " + data_dir)
