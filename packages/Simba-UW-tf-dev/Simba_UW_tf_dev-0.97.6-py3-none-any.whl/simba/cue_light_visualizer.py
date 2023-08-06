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
        self.space_scale, radius_scale, res_scale, font_scale = 25, 10, 1500, 0.8
        max_dim = max(self.video_meta_data['width'], self.video_meta_data['height'])
        self.draw_scale, self.font_size = int(radius_scale / (res_scale / max_dim)), float(font_scale / (res_scale / max_dim))
        self.spacing_scaler = int(self.space_scale / (res_scale / max_dim))
        self.read_roi_dfs()

    def update_video_meta_data(self):
        new_cap = cv2.VideoCapture(self.video_path)
        new_cap.set(1, 1)
        _, img = self.cap.read()
        bordered_img = cv2.copyMakeBorder(img, 0, 0, 0, int(self.video_meta_data['width']), borderType=cv2.BORDER_CONSTANT, value=[0, 0, 0])
        self.border_img_h, self.border_img_w = bordered_img.shape[0], bordered_img.shape[1]
        new_cap.release()


    def read_roi_dfs(self):
        if not os.path.isfile(os.path.join(self.logs_path, 'measures', 'ROI_definitions.h5')):
            raise FileNotFoundError(print('No ROI definitions were found in your SimBA project. Please draw some ROIs before analyzing your ROI data'))
        else:
            self.roi_h5_path = os.path.join(self.logs_path, 'measures', 'ROI_definitions.h5')
            self.rectangles_df = pd.read_hdf(self.roi_h5_path, key='rectangles')
            self.circles_df = pd.read_hdf(self.roi_h5_path, key='circleDf')
            self.polygon_df = pd.read_hdf(self.roi_h5_path, key='polygons')
            self.shape_names = list(itertools.chain(self.rectangles_df['Name'].unique(), self.circles_df['Name'].unique(), self.polygon_df['Name'].unique()))
            self.video_recs = self.rectangles_df.loc[(self.rectangles_df['Video'] == self.video_name) & (self.rectangles_df['Name'].isin(self.cue_light_names))]
            self.video_circs = self.circles_df.loc[(self.circles_df['Video'] == self.video_name)  & (self.circles_df['Name'].isin(self.cue_light_names))]
            self.video_polys = self.polygon_df.loc[(self.polygon_df['Video'] == self.video_name) & (self.polygon_df['Name'].isin(self.cue_light_names))]
            self.shape_names = list(itertools.chain(self.rectangles_df['Name'].unique(), self.circles_df['Name'].unique(),self.polygon_df['Name'].unique()))


    def calc_text_locs(self):
        add_spacer = 2
        self.loc_dict = {}
        for light_cnt, light_name in enumerate(self.cue_light_names):
            self.loc_dict[light_name] = {}
            self.loc_dict[light_name]['status_text'] = '{} {}'.format(light_name, 'status:')
            self.loc_dict[light_name]['onset_cnt_text'] = '{} {}'.format(light_name, 'onset counts:')
            self.loc_dict[light_name]['seconds_on_text'] = '{} {}'.format(light_name, 'time ON:')
            self.loc_dict[light_name]['seconds_off_text'] = '{} {}'.format(light_name, 'time OFF:')
            self.loc_dict[light_name]['status_text_loc'] = ((self.video_meta_data['width'] + 5), (self.video_meta_data['height'] - (self.video_meta_data['height'] + 10) + self.spacing_scaler * add_spacer))
            self.loc_dict[light_name]['status_data_loc'] = (int(self.border_img_w-(self.border_img_w/8)), (self.video_meta_data['height'] - (self.video_meta_data['height'] + 10) + self.spacing_scaler*add_spacer))
            add_spacer += 1
            self.loc_dict[light_name]['onset_cnt_text_loc'] = ((self.video_meta_data['width'] + 5), (self.video_meta_data['height'] - (self.video_meta_data['height'] + 10) + self.spacing_scaler * add_spacer))
            self.loc_dict[light_name]['onset_cnt_data_loc'] = (int(self.border_img_w-(self.border_img_w/8)), (self.video_meta_data['height'] - (self.video_meta_data['height'] + 10) + self.spacing_scaler*add_spacer))
            add_spacer += 1
            self.loc_dict[light_name]['seconds_on_text_loc'] = ((self.video_meta_data['width'] + 5), (self.video_meta_data['height'] - (self.video_meta_data['height'] + 10) + self.spacing_scaler * add_spacer))
            self.loc_dict[light_name]['seconds_on_data_loc'] = (int(self.border_img_w - (self.border_img_w / 8)), (self.video_meta_data['height'] - (self.video_meta_data['height'] + 10) + self.spacing_scaler * add_spacer))
            add_spacer += 1
            self.loc_dict[light_name]['seconds_off_text_loc'] = ((self.video_meta_data['width'] + 5), (self.video_meta_data['height'] - (self.video_meta_data['height'] + 10) + self.spacing_scaler * add_spacer))
            self.loc_dict[light_name]['seconds_off_data_loc'] = (int(self.border_img_w - (self.border_img_w / 8)), (self.video_meta_data['height'] - (self.video_meta_data['height'] + 10) + self.spacing_scaler * add_spacer))
            add_spacer += 1


    def create_text_dict(self):
        self.light_dict = {}
        for light_cnt, light_name in enumerate(self.cue_light_names):
            self.light_dict[light_name] = {}
            self.light_dict[light_name]['status'] = False
            self.light_dict[light_name]['onsets'] = False
            self.light_dict[light_name]['time_on'] = False
            self.light_dict[light_name]['time_off'] = False

    def draw_shapes_and_text(self, shape_row):


    def insert_texts_and_shapes(self):
        for light_cnt, light_name in enumerate(self.cue_light_names):
            for i, r in self.video_recs.iterrows():
                if light_name == r['Name']:
                    draw_shapes_and_text()
                    cv2.putText(self.border_img, self.loc_dict[light_name]['timer_text'], self.loc_dict[animal_name][shape_name]['timer_text_loc'], self.font, self.font_size, shape_color, 1)
                # cv2.putText(self.border_img, self.loc_dict[animal_name][shape_name]['entries_text'], self.loc_dict[animal_name][shape_name]['entries_text_loc'], self.font, self.font_size, shape_color, 1)

    def visualize_cue_light_data(self):
        self.cap = cv2.VideoCapture(self.video_path)
        frame_cnt = 0
        self.update_video_meta_data()
        self.calc_text_locs()
        self.create_text_dict()
        while (self.cap.isOpened()):
            _, img = self.cap.read()
            self.border_img = cv2.copyMakeBorder(img, 0, 0, 0, int(self.video_meta_data['width']), borderType=cv2.BORDER_CONSTANT, value=[0, 0, 0])
            self.border_img_h, self.border_img_w = self.border_img.shape[0], self.border_img.shape[1]
            self.insert_texts_and_shapes()


            break










test = CueLightVisualizer(config_path='/Users/simon/Desktop/troubleshooting/light_analyzer/project_folder/project_config.ini',
                          cue_light_names=['Cue_light'],
                          video_path='/Users/simon/Desktop/troubleshooting/light_analyzer/project_folder/videos/20220422_ALMEAG02_B0.avi')
test.visualize_cue_light_data()