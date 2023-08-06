import os
import glob
import datetime

import pandas as pd
import numpy as np
import cv2


class IDDMultimodalIterator:
    def __init__(self, index="d0", idd_multimodal_path="idd_multimodal/", enable_lidar=False, enable_obd=False):
        self.enable_lidar = enable_lidar
        self.enable_obd = enable_obd
        
        assert os.path.exists(idd_multimodal_path)

        self.INDEX = "d0"
        self.SUPPLEMENT_PATH = os.path.join(idd_multimodal_path, "supplement")
        self.SECONDARY_PATH = os.path.join(idd_multimodal_path, "secondary", self.INDEX)
        self.PRIMARY_PATH = os.path.join(idd_multimodal_path, "primary", self.INDEX)
        self.CSV_PATH = os.path.join(self.PRIMARY_PATH, "train.csv")
        self.LEFT_PATH = os.path.join(self.PRIMARY_PATH, "leftCamImgs")
        self.RIGHT_PATH = os.path.join(self.SECONDARY_PATH, "rightCamImgs")
        self.LIDAR_PATH = os.path.join(self.SUPPLEMENT_PATH, "lidar", self.INDEX)
        self.OBD_CSV_PATH = os.path.join(self.SUPPLEMENT_PATH, "obd", self.INDEX, "obd.csv")

        assert os.path.exists(self.SUPPLEMENT_PATH)
        assert os.path.exists(self.SECONDARY_PATH)
        assert os.path.exists(self.PRIMARY_PATH)
        assert os.path.exists(self.CSV_PATH)
        assert os.path.exists(self.LEFT_PATH)
        assert os.path.exists(self.RIGHT_PATH)
        assert os.path.exists(self.LIDAR_PATH)
        assert os.path.exists(self.OBD_CSV_PATH)
        
        self.df = pd.read_csv(self.CSV_PATH)
        if self.enable_obd:
            self.obd_df = pd.read_csv(self.OBD_CSV_PATH)
        else:
            self.obd_df = None
    
    def __len__(self):
        return len(self.df)

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
        row = self.df.iloc[index]
        timestamp_str, image_idx, latitude, longitude, altitude = row
        hrs, mins, secs, mss = list(map(float, timestamp_str.split("-")))
        timestamp = hrs*3600.0 + mins*60.0 + secs + mss/1000.0

        lidar_path = os.path.join(self.LIDAR_PATH, str(image_idx).zfill(7) + ".npy")
        if self.enable_lidar:
            lidar = np.load(lidar_path)
        else:
            lidar = None
        left_img_path = os.path.join(self.LEFT_PATH, str(image_idx).zfill(7) + ".jpg")
        right_img_path = os.path.join(self.RIGHT_PATH, str(image_idx).zfill(7) + ".jpg")
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
        timestamp, left_img, right_img, latitude, longitude, altitude, lidar, obd_dat = row
        full_frame = cv2.hconcat([left_img, right_img])
        full_frame = cv2.resize(full_frame, (0,0), fx=0.25, fy=0.25)
        cv2.imshow('full_frame', full_frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        print(timestamp)

if __name__ == "__main__":
    main()