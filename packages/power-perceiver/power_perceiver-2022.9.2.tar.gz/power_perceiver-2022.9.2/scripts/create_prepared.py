import glob
import os
from pathlib import Path

import numpy as np

from power_perceiver.load_prepared_batches.prepared_dataset import PreparedDataset
from power_perceiver.load_prepared_batches.data_sources import PV, GSP, HRVSatellite, NWP
from power_perceiver.production.model import FullModel
import pandas as pd
from torch.utils.data import DataLoader

dataset = PreparedDataset([PV(history_duration=pd.Timedelta("90 min"),),
                           GSP(history_duration=pd.Timedelta("2 hours"),),
                           HRVSatellite(history_duration=pd.Timedelta("30 min"),),
                           NWP(history_duration=pd.Timedelta("1 hour"),)],
                          data_path=Path("/home/jacob/Development/power_perceiver/data_for_testing/"))
print(dataset)
dataloader = DataLoader(dataset, num_workers=0, batch_size=None)
batch = next(iter(dataloader))
model = FullModel().eval()
model(batch)
for key, value in batch.items():
    if isinstance(value, np.ndarray):
        print(f"{key}: {value.shape}")
    else:
        print(f"{key}: {value}")

