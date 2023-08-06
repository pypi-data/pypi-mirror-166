import os

import pandas as pd
import numpy as np
import cv2


class IDDMultimodalIterator:

    def __init__(self,
        index="d0",
        idd_multimodal_path="idd_multimodal/",
        enable_lidar=False,
        enable_obd=False
    ):
        self.enable_lidar = enable_lidar
        self.enable_obd = enable_obd
        assert os.path.exists(idd_multimodal_path)

        self.index = 0
        self.idd_index = index
        self.supplement_path = os.path.join(idd_multimodal_path, "supplement")
        self.secondary_path = os.path.join(idd_multimodal_path, "secondary", self.idd_index)
        self.primary_path = os.path.join(idd_multimodal_path, "primary", self.idd_index)
        self.csv_path = os.path.join(self.primary_path, "train.csv")
        self.left_path = os.path.join(self.primary_path, "leftCamImgs")
        self.right_path = os.path.join(self.secondary_path, "rightCamImgs")
        self.lidar_path = os.path.join(self.supplement_path, "lidar", self.idd_index)
        self.obd_csv_path = os.path.join(self.supplement_path, "obd", self.idd_index, "obd.csv")

        assert os.path.exists(self.supplement_path)
        assert os.path.exists(self.secondary_path)
        assert os.path.exists(self.primary_path)
        assert os.path.exists(self.csv_path)
        assert os.path.exists(self.left_path)
        assert os.path.exists(self.right_path)
        assert os.path.exists(self.lidar_path)
        assert os.path.exists(self.obd_csv_path)

        self.idd_dataframe = pd.read_csv(self.csv_path)
        if self.enable_obd:
            self.obd_df = pd.read_csv(self.obd_csv_path)
        else:
            self.obd_df = None

    def __len__(self):
        return len(self.idd_dataframe)

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index >= self.__len__():
            raise StopIteration
        data = self.__getitem__(self.index)
        self.index += 1
        return data

    def __getitem__(self, index):
        row = self.idd_dataframe.iloc[index]
        timestamp_str, image_idx, latitude, longitude, altitude = row
        hrs, mins, secs, mss = list(map(float, timestamp_str.split("-")))
        timestamp = hrs*3600.0 + mins*60.0 + secs + mss/1000.0

        lidar_path = os.path.join(self.lidar_path, str(image_idx).zfill(7) + ".npy")
        if self.enable_lidar:
            lidar = np.load(lidar_path)
        else:
            lidar = None
        left_img_path = os.path.join(self.left_path, str(image_idx).zfill(7) + ".jpg")
        right_img_path = os.path.join(self.right_path, str(image_idx).zfill(7) + ".jpg")
        left_img = cv2.imread(left_img_path)
        right_img = cv2.imread(right_img_path)

        if self.enable_obd:
            obd_dat = self.obd_df[self.obd_df["timestamp"]==timestamp_str]
        else:
            obd_dat = None

        return timestamp, left_img, right_img, latitude, longitude, altitude, lidar, obd_dat


def main():
    idd = IDDMultimodalIterator(enable_obd=True)
    for row in idd:
        timestamp, left_img, right_img, _, _, _, _, _ = row
        full_frame = cv2.hconcat([left_img, right_img])
        full_frame = cv2.resize(full_frame, (0,0), fx=0.25, fy=0.25)
        cv2.imshow('full_frame', full_frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        print(timestamp)

if __name__ == "__main__":
    main()
