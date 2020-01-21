# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.3.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# This is a very short notebook:
# we collect the world population and plot it.

# %%
import world_bank_data as wb
import plotly.express as px

pop = wb.get_series('SP.POP.TOTL', country='WLD', simplify_index=True)
px.area(pop.rename('Population').reset_index(), x='Year', y='Population', title='World Population')

