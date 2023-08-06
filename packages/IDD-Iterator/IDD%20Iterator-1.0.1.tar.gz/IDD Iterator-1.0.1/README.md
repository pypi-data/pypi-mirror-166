# IDD Iterator

![pylint workflow](https://github.com/AdityaNG/idd_iterator/actions/workflows/pylint.yml/badge.svg)
![pypi workflow](https://github.com/AdityaNG/idd_iterator/actions/workflows/pypi.yml/badge.svg)
![pytest workflow](https://github.com/AdityaNG/idd_iterator/actions/workflows/pytest.yml/badge.svg)

```python
from idd_iterator import idd_multimodal_iterator
multimodal_iter = idd_multimodal_iterator.IDDMultimodalIterator()
```

## Install

```
pip install git+https://github.com/AdityaNG/idd_iterator
```

## Dataset Structre

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