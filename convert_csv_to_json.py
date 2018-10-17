import json
import numpy as np
import pandas as pd
import sys

def convert(csv_path, output_path, mode):
    if mode == 'gt':
        bbox_field = 'annotations'
    elif mode == 'hyp':
        bbox_field = 'hypotheses'
    else:
        print("Please use mode 'gt' or 'hyp'.")
        sys.exit(1)
    df = pd.read_csv(csv_path)
    entries = []
    for filename in sorted(np.unique(df['filename'])):
        file_df = df[df['filename'] == filename]
        frame_nos = sorted(np.unique(file_df['frame_no']))
        bbox_entries = []
        for frame_no in frame_nos:
            boxes = []
            for i, row in file_df[file_df['frame_no'] == frame_no].iterrows():
                xmin, ymin, xmax, ymax, obj_id = \
                    row[['xmin', 'ymin', 'xmax', 'ymax', 'obj_id']]
                if obj_id < 0:
                    continue
                height, width = ymax - ymin, xmax - xmin
                box = dict(height=height, width=width,
                           y=ymin, x=xmin, id=obj_id)
                boxes.append(box)
            bbox_entry = {'timestamp': frame_no, 'num': frame_no,
                          'class': 'frame', bbox_field: boxes}
            bbox_entries.append(bbox_entry)
        entry = {'frames': bbox_entries, 'class': 'video', 'filename': filename}
        entries.append(entry)
    json.dump(entries, open(output_path, 'w'))

if __name__ == '__main__':
    csv_path = sys.argv[1]
    output_path = sys.argv[2] 
    mode = sys.argv[3]
    convert(csv_path, output_path, mode)
