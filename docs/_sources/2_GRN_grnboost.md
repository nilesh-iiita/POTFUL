# Gene regulatory network inference


```python
import os
import re

import pandas as pd
from collections import defaultdict

from arboreto.algo import grnboost2, genie3
from arboreto.utils import load_tf_names
from distributed import LocalCluster, Client
```


```python
tfdf = pd.read_csv("Auxiliary_File/Arabidopsis_TF and family.csv")
tf_names = list(set(tfdf['Protein ID'].values.tolist()))
len(tf_names)
```




    2192



## Uncut


```python
# Exp = pd.read_csv("1_Expression_data/Expr_Uncut.csv")
# Exp.T

ex_matrix = pd.read_csv("1_Expression_data/Expr_Uncut.csv", sep=',', index_col=0).T
ex_matrix.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>Locus</th>
      <th>AT1G01010</th>
      <th>AT1G01020</th>
      <th>AT1G01030</th>
      <th>AT1G01040</th>
      <th>AT1G01046</th>
      <th>AT1G01050</th>
      <th>AT1G01060</th>
      <th>AT1G01070</th>
      <th>AT1G01073</th>
      <th>AT1G01080</th>
      <th>...</th>
      <th>ATMG01330</th>
      <th>ATMG01340</th>
      <th>ATMG01350</th>
      <th>ATMG01360</th>
      <th>ATMG01370</th>
      <th>ATMG01380</th>
      <th>ATMG01390</th>
      <th>ATMG01400</th>
      <th>ATMG01410</th>
      <th>CFP</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>wolsc_kb2_4_10</th>
      <td>7.702431</td>
      <td>0.000000</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.000000</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>10.359552</td>
    </tr>
    <tr>
      <th>wolsc_kb2_4_1</th>
      <td>0.000000</td>
      <td>8.378906</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>10.810870</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>wolsc_kb2_4_18</th>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>9.858738</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>wolsc_kb2_4_22</th>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.000000</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>6.388047</td>
    </tr>
    <tr>
      <th>wolsc_kb2_4_26</th>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>5.779188</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>4.552472</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 32679 columns</p>
</div>




```python
%%time
# tfdf = pd.read_csv("masterTF-target.txt", sep="\t")
# tf_names = list(set(tfdf.TF.values.tolist()))
# len(tf_names)

# ex_matrix = pd.read_csv("1_Expression_data/GSE10576_Fe_arboreto.tsv", sep='\t')
# ex_matrix.head()


local_cluster = LocalCluster(n_workers=10,
                                 threads_per_worker=1,
                                 memory_limit=8e9)
custom_client = Client(local_cluster)

network = grnboost2(expression_data=ex_matrix,
                    tf_names=tf_names, verbose=True, client_or_address=custom_client)

network.to_csv('3_GRN_data/GSE74488_Uncut_arboreto_regnet.tsv', sep='\t', index=False)

network.head()
```

    preparing dask client
    parsing input
    creating dask graph
    10 partitions
    computing dask graph
    not shutting down client, client was created externally
    finished
    CPU times: total: 47min 22s
    Wall time: 2h 5min 40s
    




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>TF</th>
      <th>target</th>
      <th>importance</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>287</th>
      <td>AT1G34190</td>
      <td>AT1G54150</td>
      <td>123.624165</td>
    </tr>
    <tr>
      <th>280</th>
      <td>AT1G33240</td>
      <td>AT1G32640</td>
      <td>118.439476</td>
    </tr>
    <tr>
      <th>1375</th>
      <td>AT4G01120</td>
      <td>AT3G02180</td>
      <td>116.013558</td>
    </tr>
    <tr>
      <th>1837</th>
      <td>AT5G20900</td>
      <td>AT2G46140</td>
      <td>115.321538</td>
    </tr>
    <tr>
      <th>41</th>
      <td>AT1G04990</td>
      <td>AT2G42230</td>
      <td>112.942165</td>
    </tr>
  </tbody>
</table>
</div>



## 3hpc


```python
ex_matrix = pd.read_csv("1_Expression_data/Expr_3hpc.csv", sep=',', index_col=0).T
ex_matrix.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>Locus</th>
      <th>AT1G01010</th>
      <th>AT1G01020</th>
      <th>AT1G01030</th>
      <th>AT1G01040</th>
      <th>AT1G01046</th>
      <th>AT1G01050</th>
      <th>AT1G01060</th>
      <th>AT1G01070</th>
      <th>AT1G01073</th>
      <th>AT1G01080</th>
      <th>...</th>
      <th>ATMG01330</th>
      <th>ATMG01340</th>
      <th>ATMG01350</th>
      <th>ATMG01360</th>
      <th>ATMG01370</th>
      <th>ATMG01380</th>
      <th>ATMG01390</th>
      <th>ATMG01400</th>
      <th>ATMG01410</th>
      <th>CFP</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>sc_1228_pa_30</th>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>5.380400</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>4.009010</td>
    </tr>
    <tr>
      <th>wolsc_kb2_3_13</th>
      <td>0.000000</td>
      <td>7.092747</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>10.358681</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>wolsc_kb2_3_14</th>
      <td>0.000000</td>
      <td>5.949744</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>9.528396</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>6.615233</td>
    </tr>
    <tr>
      <th>wolsc_kb2_3_2</th>
      <td>3.829904</td>
      <td>7.912041</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>10.317229</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>11.349404</td>
    </tr>
    <tr>
      <th>wolsc_kb2_3_27</th>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>8.714814</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>8.626259</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 32679 columns</p>
