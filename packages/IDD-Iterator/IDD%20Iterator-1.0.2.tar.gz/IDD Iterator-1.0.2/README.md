# IDD Iterator

![pylint workflow](https://github.com/AdityaNG/idd_iterator/actions/workflows/pylint.yml/badge.svg)
![pypi workflow](https://github.com/AdityaNG/idd_iterator/actions/workflows/pypi.yml/badge.svg)
![pytest workflow](https://github.com/AdityaNG/idd_iterator/actions/workflows/pytest.yml/badge.svg)

Example usage:

```python
from idd_iterator import idd_multimodal_iterator

# Load in the mini dataset
multimodal_iter = idd_multimodal_iterator.IDDMultimodalIterator(
    index="d0",
    idd_multimodal_path="idd_multimodal_mini/",
    enable_lidar=True,
    enable_obd=True
)

# Iterate
for row in idd:
    timestamp, left_img, right_img, latitude, longitude, altitude, lidar, obd_dat = row
    do_something()

# Indexing
timestamp, left_img, right_img, latitude, longitude, altitude, lidar, obd_dat = idd[3]
```

## Install

```bash
pip install idd_iterator
```

To install the latest (might be unstable):
```bash
pip install git+https://github.com/AdityaNG/idd_iterator
```

## Dataset Structre

Download the full dataset at <a href="https://idd.insaan.iiit.ac.in/">idd.insaan.iiit.ac.in</a>

```bash
idd_multimodal_mini/
├── primary
│   └── d0
│       ├── leftCamImgs
│       │   ├── 0000000.jpg
│       │   ├── 0000001.jpg
│       │   ├── 0000002.jpg
│       │   ├── 0000003.jpg
│       │   └── 0000004.jpg
│       ├── test.csv
│       ├── train.csv
│       └── val.csv
├── secondary
│   └── d0
│       └── rightCamImgs
│           ├── 0000000.jpg
│           ├── 0000001.jpg
│           ├── 0000002.jpg
│           ├── 0000003.jpg
│           └── 0000004.jpg
└── supplement
    ├── lidar
    │   └── d0
    │       ├── 0000000.npy
    │       ├── 0000001.npy
    │       ├── 0000002.npy
    │       ├── 0000003.npy
    │       └── 0000004.npy
    └── obd
        └── d0
            └── obd.csv
```