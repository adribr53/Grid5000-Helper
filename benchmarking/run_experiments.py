# Script used to run the experiments and collect their data

import pandas as pd
import numpy as np
import subprocess 
import time as tm
import argparse

def compute_total_throughput(data):
    return int(data[-1][-1]) / 1000000000 # In GB/s

def compute_avg_throughput(data):
    connections = data[:-1]
    tr_values = []
    for connection in connections:
        tr_values.append(int(connection[-1]))
    return np.mean(tr_values) / 1000000000 # In GB/s

def compute_avg_latency(data):
    connections = data[:-1]
    lat_values = []
    for connection in connections:
        lat_values.append(int(connection[-2]) / int(connection[-1]))
    return np.mean(lat_values) # In seconds

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Server Performance Benchmarking')
    parser.add_argument('ip_server', type=str, help='IP address of the server')
    parser.add_argument('port_server', type=str, help='Port of the server')
    parser.add_argument('ip_client', type=str, help='IP address of the client')

    args = parser.parse_args()
    print('Server IP {}'.format(args.ip_server))
    print('Server port {}'.format(args.port_server))
    print('Client IP {}'.format(args.ip_client))

    frame = pd.DataFrame(columns=['pkt_length', 'n_connections', 'time', 'total_throughput', 'avg_throughput', 'avg_latency'])

    n_connections_list = [4, 8, 32]  #[1, 8, 32, 64, 128]
    pkt_length_list = [1, 100, 500] #[1, 100, 500, 1000, 5000, 10000, 25000, 50000]
    n_runs = 3
    time = 2

    for pkt_length in pkt_length_list:
        input('Please launch server with pkt_length={}'.format(pkt_length))
        for n_connections in n_connections_list:
            print('Begin performance measures for pkt_length={}, n_connections={}, time={}'.format(pkt_length, n_connections, time))

            total_throughput_list = []
            avg_throughput_list = []
            avg_latency_list = []

            for _ in range(n_runs):
                result = subprocess.check_output("iperf -c {} -p {} -B {} -t {} -P {} -y C".format(args.ip_server, args.port_server, args.ip_client, time, n_connections), shell=True)
                result = result.decode('utf-8')

                lines = result.split("\n")
                data = [line.split(",") for line in lines]
                data.pop(-1)
                print(data)

                total_throughput = compute_total_throughput(data)
                total_throughput_list.append(total_throughput)
                print('TOTAL THROUGHPUT={} GB/s'.format(total_throughput))

                avg_throughput = compute_avg_throughput(data)
                avg_throughput_list.append(avg_throughput)
                print('AVG THROUGHPUT={} GB/s'.format(avg_throughput))

                avg_latency = compute_avg_latency(data)
                avg_latency_list.append(avg_latency)
                print('AVG LATENCY={} s'.format(avg_latency))

                print()
                tm.sleep(1)

            new_frame = pd.DataFrame({'pkt_length': [pkt_length], 'n_connections': [n_connections], 'time': [time], 'total_throughput': [np.mean(total_throughput_list)], 'avg_throughput': [np.mean(avg_throughput_list)], 'avg_latency': [np.mean(avg_latency_list)]}, index=['server-linux'])
            frame = pd.concat([frame, new_frame])
            print(frame)

    frame.to_csv(r"data1.csv", index=True)