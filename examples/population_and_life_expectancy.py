# %% [markdown]
# # Collect the data

# %%
import world_bank_data as wb

# Collect countries
countries = wb.get_countries()
region_country = countries[['region', 'name']].rename(columns={'name': 'country'})

# Population & life expectancy
region_country['population'] = wb.get_series('SP.POP.TOTL', mrv=1, id_or_value='id', simplify_index=True)
region_country['life_expectancy'] = wb.get_series('SP.DYN.LE00.IN', mrv=1, id_or_value='id', simplify_index=True)

# Observations restricted to the countries
pop_and_exp = region_country.loc[countries.region != 'Aggregates'].set_index(['region', 'country']).sort_index()
pop_and_exp

# %% [markdown]
# # Data aggregation

# %%
import numpy as np


def average(values, weights):
    """Same as np.average, but remove nans"""
    total_obs = 0.
    total_weight = 0.
    if isinstance(values, np.float):
        values = [values]
        weights = [weights]
    for x, w in zip(values, weights):
        xw = x * w
        if np.isnan(xw):
            continue
        total_obs += xw
        total_weight += w
    return total_obs / total_weight if total_weight != 0 else np.NaN


def life_expectancy(item):
    """Life expectancy associated to a tuple like (), ('Europe & Central Asia') or ('East Asia & Pacific', 'China')"""
    sub = pop_and_exp.loc[item] if item else pop_and_exp
    return average(sub.life_expectancy, weights=sub.population)


def text(item):
    """Return the text associated to a tuple like (), ('Europe & Central Asia') or ('East Asia & Pacific', 'China')"""
    life_exp = life_expectancy(item)
    if life_exp > 0:
        pop = pop_and_exp.population.loc[item].sum() if item else pop_and_exp.population.sum()  
        return 'Population: {:,}<br>Life expectancy: {:.2f}'.format(int(pop), life_exp)


# %% [markdown]
# # Plot

# %%
import plotly.graph_objects as go
import easyplotly as ep

treemap = ep.Treemap(pop_and_exp.population,
                     hoverinfo='label+text',
                     text=text,
                     root_label='World',
                     # magic underscore notation
                     marker_colors=life_expectancy,
                     marker_colorscale='RdBu')

layout = go.Layout(title='World Population and Life Expectancy<br>Data from the World Bank', height=600)

go.Figure(treemap, layout)

# %%
