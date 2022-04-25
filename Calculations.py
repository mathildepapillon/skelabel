import numpy as np
import plotly.graph_objects as go
import plotly

import os
from glob import glob

#############################################################################



def load_mariel_raw(pattern="data/mariel_*.npy"):
    """Load six datasets and perform minimal preprocessing.

    Processing amunts to center each dancer, such that
    the barycenter becomes 0.

    From Pettee 2019:
    Each frame of the dataset is transformed such that the
    overall average (x,y) position per frame is centered at
    the same point and scaled such that all of the coordinates
    fit within the unit cube.
    """
    datasets = {}
    ds_all = []

    exclude_points = [26, 53]
    point_mask = np.ones(55, dtype=bool)
    point_mask[exclude_points] = 0

    for f in sorted(glob(pattern)):
        ds_name = os.path.basename(f)[7:-4]
        ds = np.load(f).transpose((1, 0, 2))
        ds = ds[500:-500, point_mask]

        ds[:, :, 2] *= -1
        # print("\t Min:", np.min(ds, axis=(0, 1)))
        # print("\t Max:", np.max(ds, axis=(0, 1)))

        # ds = filter_points(ds)

        datasets[ds_name] = ds
        ds_all.append(ds)

    ds_counts = np.array([ds.shape[0] for ds in ds_all])
    ds_offsets = np.zeros_like(ds_counts)
    ds_offsets[1:] = np.cumsum(ds_counts[:-1])

    ds_all = np.concatenate(ds_all)
    # print("Full data shape:", ds_all.shape)
    # # print("Offsets:", ds_offsets)

    # # print(ds_all.min(axis=(0,1)))
    low, hi = np.quantile(ds_all, [0.01, 0.99], axis=(0, 1))
    xy_min = min(low[:2])
    xy_max = max(hi[:2])
    xy_range = xy_max - xy_min
    ds_all[:, :, :2] -= xy_min
    ds_all *= 2 / xy_range
    ds_all[:, :, :2] -= 1.0

    # it's also useful to have these datasets centered,
    # i.e. with the x and y offsets
    # subtracted from each individual frame

    ds_all_centered = ds_all.copy()
    ds_all_centered[:, :, :2] -= ds_all_centered[:, :, :2].mean(axis=1, keepdims=True)

    datasets_centered = {}
    for ds in datasets:
        datasets[ds][:, :, :2] -= xy_min
        datasets[ds] *= 2 / xy_range
        datasets[ds][:, :, :2] -= 1.0
        datasets_centered[ds] = datasets[ds].copy()
        datasets_centered[ds][:, :, :2] -= datasets[ds][:, :, :2].mean(
            axis=1, keepdims=True
        )

    # # print(ds_all.min(axis=(0,1)))
    low, hi = np.quantile(ds_all, [0.01, 0.99], axis=(0, 1))
    return ds_all, ds_all_centered, datasets, datasets_centered, ds_counts

def get_seq_data(chosen_seq_len_):
    print(chosen_seq_len_)
    #chosen_seq_len = int(chosen_seq_len)
    ds, ds_c, _, _, _ = load_mariel_raw()
    print('loaded data')
    my_data = ds_c
    seq_data = np.zeros(
        (my_data.shape[0] - chosen_seq_len_, chosen_seq_len_, my_data.shape[1], my_data.shape[2])
    )
    for i in range((my_data.shape[0] - chosen_seq_len_)):
        seq_data[i] = my_data[i : i + chosen_seq_len_]
    print('sequified data')
    return seq_data

# these are the ordered label names of the 53 vertices
# (after the Labeling/SolvingHips points have been excised)
# PS: See http://www.cs.uu.nl/docs/vakken/mcanim/mocap-manual/site/img/markers.png
# for detailed marker definitions
point_labels = [
    "ARIEL",
    "C7",
    "CLAV",
    "LANK",
    "LBHD",
    "LBSH",
    "LBWT",
    "LELB",
    "LFHD",
    "LFRM",
    "LFSH",
    "LFWT",
    "LHEL",
    "LIEL",
    "LIHAND",
    "LIWR",
    "LKNE",
    "LKNI",
    "LMT1",
    "LMT5",
    "LOHAND",
    "LOWR",
    "LSHN",
    "LTHI",
    "LTOE",
    "LUPA",
    # 'LabelingHips',
    "MBWT",
    "MFWT",
    "RANK",
    "RBHD",
    "RBSH",
    "RBWT",
    "RELB",
    "RFHD",
    "RFRM",
    "RFSH",
    "RFWT",
    "RHEL",
    "RIEL",
    "RIHAND",
    "RIWR",
    "RKNE",
    "RKNI",
    "RMT1",
    "RMT5",
    "ROHAND",
    "ROWR",
    "RSHN",
    "RTHI",
    "RTOE",
    "RUPA",
    "STRN",
    # 'SolvingHips',
    "T10",
]

