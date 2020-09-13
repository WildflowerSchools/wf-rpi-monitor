import psutil
import re
import datetime
from collections import OrderedDict
import csv
import os
import time

FIELD_NAMES = [
    'timestamp',
    'cpu_count',
    'cpu_percent',
    'cpu_freq_psutil',
    'clock_arm_vcgencmd',
    'temp_celsius_psutil',
    'temp_high_psutil',
    'temp_critical_psutil',
    'temp_vcgencmd',
    'voltage_core',
    'throttled_undervoltage',
    'throttled_arm_freq_capped',
    'throttled_currently_throttled',
    'throttled_soft_temp_limit_active',
    'throttled_undervoltage_has_occurred',
    'throttled_arm_freq_capping_has_occurred',
    'throttled_throttling_has_occurred',
    'throttled_soft_temp_limit_has_occurred',
    'virtual_memory_total',
    'virtual_memory_available',
    'virtual_memory_percent',
    'virtual_memory_used',
    'virtual_memory_free',
    'virtual_memory_active',
    'virtual_memory_inactive',
    'virtual_memory_buffers',
    'virtual_memory_cached',
    'virtual_memory_shared',
    'virtual_memory_slab',
    'fetch_time_ms'
]

THROTTLED_UNDERVOLTAGE_BIT_NUMBER = 0
THROTTLED_ARM_FREQ_CAPPED_BIT_NUMBER = 1
THROTTLED_CURRENTLY_THROTTLED_BIT_NUMBER = 2
THROTTLED_SOFT_TEMP_LIMIT_ACTIVE_BIT_NUMBER = 3
THROTTLED_UNDERVOLTAGE_HAS_OCCURRED_BIT_NUMBER = 16
THROTTLED_ARM_FREQ_CAPPING_HAS_OCCURRED_BIT_NUMBER = 17
THROTTLED_THROTTLING_HAS_OCCURRED_BIT_NUMBER = 18
THROTTLED_SOFT_TEMP_LIMIT_HAS_OCCURRED_BIT_NUMBER = 19

