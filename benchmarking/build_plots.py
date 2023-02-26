# Script used to create and save plots using the data collected during the experiments

import matplotlib.pyplot as plt
import pandas as pd

unit_tr = 1000000000
unit_tr_str = "GB/s"
unit_time = 1000
unit_time_str = "ms"

df1 = pd.read_csv('data1.csv', index_col=0)
df1['total_throughput'] = df1['total_throughput'] / unit_tr
df1['std_total_throughput'] = df1['std_total_throughput'] / unit_tr
df1['avg_throughput'] = df1['avg_throughput'] / unit_tr 
df1['std_avg_throughput'] = df1['std_avg_throughput'] / unit_tr
df1['avg_latency'] = df1['avg_latency'] * unit_time
df1['std_avg_latency'] = df1['std_avg_latency'] * unit_time
print(df1)

df2 = pd.read_csv('data2.csv', index_col=0)
df2['total_throughput'] = df2['total_throughput'] / unit_tr
df2['std_total_throughput'] = df2['std_total_throughput'] / unit_tr
df2['avg_throughput'] = df2['avg_throughput'] / unit_tr 
df2['std_avg_throughput'] = df2['std_avg_throughput'] / unit_tr 
df2['avg_latency'] = df2['avg_latency'] * unit_time
df2['std_avg_latency'] = df2['std_avg_latency'] * unit_time
print(df2)

# AVG THROUGHPUT
df_server_linux = df1.loc[['server-linux']].pivot("n_connections", "pkt_length", "avg_throughput")
yerr = df1.loc[['server-linux']].pivot("n_connections", "pkt_length", "std_avg_throughput")
df_server_linux.plot(kind='bar', yerr=yerr, rot=0)
plt.title("Average Throughput/Connection  of Linux server for \n various number of parallel connections and packet length")
plt.xlabel('Number of parallel connections')
plt.ylabel('Average Throughput/Connection  ({})'.format(unit_tr_str))
plt.grid(axis="y", linestyle="dashed", zorder=0)
plt.savefig("plots/avg_tr_linux.svg")

# TOTAL THROUGHPUT
df_server_linux = df1.loc[['server-linux']].pivot("n_connections", "pkt_length", "total_throughput")
yerr = df1.loc[['server-linux']].pivot("n_connections", "pkt_length", "std_total_throughput")
df_server_linux.plot(kind='bar', yerr=yerr, rot=0)
plt.title("Total Throughput of Linux server for \n various number of parallel connections and packet length")
plt.xlabel('Number of parallel connections')
plt.ylabel('Total Throughput ({})'.format(unit_tr_str))
plt.grid(axis="y", linestyle="dashed", zorder=0)
plt.savefig("plots/total_tr_linux.svg")

# AVG LATENCY
df_server_linux = df1.loc[['server-linux']].pivot("n_connections", "pkt_length", "avg_latency")
yerr = df1.loc[['server-linux']].pivot("n_connections", "pkt_length", "std_avg_latency")
df_server_linux.plot(kind='bar', yerr=yerr, rot=0)
plt.title("Average Latency of Linux server for \n various number of parallel connections and packet length")
plt.xlabel('Number of parallel connections')
plt.ylabel('Average Latency ({})'.format(unit_time_str))
plt.grid(axis="y", linestyle="dashed", zorder=0)
plt.savefig("plots/avg_latency_linux.svg")


# Do the same for LwIP-DPDK
# AVG THROUGHPUT
df_server_dpdk = df2.loc[['server-dpdk']].pivot("n_connections", "pkt_length", "avg_throughput")
yerr = df2.loc[['server-dpdk']].pivot("n_connections", "pkt_length", "std_avg_throughput")
df_server_dpdk.plot(kind='bar', yerr=yerr, rot=0)
plt.title("Average Throughput/Connection  of LwIP-DPDK server for \n various number of parallel connections and packet length")
plt.xlabel('Number of parallel connections')
plt.ylabel('Average Throughput/Connection  ({})'.format(unit_tr_str))
plt.grid(axis="y", linestyle="dashed", zorder=0)
plt.savefig("plots/avg_tr_dpdk.svg")