# This array defines the points between which skeletal lines should
# be drawn. Each segment is defined as a line between a group of one
# or more named points -- the line will be drawn at the average position
# of the points in the group
skeleton_lines = [
    #     ( (start group), (end group) ),
    (("LHEL",), ("LTOE",)),  # toe to heel
    (("RHEL",), ("RTOE",)),
    (("LKNE", "LKNI"), ("LHEL",)),  # heel to knee
    (("RKNE", "RKNI"), ("RHEL",)),
    (("LKNE", "LKNI"), ("LFWT", "RFWT", "LBWT", "RBWT")),  # knee to "navel"
    (("RKNE", "RKNI"), ("LFWT", "RFWT", "LBWT", "RBWT")),
    (
        ("LFWT", "RFWT", "LBWT", "RBWT"),
        (
            "STRN",
            "T10",
        ),
    ),  # "navel" to chest
    (
        (
            "STRN",
            "T10",
        ),
        (
            "CLAV",
            "C7",
        ),
    ),  # chest to neck
    (
        (
            "CLAV",
            "C7",
        ),
        (
            "LFSH",
            "LBSH",
        ),
    ),  # neck to shoulders
    (
        (
            "CLAV",
            "C7",
        ),
        (
            "RFSH",
            "RBSH",
        ),
    ),
    (
        (
            "LFSH",
            "LBSH",
        ),
        (
            "LELB",
            "LIEL",
        ),
    ),  # shoulders to elbows
    (
        (
            "RFSH",
            "RBSH",
        ),
        (
            "RELB",
            "RIEL",
        ),
    ),
    (
        (
            "LELB",
            "LIEL",
        ),
        (
            "LOWR",
            "LIWR",
        ),
    ),  # elbows to wrist
    (
        (
            "RELB",
            "RIEL",
        ),
        (
            "ROWR",
            "RIWR",
        ),
    ),
    (("LFHD",), ("LBHD",)),  # draw lines around circumference of the head
    (("LBHD",), ("RBHD",)),
    (("RBHD",), ("RFHD",)),
    (("RFHD",), ("LFHD",)),
    (("LFHD",), ("ARIEL",)),  # connect circumference points to top of head
    (("LBHD",), ("ARIEL",)),
    (("RBHD",), ("ARIEL",)),
    (("RFHD",), ("ARIEL",)),
]


def get_line_segments(seq, zcolor=None, cmap=None):

    # Normal, connected skeleton:
    skeleton_idxs = []
    for g1, g2 in skeleton_lines:
        entry = []
        entry.append([point_labels.index(line) for line in g1])
        entry.append([point_labels.index(line) for line in g2])
        skeleton_idxs.append(entry)

    """Calculate coordinates for the lines."""
    xline = np.zeros((seq.shape[0], len(skeleton_idxs), 3, 2))
    if cmap:
        colors = np.zeros((len(skeleton_idxs), 4))
    for i, (g1, g2) in enumerate(skeleton_idxs):
        xline[:, i, :, 0] = np.mean(seq[:, g1], axis=1)
        xline[:, i, :, 1] = np.mean(seq[:, g2], axis=1)
        if cmap is not None:
            colors[i] = cmap(0.5 * (zcolor[g1].mean() + zcolor[g2].mean()))
    if cmap:
        return xline, colors
    else:
        return xline



def make_dream_x(xline):
    all_x = np.zeros((xline.shape[0], 22*3))

    for pose in range(xline.shape[0]):
        pose_ = xline[pose]

        x_list=[]
        for i in range(pose_.shape[0]):
            x_start = pose_[i,0,0]
            x_end = pose_[i, 0, 1]
            x_list.append(x_start)
            x_list.append(x_end)
            x_list.append(None)

        all_x[pose] = x_list
        
    return all_x

def make_dream_y(xline):
    all_x = np.zeros((xline.shape[0], 22*3))

    for pose in range(xline.shape[0]):
        pose_ = xline[pose]

        x_list=[]
        for i in range(pose_.shape[0]):
            x_start = pose_[i,1,0]
            x_end = pose_[i, 1, 1]
            x_list.append(x_start)
            x_list.append(x_end)
            x_list.append(None)

        all_x[pose] = x_list
        
    return all_x

def make_dream_z(xline):
    all_x = np.zeros((xline.shape[0], 22*3))

    for pose in range(xline.shape[0]):
        pose_ = xline[pose]

        x_list=[]
        for i in range(pose_.shape[0]):
            x_start = pose_[i,2,0]
            x_end = pose_[i, 2, 1]
            x_list.append(x_start)
            x_list.append(x_end)
            x_list.append(None)

        all_x[pose] = x_list
        
    return all_x

def make_dreams(seq_data, which_seq):
    dance_to_plot = seq_data[which_seq]
    xline = get_line_segments(dance_to_plot)
    dream_x = make_dream_x(xline)
    dream_y = make_dream_y(xline)
    dream_z = make_dream_z(xline)

    return dream_x, dream_y, dream_z
