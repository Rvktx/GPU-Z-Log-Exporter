import os
import subprocess
import time

from dotenv import load_dotenv
from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY, GaugeMetricFamily


def reset_file():
    subprocess.Popen(['taskkill', '-f', '-im', 'GPU-Z.exe'])
    subprocess.Popen('Del "' + STATS_FILE_PATH + '"', shell=True)
    subprocess.Popen(GPUZ_EXEC_PATH, shell=True)
    time.sleep(6)


def get_header_data():
    print('Searching for metrics in file header.')
    with open(STATS_FILE_PATH, 'r') as f:
        header = f.readlines()[0]

    header_elements = [element.strip() for element in header.split(',')[1:-1]]
    print('Found {} metrics.'.format(len(header_elements)))
    return header_elements


def get_data():
    print('Getting data.')
    with open(STATS_FILE_PATH, 'r') as f:
        content = f.readlines()[-1]

    if os.path.getsize(STATS_FILE_PATH) > MAX_FILE_SIZE:
        reset_file()
    
    stats = [stat.strip() for stat in content.split(',')[1:-1]]
    return stats


class GPUZCollector(object):
    CLOCKS_DESC = "Clock speeds of your GPU and VRAM."
    TEMPS_DESC = "Temperature of your GPU."
    FANS_P_DESC = "Fan speeds as a percentage of max RPM."
    FANS_RPM_DESC = "Fan speeds in RPM."
    MEM_DESC = "Current VRAM memory usage."
    LOAD_DESC = "Current GPU core and other usages."
    POWER_P_DESC = "Power usage as a percentage of standard maximal TDP."
    POWER_W_DESC = "Power draw stats in watts."
    VOLT_DESC = "Current GPU core and other voltages."

    def collect(self):
        clocks = GaugeMetricFamily('gpuz_clocks_mhz', self.CLOCKS_DESC, labels=['dimension'])
        temps = GaugeMetricFamily('gpuz_temps_c', self.TEMPS_DESC, labels=['dimension'])
        fan_speeds_percent = GaugeMetricFamily('gpuz_fan_speed_percent', self.FANS_P_DESC, labels=['dimension'])
        fan_speeds_rpm = GaugeMetricFamily('gpuz_fan_speed_rpm', self.FANS_RPM_DESC, labels=['dimension'])
        mem_used = GaugeMetricFamily('gpuz_memory_usage_mb', self.MEM_DESC)
        loads = GaugeMetricFamily('gpuz_load', self.LOAD_DESC, labels=['dimension'])
        power_usage_percent = GaugeMetricFamily('gpuz_power_percent', self.POWER_P_DESC)
        power_usage_watts = GaugeMetricFamily('gpuz_power_watt', self.POWER_W_DESC, labels=['dimension'])
        voltages = GaugeMetricFamily('gpuz_voltage_v', self.VOLT_DESC, labels=['dimension'])

        for metric, value in zip(head_metrics, get_data()):
            if 'Clock' in metric:
                clocks.add_metric([metric], value)
            elif 'Temperature' in metric or 'Hot Spot' in metric:
                temps.add_metric([metric], value)
            elif 'Fan' in metric and '%' in metric:
                fan_speeds_percent.add_metric([metric], value)
            elif 'Fan' in metric and 'RPM' in metric:
                fan_speeds_rpm.add_metric([metric], value)
            elif 'Memory Used' in metric:
                mem_used.add_metric([metric], value)
            elif 'Load' in metric:
                loads.add_metric([metric], value)
            elif 'Power Consumption' in metric and '%' in metric:
                power_usage_percent.add_metric([metric], value)
            elif 'Power' in metric:
                power_usage_watts.add_metric([metric], value)
            elif 'Voltage' in metric:
                voltages.add_metric([metric], value)

        yield clocks
        yield temps
        yield fan_speeds_percent
        yield fan_speeds_rpm
        yield mem_used
        yield loads
        yield power_usage_percent
        yield power_usage_watts
        yield voltages


def start_exporter():
    start_http_server(PORT)
    REGISTRY.register(GPUZCollector())
    print(F'listening on port {PORT}.')


if __name__ == '__main__':
    load_dotenv()
    PORT = int(os.getenv('PORT', 7777))
    STATS_FILE_PATH = os.getenv('FILE_PATH', 'GPU-Z Sensor Log.txt')
    MAX_FILE_SIZE = int(os.getenv('MAX_SIZE', 10_000_000))
    GPUZ_EXEC_PATH = os.getenv('GPUZ_PATH', 'RunGPU-Z.exe')

    head_metrics = get_header_data()
    start_exporter()
    while True:
        time.sleep(5)