</div>




```python
local_cluster = LocalCluster(n_workers=10,
                                 threads_per_worker=1,
                                 memory_limit=8e9)
custom_client = Client(local_cluster)

network = grnboost2(expression_data=ex_matrix,
                    tf_names=tf_names, verbose=True, client_or_address=custom_client)

network.to_csv('3_GRN_data/GSE74488_3hpc_arboreto_regnet.tsv', sep='\t', index=False)

network.head()
```

    preparing dask client
    parsing input
    creating dask graph
    10 partitions
    computing dask graph
    

    2022-09-26 15:38:38,710 - distributed.scheduler - WARNING - Worker failed to heartbeat within 300 seconds. Closing: <WorkerState 'tcp://127.0.0.1:59010', name: 3, status: running, memory: 1294, processing: 2851>
    2022-09-26 15:38:40,154 - distributed.scheduler - WARNING - Worker failed to heartbeat within 300 seconds. Closing: <WorkerState 'tcp://127.0.0.1:59016', name: 2, status: running, memory: 1290, processing: 4233>
    2022-09-26 15:38:43,509 - distributed.scheduler - WARNING - Worker failed to heartbeat within 300 seconds. Closing: <WorkerState 'tcp://127.0.0.1:59022', name: 0, status: running, memory: 1312, processing: 2648>
    2022-09-26 15:38:44,025 - distributed.scheduler - WARNING - Worker failed to heartbeat within 300 seconds. Closing: <WorkerState 'tcp://127.0.0.1:59028', name: 1, status: running, memory: 1181, processing: 4211>
    2022-09-26 15:38:44,917 - distributed.scheduler - WARNING - Worker failed to heartbeat within 300 seconds. Closing: <WorkerState 'tcp://127.0.0.1:59034', name: 5, status: running, memory: 861, processing: 5912>
    2022-09-26 15:38:46,231 - distributed.scheduler - WARNING - Received heartbeat from unregistered worker 'tcp://127.0.0.1:59010'.
    2022-09-26 15:38:46,237 - distributed.scheduler - WARNING - Received heartbeat from unregistered worker 'tcp://127.0.0.1:59028'.
    2022-09-26 15:38:46,240 - distributed.scheduler - WARNING - Received heartbeat from unregistered worker 'tcp://127.0.0.1:59034'.
    2022-09-26 15:38:46,248 - distributed.scheduler - WARNING - Received heartbeat from unregistered worker 'tcp://127.0.0.1:59022'.
    2022-09-26 15:38:46,252 - distributed.scheduler - WARNING - Received heartbeat from unregistered worker 'tcp://127.0.0.1:59016'.
    2022-09-26 15:38:49,243 - distributed.nanny - WARNING - Restarting worker
    2022-09-26 15:38:49,265 - distributed.nanny - WARNING - Restarting worker
    2022-09-26 15:38:49,274 - distributed.nanny - WARNING - Restarting worker
    2022-09-26 15:38:49,286 - distributed.nanny - WARNING - Restarting worker
    2022-09-26 15:38:49,957 - distributed.nanny - WARNING - Restarting worker
    

    not shutting down client, client was created externally
    finished
    




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>TF</th>
      <th>target</th>
      <th>importance</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>421</th>
      <td>AT1G62990</td>
      <td>AT4G09990</td>
      <td>123.463492</td>
    </tr>
    <tr>
      <th>421</th>
      <td>AT1G62990</td>
      <td>AT3G18660</td>
      <td>96.355794</td>
    </tr>
    <tr>
      <th>902</th>
      <td>AT2G42680</td>
      <td>AT4G32470</td>
      <td>91.878618</td>
    </tr>
    <tr>
      <th>2006</th>
      <td>AT5G49450</td>
      <td>AT5G49448</td>
      <td>89.479224</td>
    </tr>
    <tr>
      <th>660</th>
      <td>AT2G18160</td>
      <td>AT2G18162</td>
      <td>88.655565</td>
    </tr>
  </tbody>
</table>
</div>



END
