# Script used to create and save plots using the data collected during the experiments

import matplotlib.pyplot as plt
import pandas as pd

df1 = pd.read_csv('data1.csv', index_col=0)
print(df1)

df2 = pd.read_csv('data2.csv', index_col=0)
print(df2)

# AVG THROUGHPUT
df_server_linux = df1.loc[['server-linux']].pivot("n_connections", "pkt_length", "avg_throughput").plot(kind='bar')
plt.title("Average Throughput of Linux server for various number of parallel connections and packet length")
plt.xlabel('Number of parallel connections')
plt.ylabel('Average Throughput (GB/s)')
plt.grid(axis="y", linestyle="dashed", zorder=0)
plt.savefig("plots/avg_tr_linux.svg")

# TOTAL THROUGHPUT
df_server_linux = df1.loc[['server-linux']].pivot("n_connections", "pkt_length", "total_throughput").plot(kind='bar')
plt.title("Total Throughput of Linux server for various number of parallel connections and packet length")
plt.xlabel('Number of parallel connections')
plt.ylabel('Total Throughput (GB/s)')
plt.grid(axis="y", linestyle="dashed", zorder=0)
plt.savefig("plots/total_tr_linux.svg")

# AVG LATENCY
df_server_linux = df1.loc[['server-linux']].pivot("n_connections", "pkt_length", "avg_latency").plot(kind='bar')
plt.title("Average Latency of Linux server for various number of parallel connections and packet length")
plt.xlabel('Number of parallel connections')
plt.ylabel('Average Latency (s)')
plt.grid(axis="y", linestyle="dashed", zorder=0)
plt.savefig("plots/avg_latency_linux.svg")


# Do the same for LwIP-DPDK
# AVG THROUGHPUT
df_server_dpdk = df2.loc[['server-dpdk']].pivot("n_connections", "pkt_length", "avg_throughput").plot(kind='bar')
plt.title("Average Throughput of LwIP-DPDK server for various number of parallel connections and packet length")
plt.xlabel('Number of parallel connections')
plt.ylabel('Average Throughput (GB/s)')
plt.grid(axis="y", linestyle="dashed", zorder=0)
plt.savefig("plots/avg_tr_dpdk.svg")

# TOTAL THROUGHPUT
df_server_dpdk = df2.loc[['server-dpdk']].pivot("n_connections", "pkt_length", "total_throughput").plot(kind='bar')
plt.title("Total Throughput of LwIP-DPDK  server for various number of parallel connections and packet length")
plt.xlabel('Number of parallel connections')
plt.ylabel('Total Throughput (GB/s)')
plt.grid(axis="y", linestyle="dashed", zorder=0)
plt.savefig("plots/total_tr_dpdk.svg")

# AVG LATENCY
df_server_dpdk = df2.loc[['server-dpdk']].pivot("n_connections", "pkt_length", "avg_latency").plot(kind='bar')
plt.title("Average Latency of LwIP-DPDK  server for various number of parallel connections and packet length")
plt.xlabel('Number of parallel connections')
plt.ylabel('Average Latency (s)')
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
for pkt_length in pkt_lengths:
    df_comp_fixed = df_comp[df_comp['pkt_length'] == pkt_length]

    df_comp_fixed = df_comp_fixed.pivot("n_connections", "Implementation", "avg_throughput").plot(kind='bar')
    plt.title("Average Throughput comparison for various number of parallel connections and packet length={}".format(pkt_length))
    plt.xlabel('Number of parallel connections')
    plt.ylabel('Average Throughput (GB/s)')
    plt.grid(axis="y", linestyle="dashed", zorder=0)
    plt.savefig("plots/compare_tr_length={}.svg".format(pkt_length))


#Compare average latency
for pkt_length in pkt_lengths:
    df_comp_fixed = df_comp[df_comp['pkt_length'] == pkt_length]

    df_comp_fixed = df_comp_fixed.pivot("n_connections", "Implementation", "avg_latency").plot(kind='bar')
    plt.title("Average Latency comparison for various number of parallel connections and packet length={}".format(pkt_length))
    plt.xlabel('Number of parallel connections')
    plt.ylabel('Average Latency (s)')
    plt.grid(axis="y", linestyle="dashed", zorder=0)
    plt.savefig("plots/compare_latency_length={}.svg".format(pkt_length))

plt.close("all")