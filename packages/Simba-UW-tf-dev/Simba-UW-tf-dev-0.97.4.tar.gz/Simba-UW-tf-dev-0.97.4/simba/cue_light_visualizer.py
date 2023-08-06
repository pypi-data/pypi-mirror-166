from simba.read_config_unit_tests import (read_config_entry, read_config_file, check_file_exist_and_readable)
from simba.features_scripts.unit_tests import read_video_info_csv, read_video_info
from simba.misc_tools import get_video_meta_data
import glob, itertools, os
from simba.drop_bp_cords import get_fn_ext
from simba.rw_dfs import read_df
import pandas as pd
import cv2



class CueLightVisualizer(object):
    def __init__(self,
                 config_path: str=None,
                 cue_light_names: list=None,
                 video_path: str=None):
        self.config = read_config_file(config_path)
        self.project_path = read_config_entry(self.config, 'General settings', 'project_path', data_type='folder_path')
        self.in_dir = os.path.join(self.project_path, 'csv', 'outlier_corrected_movement_location')
        self.file_type = read_config_entry(self.config, 'General settings', 'workflow_file_type', 'str', 'csv')
        self.cue_light_names, self.video_path = cue_light_names, video_path
        _, self.video_name, _ = get_fn_ext(video_path)
        self.video_meta_data = get_video_meta_data(self.video_path)
        self.logs_path, self.video_dir = os.path.join(self.project_path, 'logs'), os.path.join(self.project_path, 'videos')
        self.data_file_path = os.path.join(self.in_dir, self.video_name + '.' + self.file_type)
        check_file_exist_and_readable(self.data_file_path)
        self.data_df = read_df(self.data_file_path, self.file_type)
        self.vid_info_df = read_video_info_csv(os.path.join(self.project_path, 'logs', 'video_info.csv'))
        self.video_settings, pix_per_mm, self.fps = read_video_info(self.vid_info_df, self.video_name)


    def read_roi_dfs(self):
        if not os.path.isfile(os.path.join(self.logs_path, 'measures', 'ROI_definitions.h5')):
            raise FileNotFoundError(print('No ROI definitions were found in your SimBA project. Please draw some ROIs before analyzing your ROI data'))
        else:
            self.roi_h5_path = os.path.join(self.logs_path, 'measures', 'ROI_definitions.h5')
            self.rectangles_df = pd.read_hdf(self.roi_h5_path, key='rectangles')
            self.circles_df = pd.read_hdf(self.roi_h5_path, key='circleDf')
            self.polygon_df = pd.read_hdf(self.roi_h5_path, key='polygons')
            self.shape_names = list(itertools.chain(self.rectangles_df['Name'].unique(), self.circles_df['Name'].unique(), self.polygon_df['Name'].unique()))


    def visualize_cue_light_data(self):
        self.cap = cv2.VideoCapture(self.video_path)
        frame_cnt = 0
        while (self.cap.isOpened()):
            _, img = self.cap.read()
            self.border_img = cv2.copyMakeBorder(img, 0, 0, 0, int(self.video_meta_data['width']), borderType=cv2.BORDER_CONSTANT, value=[0, 0, 0])










test = CueLightVisualizer(config_path='/Users/simon/Desktop/troubleshooting/light_analyzer/project_folder/project_config.ini',
                          cue_light_names=['Cue_light'],
                          video_name='/Users/simon/Desktop/troubleshooting/light_analyzer/project_folder/videos/20220422_ALMEAG02_B0.avi')