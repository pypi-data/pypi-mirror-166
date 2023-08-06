import os
import torch
import numpy as np
import matplotlib.pyplot as plt
from brainspy.utils.pytorch import TorchUtils
from brainspy.utils.waveform import WaveformManager
from itertools import cycle
import pickle
import time

##### 
import nidaqmx
import nidaqmx.constants as constants
import matplotlib.pyplot as plt
from nidaqmx.constants import Edge
from nidaqmx.stream_readers import AnalogSingleChannelReader
from nidaqmx.stream_writers import (
    AnalogSingleChannelWriter, AnalogMultiChannelWriter)
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
    for i in range(outputs.shape[1]):
        color = next(color_cycle)
        if mask is None:
            mean = outputs[:, i].mean(axis=0)
            std = outputs[:, i].std(axis=0)
           
        else:
            mean = outputs[:, i].T[mask].T.mean(axis=0)
            std = outputs[:, i].T[mask].T.std(axis=0)
            #plt.plot(outputs[i][mask], label=f'Frequency {frequencies[i]} Hz', alpha=0.5)
        plt.plot(mean, label=f'Frequency {frequencies[i]} Hz', c=color)
        plt.plot(mean - std, alpha=0.5, linestyle='dashed', c=color)
        plt.plot(mean + std, label=f'Std {frequencies[i]} Hz', alpha=0.5, linestyle='dashed', c=color)
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
    plot_outputs(results['outputs'],results['frequencies'], mask=results['mask'])

