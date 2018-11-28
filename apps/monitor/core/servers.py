import re
import time

import paramiko
from paramiko.ssh_exception import NoValidConnectionsError, AuthenticationException


def login_server(ip, port, username, password, rsa_key_file):
    server_ssh = paramiko.SSHClient()
    server_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        p_key = paramiko.RSAKey.from_private_key_file(rsa_key_file)
        server_ssh.connect(hostname=ip, port=port, username=username, pkey=p_key)
    except (NoValidConnectionsError, AuthenticationException, TypeError):
        server_ssh.connect(hostname=ip, port=port, username=username, password=password)
    return server_ssh


def get_memory(ssh_obj):
    stdin, stdout, stderr = ssh_obj.exec_command('cat /proc/meminfo')
    str_out = stdout.read().decode()
    str_err = stderr.read().decode()

    if str_err != "":
        raise Exception("Command error")

    str_total = re.search('MemTotal:.*?\n', str_out).group()
    total_mem = float(re.search('\d+', str_total).group())

    str_free = re.search('MemFree:.*?\n', str_out).group()
    free_mem = float(re.search('\d+', str_free).group())

    str_buffers = re.search('Buffers:.*?\n', str_out).group()
    buffers_mem = float(re.search('\d+', str_buffers).group())

    str_cached = re.search('Cached:.*?\n', str_out).group()
    cached_mem = float(re.search('\d+', str_cached).group())

    str_slab = re.search('Slab:.*?\n', str_out).group()
    slab_mem = float(re.search('\d+', str_slab).group())

    str_swap_total = re.search('SwapTotal:.*?\n', str_out).group()
    swap_total = float(re.search('\d+', str_swap_total).group())

    str_swap_free = re.search('SwapFree:.*?\n', str_out).group()
    swap_free = float(re.search('\d+', str_swap_free).group())

    used_mem = total_mem - free_mem - buffers_mem - cached_mem - slab_mem
    used = round(float(used_mem)/float(total_mem), 2)

    return {"total_mem": total_mem, "used_mem": used_mem,
            "mem_used_percent": used, "buffers_cached_mem": buffers_mem + cached_mem,
            "swap_total": swap_total, "swap_used": swap_total - swap_free}


def _cpu_usage(ssh_obj):
    stdin, stdout, stderr = ssh_obj.exec_command('cat /proc/stat | grep "cpu "')
    str_out = stdout.read().decode()
    str_err = stderr.read().decode()

    if str_err != "":
        raise Exception("Command error")
    cpu_time_list = re.findall('\d+', str_out)
    cpu_idle = cpu_time_list[3]
    total_cpu_time = 0
    for t in cpu_time_list:
        total_cpu_time = total_cpu_time + int(t)
    return {"total_cpu_time": total_cpu_time, "cpu_idle": cpu_idle}


def get_cpu_usage(ssh_obj):
    cpu1 = _cpu_usage(ssh_obj)
    time.sleep(2)
    cpu2 = _cpu_usage(ssh_obj)
    cpu_usage = round(1 - (float(cpu2["cpu_idle"]) - float(cpu1["cpu_idle"])) /
                      (cpu2["total_cpu_time"] - cpu1["total_cpu_time"]), 2)
    # ssh_obj.close()
    return {"cpu_usage": cpu_usage}


def get_cpu_cores(ssh_obj):
    stdin, stdout, stderr = ssh_obj.exec_command('cat /proc/cpuinfo | grep "physical id"| sort| uniq | wc -l')
    str_out = stdout.read().decode()
    str_err = stderr.read().decode()
    if str_err != "":
        raise Exception("Command error")
    physical_cores = re.search('\d+', str_out).group()

    stdin, stdout, stderr = ssh_obj.exec_command('cat /proc/cpuinfo | grep "processor"| wc -l')
    str_out = stdout.read().decode()
    str_err = stderr.read().decode()
    if str_err != "":
        raise Exception("Command error")
    processor_cores = re.search('\d+', str_out).group()
    return {"physical_cores": physical_cores, "processor_cores": processor_cores}


def get_top_message(ssh_obj):
    stdin, stdout, stderr = ssh_obj.exec_command('top -bi -n 1')
    str_out = stdout.read().decode()
    str_err = stderr.read().decode()

    try:
        cpu_free = [i for i in str_out.split('\n')[2].split(', ')
                    if re.search('id', i)][0].replace('id', '').replace('%', '')
        cpu_use = 1 - float(cpu_free)/100
    except:
        cpu_use = 0.0

    if str_err != "":
        raise Exception("Command error")
    return {"cpu_use": round(cpu_use, 2), "message": str_out}
