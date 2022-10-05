from copy import deepcopy
import pandas as pd
import numpy as np


def project_hemis_surf(surf, hemis="left"):
    """Keep brain surfaces of one hemisphere."""

    surf_hemis = deepcopy(surf)

    if hemis == "right":
        idx = np.where(surf.coordinates[:, 0] >= 0)[0]
    elif hemis == "left":
        idx = np.where(surf.coordinates[:, 0] <= 0)[0]
    idx_faces = [i for i, f in enumerate(surf.faces) if set(f).issubset(idx)]
    # We need to map the coordinates into new indexes values
    faces_hemis = surf.faces[idx_faces]
    mapper = {e: i for i, e in enumerate(idx)}

    surf_hemis = surf_hemis._replace(
        coordinates=surf.coordinates[idx], faces=np.vectorize(mapper.get)(faces_hemis)
    )

    return surf_hemis


def project_hemis_chans(points, hemis="left"):
    """Project MNI coordinates on one hemisphere."""

    if hemis == "right":
        sign = 1
    elif hemis == "left":
        sign = -1

    points[:, 0] = sign * np.abs(points[:, 0])

    return points


def get_MNI_params(
    df_mni: pd.DataFrame, df_params: pd.DataFrame, param_names: list
) -> pd.DataFrame:
    """Get parameter of interest and MNI coordinates from each electrode.

    Args:
        df_mni (pd.DataFrame): dataframe with MNI coordinates (x,y,z) and channel as columns, patient code as index.
        df_params (pd.DataFrame): dataframe with param_names and channel as columns, patient code as index.
        param_names (list): list of parameters names of interest.

    Returns:
        pd.DataFrame: merged dataframe with MNI coordinates and parameters.
    """

    # Store results in new Dataframe
    df_mni_params = []

    # Check param_names is a ctually a list
    if not isinstance(param_names, list):
        param_names = [param_names]

    # Loop through each subject to intersect the channels
    for pat in df_mni.index.unique():

        df_mni_pat = df_mni[df_mni.index == pat]
        df_params_pat = df_params[df_params.index == pat]
        chans_both = np.intersect1d(df_mni_pat.chan, df_params_pat.chan)
        df_mni_pat = df_mni_pat[df_mni_pat.chan.isin(chans_both)]
        df_params_pat = df_params_pat[df_params_pat.chan.isin(chans_both)]

        df_params_pat_sort = df_params_pat.set_index("chan", drop=False)
        df_params_pat_sort = df_params_pat_sort.loc[df_mni_pat.chan.to_list()]
        df_params_pat_sort.index = [pat] * len(df_params_pat_sort)

        df = pd.DataFrame(
            data=None,
            index=df_params_pat_sort.index,
            columns=["chan", "region", "mni_x", "mni_y", "mni_z"] + param_names,
        )
        df.loc[:, "chan"] = df_mni_pat["chan"].to_list()
        df.loc[:, "region"] = df_mni_pat["region"].to_list()
        df.loc[:, "mni_x"] = df_mni_pat["mni_x"].to_list()
        df.loc[:, "mni_y"] = df_mni_pat["mni_y"].to_list()
        df.loc[:, "mni_z"] = df_mni_pat["mni_z"].to_list()
        df.loc[:, param_names] = df_params_pat_sort.loc[:, param_names].copy()
        df_mni_params.append(df)

    # Concatenate data from all patients
    df_mni_params = pd.concat(df_mni_params)

    return df_mni_params


def get_resp_params(
    df_resp: pd.DataFrame, df_params: pd.DataFrame, param_names: list
) -> pd.DataFrame:
    """Get parameter of interest and response latencies from each electrode.

    Args:
        df_resp (pd.DataFrame): dataframe with latencies and channel as columns, patient code as index.
        df_params (pd.DataFrame): dataframe with param_names and channel as columns, patient code as index.
        param_names (list): list of parameters names of interest.

    Returns:
        pd.DataFrame: merged dataframe with response latencies and parameters.
    """

    # Store results in new Dataframe
    df_resp_params = []

    # Check param_names is a ctually a list
    if not isinstance(param_names, list):
        param_names = [param_names]

    # Loop through each subject to intersect the channels
    for pat in df_resp.index.unique():

        df_resp_pat = df_resp[df_resp.index == pat]
        df_params_pat = df_params[df_params.index == pat]
        chans_both = np.intersect1d(df_resp_pat.chan, df_params_pat.chan)
        df_resp_pat = df_resp_pat[df_resp_pat.chan.isin(chans_both)]
        df_params_pat = df_params_pat[df_params_pat.chan.isin(chans_both)]

        df_params_pat_sort = df_params_pat.set_index("chan", drop=False)
        df_params_pat_sort = df_params_pat_sort.loc[df_resp_pat.chan.to_list()]
        df_params_pat_sort.index = [pat] * len(df_params_pat_sort)

        df = pd.DataFrame(
            data=None,
            index=df_params_pat_sort.index,
            columns=["chan", "region", "onset", "peak"] + param_names,
        )
        df.loc[:, "chan"] = df_resp_pat["chan"].to_list()
        df.loc[:, "region"] = df_resp_pat["region"].to_list()
        df.loc[:, "onset"] = df_resp_pat["onset"].to_list()
        df.loc[:, "peak"] = df_resp_pat["peak"].to_list()
        df.loc[:, param_names] = df_params_pat_sort.loc[:, param_names].copy()
        df_resp_params.append(df)

    # Concatenate data from all patients
    df_resp_params = pd.concat(df_resp_params)

    return df_resp_params


def compute_sig_blocks(pvals, alpha):
    """Compute endpoints of blocks of significance."""

    points_sign_bool = np.where(pvals < alpha, 1, 0)
    points_sign_step = np.where(np.diff(points_sign_bool) != 0)[0] + 1
    points_sign_periods = np.split(points_sign_bool, points_sign_step)
    points_sign_step = np.insert(
        points_sign_step, 0, 0
    )  # to allow same number of elements of points_sign_periods
    points_sign_blocks = []
    for i, p in enumerate(points_sign_periods):
        if p[0] == 1:
            points_sign_blocks.append(
                [points_sign_step[i], points_sign_step[i] + len(p) - 1]
            )

    return points_sign_blocks