if __name__ == '__main__':
    from brainspy.utils.io import load_configs, create_directory_timestamp
    from brainspy.utils.manager import get_driver
    
    configs = load_configs(r'C:\Users\Mohamadreza\Documents\github\brainspy-smg\configs\utils\spike_configs_template_cdaq_to_cdaq.yaml')
    
    
    waveform_mgr = WaveformManager(configs['waveform'])

    data_dir = create_directory_timestamp(configs['save_dir'], configs['test_name'])

    inputs, mask = generate_inputs(configs['driver']['instruments_setup']['activation_voltage_ranges'], configs['data_input_indices'], waveform_mgr)
    sample_rate = 10000
    plot_inputs(inputs, data_dir)
    all_outputs = np.zeros((configs['repetitions'], len(configs['frequencies']), inputs.shape[0]))

    activation_task =  nidaqmx.Task("activation_task")
    readout_task = nidaqmx.Task("readout_task"+str(int(time.time())))
    
    activation_task.ao_channels.add_ao_voltage_chan("cDAQ1Mod3/ao0")
    # activation_task.triggers.start_trigger.dig_edge_dig_sync_enable = True
    
    readout_task.ai_channels.add_ai_voltage_chan("cDAQ1Mod4/ai0")

    activation_task.triggers.start_trigger.cfg_dig_edge_start_trig(
            "/cDAQ1/segment1/ai/StartTrigger")

    # sample_clk_task = nidaqmx.Task('sync_task')
    # sample_clk_task.co_channels.add_co_pulse_chan_freq("cDAQ1Mod4/ctr0", freq=sample_rate)
    # sample_clk_task.do_channels.add_do_chan("cDAQ1Mod2/port0/line1")


    ac_type = constants.AcquisitionType.CONTINUOUS #FINITE



    for i in range(len(configs['frequencies'])):
        for j in range(configs['repetitions']):

            print('Repetition: '+ str(j))
            configs['driver']['sampling_frequency'] = configs['frequencies'][i]
            #driver = get_driver(configs["driver"])

            inputs_submit = inputs
            #inputs_submit = np.concatenate((inputs, inputs[-1, :] * np.ones((1, inputs.shape[1])), inputs[-1, :] * np.ones((1, inputs.shape[1]))))
            inputs_submit = inputs_submit.T
            inputs_submit = np.require(inputs_submit, dtype=inputs_submit.dtype, requirements=["C", "W"])


            # sample_clk_task.timing.cfg_implicit_timing(sample_mode = constants.AcquisitionType.CONTINUOUS)   #  samps_per_chan=inputs_submit[0].shape[0])

            samp_term = "/cDAQ1/Segment1/ai/SampleClock"#"/cDAQ1/Ctr0InternalOutput"
            # samp_term = "cDAQ1/segment1/ai/SampleClock"
            activation_freq = 5000
            readout_freq = 10000
            activation_task.timing.cfg_samp_clk_timing(
                activation_freq, 
                #source = samp_term,
                 #source="cDAQ1/do/SampleClock",
                sample_mode = constants.AcquisitionType.FINITE, #ac_type,
                # active_edge=Edge.RISING
                samps_per_chan=inputs_submit[1].shape[0])

            readout_task.timing.cfg_samp_clk_timing(
                readout_freq, 
                # source = samp_term,
                sample_mode =  constants.AcquisitionType.FINITE,
               # active_edge=Edge.RISING,
                samps_per_chan=int((readout_freq/activation_freq)*inputs_submit[1].shape[0]))


            # readout_task.change_detect_di_rising_edge_physical_chans.

            # activation_task.triggers.start_trigger.cfg_dig_edge_start_trig(
            #  "/cDAQ1/te0/StartTrigger",Edge.RISING)
            # readout_task.triggers.start_trigger.cfg_dig_edge_start_trig(
            #  "/cDAQ1/di/StartTrigger",Edge.RISING)


            # activation_task.start()
            # readout_task.timing.cfg_samp_clk_timing(
            # #5000,
            # 10000,
            # #source="OnboardClock",
            # sample_mode=ac_type)#,
            # #samps_per_chan=inputs_submit[0].shape[0])


            # activation_task.timing.cfg_samp_clk_timing(
            #         10000,
            #         #source="OnboardClock",
            #         source="/cDAQ1Mod3/ai/SampleClock",
            #         sample_mode=ac_type)#,
            #         #samps_per_chan=inputs_submit[0].shape[0])
            
            # writer = AnalogSingleChannelWriter(activation_task.out_stream, auto_start=False)
            # reader = AnalogSingleChannelReader(readout_task.in_stream)
            values_read = inputs_submit[0].copy()
            # writer.write_many_sample(inputs_submit[0])

            
            
            # # readout_task.start()
            # activation_task.start()
            # # sample_clk_task.start()
            # # sample_clk_task.write(True)
            
            


            activation_task.write(inputs_submit[1], auto_start=True)
            #activation_task.start()
            read_data = readout_task.read(int((readout_freq/activation_freq)*inputs_submit[1].shape[0]))
            #readout_task.start()



            # reader.read_many_sample(
            #     values_read, number_of_samples_per_channel=inputs_submit[0].shape[0],
            #     timeout=2)

            # driver.set_shape_vars(inputs_submit.shape[1])
            # driver.tasks_driver.start_trigger(driver.configs["instruments_setup"]["trigger_source"])
            # driver.tasks_driver.write(inputs_submit, driver.configs["auto_start"])
            # driver.tasks_driver.activation_task
            # driver.tasks_driver.readout_task
            # driver.tasks_driver.stop_tasks()
            #read_data = driver.tasks_driver.read(driver.offsetted_shape, driver.ceil)
            #data = -1 * driver.process_output_data(read_data)[:, 1:]
            #output = data.T
            output = np.array(read_data).T
            activation_task.stop()
            readout_task.stop()
            plt.figure()
            plt.plot(output[int((readout_freq/activation_freq)):], label='output')
            test = waveform_mgr.points_to_plateaus(inputs_submit[1])
            plt.plot(test, label='inputs')
            plt.legend()
            plt.show()
            # output = driver.forward_numpy(inputs)
            #driver.close_tasks()
            all_outputs[j, i] = output[int((readout_freq/activation_freq)):].copy()  # It should be changed for allowing multiple outputs
        activation_task.close()
        readout_task.close()
        # print('')
    np.savez(os.path.join(data_dir, 'results'), inputs=inputs, outputs=all_outputs, mask=mask, frequencies=configs['frequencies'])
    plot_outputs(all_outputs, configs['frequencies'], data_dir)
    plot_outputs(all_outputs, configs['frequencies'], data_dir, mask=mask)
    plt.show()
    plt.close()
    print("Plots saved in: " + data_dir)
