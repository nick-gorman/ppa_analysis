import pandas as pd
import numpy as np
import scenario_runner
from get_emissions_intensity import get_emissions_intensity

load_profiles = pd.read_csv('tests/data/sample_one_day_data.csv')
price_profiles = pd.read_csv('tests/data/sample_price_set.csv')
charge_set = pd.read_csv('tests/data/sample_charge_set.csv')
scenarios = pd.read_csv('tests/data/sample_scenarios.csv').fillna(np.nan).replace([np.nan], [None])
emissions = get_emissions_intensity(
    start=load_profiles['DateTime'].iloc[0], 
    end=load_profiles['DateTime'].iloc[-1],
    cache='cache_nemed/',
    regions=['QLD1', 'NSW1', 'SA1'],
    period='30min'
    )

scenarios['retail'], scenarios['ppa'] = \
    zip(*scenarios.apply(scenario_runner.run_scenario_from_row, axis=1, price_profiles=price_profiles,
                         load_profiles=load_profiles, charge_set=charge_set, emissions_profiles=emissions))
scenarios.to_csv('tests/data/costs_year.csv')