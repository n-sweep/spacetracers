# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: hydrogen
#       format_version: '1.3'
#       jupytext_version: 1.16.0
#   kernelspec:
#     display_name: Python3
#     language: python
#     name: Python3
# ---

# %%
import os
import plotly.io as pio
import pandas as pd
from api import ST

# plotly setup
pio.renderers.default = 'notebook'
pd.options.plotting.backend = 'plotly'


def pwrite(fig, plt='/tmp/vis/plot.json'):
    fig = fig.update_layout(autosize=False)
    fig.write_json(plt)


# %% [markdown]
# # SpaceTraders API Testing

# %%
api = ST(token_fp=os.path.expanduser('~/.config/st/tokens'))
api.request()

# %%
r = api.register('API_T3ST', 'COSMIC')
r.content

# %%
r = api.get_agent('API_T3ST')
r.content

# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
