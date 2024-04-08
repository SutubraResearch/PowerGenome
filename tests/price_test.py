"Test functions from financials.py"

import numpy as np
import pandas as pd
import pytest

from powergenome.eia_opendata import load_aeo_series
from powergenome.financials import (
    inflation_price_adjustment,
    investment_cost_calculator,
    load_cpi_data,
)
from powergenome.params import SETTINGS


def test_load_cpi(tmp_path):
    # Get data the first time
    cpi = load_cpi_data(data_path=tmp_path / "cpi_data.csv")

    # Get data saved to file
    cpi = load_cpi_data(data_path=tmp_path / "cpi_data.csv")

    assert all(cpi["value"].notna())
    assert all(cpi["period"] == 12)


def test_inflate_price(tmp_path):
    p = 10
    p2 = inflation_price_adjustment(p, 2000, 2010, data_path=tmp_path / "cpi_data.csv")
    assert p2 > p

    # remove later years from saved CPI file
    cpi = pd.read_csv(tmp_path / "cpi_data.csv")
    first_year = cpi["year"].min()
    last_year = cpi["year"].max()
    cpi.loc[5:10, :].to_csv(tmp_path / "cpi_data.csv", float_format="%g")

    p = pd.Series([1, 10])
    p2 = inflation_price_adjustment(p, first_year, last_year)
    assert all(p2 > p)


def test_aeo_series():
    series_id = "AEO.2022.REF2022.PRCE_REAL_ELEP_NA_NG_NA_NEENGL_Y13DLRPMMBTU.A"
    df = load_aeo_series(series_id)
    assert not df.empty


# Generated by CodiumAI


class TestInvestmentCostCalculator:
    # Tests that the function correctly calculates the investment cost with a single capex, wacc, and cap_rec_years
    def test_single_capex_wacc_cap_rec_years(self):
        capex = 1000
        wacc = 0.05
        cap_rec_years = 5
        expected_result = 230.97

        result = investment_cost_calculator(capex, wacc, cap_rec_years)

        assert result == pytest.approx(expected_result, abs=0.01)

    # Tests that the function correctly calculates the investment cost with list-like capex, wacc, and cap_rec_years
    def test_list_like_capex_wacc_cap_rec_years(self):
        capex = [1000, 2000, 3000]
        wacc = [0.05, 0.06, 0.07]
        cap_rec_years = [5, 10, 15]
        expected_result = [230.97, 271.73, 329.38]

        result = investment_cost_calculator(capex, wacc, cap_rec_years)

        assert result == pytest.approx(expected_result, abs=0.01)

    # Tests that the function raises a TypeError when a single capex and wacc are provided, but list-like cap_rec_years
    def test_single_capex_wacc_list_like_cap_rec_years(self):
        capex = 1000
        wacc = 0.05
        cap_rec_years = [5, 10, 15]

        with pytest.raises(TypeError):
            investment_cost_calculator(capex, wacc, cap_rec_years)

    # Tests that the function correctly calculates the investment cost with list-like capex and cap_rec_years, but a single wacc
    def test_list_like_capex_cap_rec_years_single_wacc(self):
        capex = [1000, 2000, 3000]
        wacc = 0.05
        cap_rec_years = [5, 10, 15]
        expected_result = [230.97, 259.01, 289.03]

        result = investment_cost_calculator(capex, wacc, cap_rec_years)

        assert result == pytest.approx(expected_result, abs=0.01)

    # Tests that the function correctly calculates the investment cost with list-like capex and wacc, but a single cap_rec_years
    def test_list_like_capex_wacc_single_cap_rec_years(self):
        capex = [1000, 2000, 3000]
        wacc = [0.05, 0.06, 0.07]
        cap_rec_years = 5
        expected_result = [230.97, 474.79, 731.67]

        result = investment_cost_calculator(capex, wacc, cap_rec_years)

        assert result == pytest.approx(expected_result, abs=0.01)

    # Tests that the function correctly calculates the investment cost with list-like capex, wacc, and cap_rec_years using continuous compounding
    def test_list_like_capex_wacc_cap_rec_years_continuous_compounding(self):
        capex = [1000, 2000, 3000]
        wacc = [0.05, 0.06, 0.07]
        cap_rec_years = [5, 10, 15]
        compound_method = "continuous"
        expected_result = [231.79, 274.11, 334.62]

        result = investment_cost_calculator(capex, wacc, cap_rec_years, compound_method)

        assert result == pytest.approx(expected_result, abs=0.01)

    # Tests that a ValueError is raised when the compound_method argument is set to "neither"
    def test_invalid_compound_method(self):
        capex = [1000, 2000, 3000]
        wacc = [0.05, 0.06, 0.07]
        cap_rec_years = [5, 10, 15]
        compound_method = "neither"

        with pytest.raises(ValueError):
            investment_cost_calculator(capex, wacc, cap_rec_years, compound_method)

    # Tests that a ValueError is raised when one of the capex values is nan
    def test_nan_capex_value(self):
        capex = [1000, np.nan, 2000]
        wacc = 0.05
        cap_rec_years = 5

        with pytest.raises(ValueError):
            investment_cost_calculator(capex, wacc, cap_rec_years)

    # Tests that the function correctly calculates the investment cost with list-like capex, wacc, and cap_rec_years as pandas Series
    def test_list_like_capex_wacc_cap_rec_years_as_pandas_series(self):
        capex = pd.Series([1000, 2000, 3000])
        wacc = pd.Series([0.05, 0.06, 0.07])
        cap_rec_years = pd.Series([5, 10, 15])
        expected_result = np.array([230.97, 271.73, 329.38])

        result = investment_cost_calculator(capex, wacc, cap_rec_years)

        assert result == pytest.approx(expected_result, abs=0.01)