def log_rpi_status_csv(
    path,
    interval=30
):
    with open(path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(
            f=csvfile,
            fieldnames=FIELD_NAMES
        )
        writer.writeheader()
        while True:
            rpi_status = get_rpi_status()
            writer.writerow(rpi_status)
            time.sleep(interval)

def get_rpi_status():
    data = OrderedDict()
    fetch_start=time.time()
    timestamp = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
    data['timestamp'] = timestamp
    cpu_count_psutil = get_cpu_count_psutil()
    data['cpu_count'] = cpu_count_psutil
    cpu_percent_psutil = get_cpu_percent_psutil()
    data['cpu_percent'] = cpu_percent_psutil
    cpu_freq_psutil = get_cpu_freq_psutil()
    data['cpu_freq_psutil'] = cpu_freq_psutil
    clock_arm_vcgencmd = get_clock_arm_vcgencmd()
    data['clock_arm_vcgencmd'] = clock_arm_vcgencmd
    temp_psutil = get_temp_psutil()
    data.update(temp_psutil)
    temp_vcgencmd = get_temp_vcgencmd()
    data['temp_vcgencmd'] = temp_vcgencmd
    voltage_core_vcgencmd = get_voltage_core_vcgencmd()
    data['voltage_core'] = voltage_core_vcgencmd
    throttling_vcgencmd = get_throttling_vcgencmd()
    data.update(throttling_vcgencmd)
    virtual_memory_psutil = get_virtual_memory_psutil()
    data.update(virtual_memory_psutil)
    fetch_time_ms = 1000*(time.time() - fetch_start)
    data['fetch_time_ms'] = fetch_time_ms
    return data

def get_cpu_count_psutil():
    cpu_count = psutil.cpu_count(logical=True)
    return cpu_count

def get_cpu_percent_psutil():
    cpu_percent=psutil.cpu_percent(interval=None, percpu=True)
    return cpu_percent

def get_cpu_freq_psutil():
    cpu_freq_psutil = psutil.cpu_freq(percpu=True)
    cpu_freq = None
    try:
        cpu_freq = [cpu_freq_core.current for cpu_freq_core in cpu_freq_psutil]
    except:
        pass
    return cpu_freq

def get_virtual_memory_psutil():
    virtual_memory = psutil.virtual_memory()
    data = OrderedDict()
    if hasattr(virtual_memory, 'total'):
        data['virtual_memory_total'] = virtual_memory.total
    else:
        data['virtual_memory_total'] = None
    if hasattr(virtual_memory, 'available'):
        data['virtual_memory_available'] = virtual_memory.available
    else:
        data['virtual_memory_available'] = None
    if hasattr(virtual_memory, 'percent'):
        data['virtual_memory_percent'] = virtual_memory.percent
    else:
        data['virtual_memory_percent'] = None
    if hasattr(virtual_memory, 'used'):
        data['virtual_memory_used'] = virtual_memory.used
    else:
        data['virtual_memory_used'] = None
    if hasattr(virtual_memory, 'free'):
        data['virtual_memory_free'] = virtual_memory.free
    else:
        data['virtual_memory_free'] = None
    if hasattr(virtual_memory, 'active'):
        data['virtual_memory_active'] = virtual_memory.active
    else:
        data['virtual_memory_active'] = None
    if hasattr(virtual_memory, 'inactive'):
        data['virtual_memory_inactive'] = virtual_memory.inactive
    else:
        data['virtual_memory_inactive'] = None
    if hasattr(virtual_memory, 'buffers'):
        data['virtual_memory_buffers'] = virtual_memory.buffers
    else:
        data['virtual_memory_buffers'] = None
    if hasattr(virtual_memory, 'cached'):
        data['virtual_memory_cached'] = virtual_memory.cached
    else:
        data['virtual_memory_cached'] = None
    if hasattr(virtual_memory, 'shared'):
        data['virtual_memory_shared'] = virtual_memory.shared
    else:
        data['virtual_memory_shared'] = None
    if hasattr(virtual_memory, 'slab'):
        data['virtual_memory_slab'] = virtual_memory.slab
    else:
        data['virtual_memory_slab'] = None
    return data

def get_temp_psutil():
    temp_psutil = psutil.sensors_temperatures(fahrenheit=False)
    data = OrderedDict([
        ('temp_celsius_psutil', None),
        ('temp_high_psutil', None),
        ('temp_critical_psutil', None),
    ])
    try:
        temp_cpu_thermal_psutil = temp_psutil.get('cpu_thermal')[0]
        if hasattr(temp_cpu_thermal_psutil, 'current'):
            data['temp_celsius_psutil'] = temp_cpu_thermal_psutil.current
        if hasattr(temp_cpu_thermal_psutil, 'high'):
            data['temp_high_psutil'] = temp_cpu_thermal_psutil.high
        if hasattr(temp_cpu_thermal_psutil, 'critical'):
            data['temp_critical_psutil'] = temp_cpu_thermal_psutil.critical
    except:
        pass
    return data

def get_clock_arm_vcgencmd():
    with os.popen("vcgencmd measure_clock arm") as process:
        clock_arm_string_vcgencmd = process.readline()
    clock_arm = None
    clock_arm_match = re.match('frequency\([0-9]*\)=(?P<clock_arm_string>[0-9]*)', clock_arm_string_vcgencmd)
    if clock_arm_match:
        clock_arm = float(clock_arm_match.group('clock_arm_string'))/10**6
    return clock_arm

def get_temp_vcgencmd():
    with os.popen("vcgencmd measure_temp") as process:
        temp_string_vcgencmd = process.readline()
    temp = None
    temp_match = re.match('temp=(?P<temp_string>[0-9.]*)', temp_string_vcgencmd)
    if temp_match:
        temp = float(temp_match.group('temp_string'))
    return temp

def get_throttling_vcgencmd():
    with os.popen("vcgencmd get_throttled") as process:
        throttled_string_vcgencmd = process.readline()
    data = OrderedDict([
        ('throttled_undervoltage', None),
        ('throttled_arm_freq_capped', None),
        ('throttled_currently_throttled', None),
        ('throttled_soft_temp_limit_active', None),
        ('throttled_undervoltage_has_occurred', None),
        ('throttled_arm_freq_capping_has_occurred', None),
        ('throttled_throttling_has_occurred', None),
        ('throttled_soft_temp_limit_has_occurred', None),
    ])
    throttled_match = re.match('throttled=(?P<throttled_string_hex>.*)', throttled_string_vcgencmd)
    if throttled_match:
        throttled_int = int(throttled_match.group('throttled_string_hex'), 16)
        data['throttled_undervoltage'] = bool(throttled_int & 2**THROTTLED_UNDERVOLTAGE_BIT_NUMBER)
        data['throttled_arm_freq_capped'] = bool(throttled_int & 2**THROTTLED_ARM_FREQ_CAPPED_BIT_NUMBER)
        data['throttled_currently_throttled'] = bool(throttled_int & 2**THROTTLED_CURRENTLY_THROTTLED_BIT_NUMBER)
        data['throttled_soft_temp_limit_active'] = bool(throttled_int & 2**THROTTLED_SOFT_TEMP_LIMIT_ACTIVE_BIT_NUMBER)
        data['throttled_undervoltage_has_occurred'] = bool(throttled_int & 2**THROTTLED_UNDERVOLTAGE_HAS_OCCURRED_BIT_NUMBER)
        data['throttled_arm_freq_capping_has_occurred'] = bool(throttled_int & 2**THROTTLED_ARM_FREQ_CAPPING_HAS_OCCURRED_BIT_NUMBER)
        data['throttled_throttling_has_occurred'] = bool(throttled_int & 2**THROTTLED_THROTTLING_HAS_OCCURRED_BIT_NUMBER)
        data['throttled_soft_temp_limit_has_occurred'] = bool(throttled_int & 2**THROTTLED_SOFT_TEMP_LIMIT_HAS_OCCURRED_BIT_NUMBER)
    return data

def get_voltage_core_vcgencmd():
    with os.popen("vcgencmd measure_volts core") as process:
        voltage_core_string_vcgencmd = process.readline()
    voltage_core = None
    voltage_core_match = re.match('volt=(?P<voltage_core_string>[0-9.]*)', voltage_core_string_vcgencmd)
    if voltage_core_match:
        voltage_core = float(voltage_core_match.group('voltage_core_string'))
    return voltage_core