# TOTAL THROUGHPUT
df_server_dpdk = df2.loc[['server-dpdk']].pivot("n_connections", "pkt_length", "total_throughput")
yerr = df2.loc[['server-dpdk']].pivot("n_connections", "pkt_length", "std_total_throughput")
df_server_dpdk.plot(kind='bar', yerr=yerr, rot=0)
plt.title("Total Throughput of LwIP-DPDK  server for \n various number of parallel connections and packet length")
plt.xlabel('Number of parallel connections')
plt.ylabel('Total Throughput ({})'.format(unit_tr_str))
plt.grid(axis="y", linestyle="dashed", zorder=0)
plt.savefig("plots/total_tr_dpdk.svg")

# AVG LATENCY
df_server_dpdk = df2.loc[['server-dpdk']].pivot("n_connections", "pkt_length", "avg_latency")
yerr = df2.loc[['server-dpdk']].pivot("n_connections", "pkt_length", "std_avg_latency")
df_server_dpdk.plot(kind='bar', yerr=yerr, rot=0)
plt.title("Average Latency of LwIP-DPDK  server for \n various number of parallel connections and packet length")
plt.xlabel('Number of parallel connections')
plt.ylabel('Average Latency ({})'.format(unit_time_str))
plt.grid(axis="y", linestyle="dashed", zorder=0)
plt.savefig("plots/avg_latency_dpdk.svg")


###### Compare servers ######
#Compare average throughput

df1_comp = df1.reset_index()
df1_comp = df1_comp.rename(columns={"index": "Implementation"})

df2_comp = df2.reset_index()
df2_comp = df2_comp.rename(columns={"index": "Implementation"})

df_comp = df1_comp.append(df2_comp)
print(df_comp)

pkt_lengths = [1, 100, 500]

#Compare average throughput
for pkt_length in pkt_lengths:
    df_comp_fixed = df_comp[df_comp['pkt_length'] == pkt_length]

    df_comp_fixed_temp = df_comp_fixed.pivot("n_connections", "Implementation", "avg_throughput")
    yerr = df_comp_fixed.pivot("n_connections", "Implementation", "std_avg_throughput")
    df_comp_fixed_temp.plot(kind='bar', yerr=yerr, rot=0)
    plt.title("Average Throughput/Connection comparison for \n various number of parallel connections and packet length={}".format(pkt_length))
    plt.xlabel('Number of parallel connections')
    plt.ylabel('Average Throughput/Connection ({})'.format(unit_tr_str))
    plt.grid(axis="y", linestyle="dashed", zorder=0)
    plt.savefig("plots/compare_avg_tr_length={}.svg".format(pkt_length))

#Compare total throughput
for pkt_length in pkt_lengths:
    df_comp_fixed = df_comp[df_comp['pkt_length'] == pkt_length]

    df_comp_fixed_temp = df_comp_fixed.pivot("n_connections", "Implementation", "total_throughput")
    yerr = df_comp_fixed.pivot("n_connections", "Implementation", "std_total_throughput")
    df_comp_fixed_temp.plot(kind='bar', yerr=yerr, rot=0)
    plt.title("Total Throughput comparison for \n various number of parallel connections and packet length={}".format(pkt_length))
    plt.xlabel('Number of parallel connections')
    plt.ylabel('Total Throughput ({})'.format(unit_tr_str))
    plt.grid(axis="y", linestyle="dashed", zorder=0)
    plt.savefig("plots/compare_total_tr_length={}.svg".format(pkt_length))

#Compare average latency
for pkt_length in pkt_lengths:
    df_comp_fixed = df_comp[df_comp['pkt_length'] == pkt_length]

    df_comp_fixed_temp = df_comp_fixed.pivot("n_connections", "Implementation", "avg_latency")
    yerr = df_comp_fixed.pivot("n_connections", "Implementation", "std_avg_latency")
    df_comp_fixed_temp.plot(kind='bar', yerr=yerr, rot=0)
    plt.title("Average Latency comparison for \n various number of parallel connections and packet length={}".format(pkt_length))
    plt.xlabel('Number of parallel connections')
    plt.ylabel('Average Latency ({})'.format(unit_time_str))
    plt.grid(axis="y", linestyle="dashed", zorder=0)
    plt.savefig("plots/compare_latency_length={}.svg".format(pkt_length))

plt.close("all")