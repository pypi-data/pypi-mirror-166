import trilearn.pgibbs as pg
import pandas as pd

data_filename = "sample_data/czech_autoworkers.csv"
df = pd.read_csv(data_filename, sep=',', header=[0, 1])
N = 5
M = 5
p = df.shape[1]

print(df.head())
traj = pg.sample_trajectory_loglin(df, N, M ,pseudo_obs=1.0, alpha=0.5, beta=0.5, radius=p)
traj.write_adjvec_trajectory("testraj.json")