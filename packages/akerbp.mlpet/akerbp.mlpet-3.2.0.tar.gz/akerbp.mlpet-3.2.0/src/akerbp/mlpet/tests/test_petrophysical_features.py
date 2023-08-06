import os

import numpy as np
import pandas as pd
from cognite.experimental import CogniteClient

from akerbp.mlpet import feature_engineering, petrophysical_features
from akerbp.mlpet.dataloader import DataLoader


def test_guess_bs_from_cali():
    input = pd.DataFrame({"CALI": [6.1, 5.9, 12.0, 12.02]})
    df = petrophysical_features.guess_BS_from_CALI(input)
    assert "BS" in df.columns.tolist()


def test_calculate_cali_bs():
    input = pd.DataFrame({"CALI": np.array([6.1, 5.9, 12.0, 12.02])})
    df = petrophysical_features.calculate_CALI_BS(input)
    assert "CALI-BS" in df.columns.tolist()


def test_calculate_VSH():
    client = CogniteClient(
        client_name="mlpet-unittest",
        project="akbp-subsurface",
        api_key=os.environ[
            "COGNITE_API_KEY_FUNCTIONS"
        ],  # Assumes COGNITE_API_KEY_FUNCTIONS is set in the environment
    )
    dl = DataLoader()
    df = dl.load_from_cdf(
        client=client, metadata={"wellbore_name": "15/3-5", "subtype": "BEST"}
    )
    df["well_name"] = "15/3-5"
    df = petrophysical_features.calculate_LFI(df)
    df = feature_engineering.add_formations_and_groups(
        df, id_column="well_name", depth_column="DEPTH"
    )
    df = feature_engineering.add_vertical_depths(
        df, id_column="well_name", md_column="DEPTH"
    )
    df_out = petrophysical_features.calculate_VSH(
        df,
        id_column="well_name",
        env="prod",
        return_CI=True,
        client=client,
        keyword_arguments=dict(
            calculate_denneu=True,
            VSH_curves=["GR", "LFI"],
            groups_column_name="GROUP",
            formations_column_name="FORMATION",
            return_only_vsh_aut=False,
            nan_numerical_value=-9999,
            nan_textual_value="MISSING",
        ),
    )
    assert "VSH" in df_out.columns.tolist()
