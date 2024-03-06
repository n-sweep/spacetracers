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
# import plotly.express as px
# import plotly.graph_objs as go
import plotly.io as pio
import pandas as pd
import requests

# plotly setup
pio.renderers.default = 'notebook'
pd.options.plotting.backend = 'plotly'


def pwrite(fig, plt='/tmp/vis/plot.json'):
    fig = fig.update_layout(autosize=False)
    fig.write_json(plt)


def ensure_directory(dir):
    """ ensure the directory exists """
    if os.path.isfile(dir):
        dir = os.path.dirname(dir)
    if not os.path.exists(dir):
        os.makedirs(dir)


# %% [markdown]
# # SpaceTraders

# %%
callsign = 'API_T3ST'
faction = 'COSMIC'
base_url = 'https://api.spacetraders.io/v2'
token_fp = os.path.expanduser('~/.config/st/tokens')
ensure_directory(token_fp)

# %%
# registering a new agent
res = requests.post(
    os.path.join(base_url, 'register'),
    headers={'Content-Type': 'application/json'},
    data={
        'symbol': callsign,
        'faction': faction
    }
)
if res.ok:
    data = res.json()['data']
    with open(os.path.join(token_fp, callsign), 'w+') as f:
        f.write(data['token'])

# %%
# reading token by agent callsign
with open(os.path.join(token_fp, callsign), 'r') as f:
    token = f.read()

# %%
# get agent
res = requests.get(
    os.path.join(base_url, 'my/agent'),
    headers={'Authorization': f'Bearer {token}'}
)
res

# %%
agent = res.json()['data']
agent

# %%
hq = agent['headquarters']
hq_split = hq.split('-')
hq_sector = hq_split[0]
hq_system = '-'.join(hq_split[:2])

# %%
# view your starting location
res = requests.get(
    os.path.join(base_url, 'systems', hq_system, 'waypoints', hq),
    headers={'Content-Type': 'application/json'},
)
res

# %%
res.json()

# %%
# view contracts
res = requests.get(
    os.path.join(base_url, 'my/contracts'),
    headers={'Authorization': f'Bearer {token}'}
)
contracts = res.json()['data']
contracts

# %%
# accept a contract
contract = contracts[0]
res = requests.post(
    os.path.join(base_url, 'my/contracts', contract['id'], 'accept'),
    headers={'Authorization': f'Bearer {token}'}
)
res

# %%
res.json()

# %%
# find a shipyard
res = requests.get(
    os.path.join(base_url, 'systems', hq_system, 'waypoints'),
    params={'traits': 'SHIPYARD'},
    headers={'Authorization': f'Bearer {token}'}
)
res

# %%
shipyards = res.json()['data']

# %%
# view available ships
res = requests.get(
    os.path.join(
        base_url,
        'systems',
        hq_system,
        'waypoints',
        shipyards[1]['symbol'],
        'shipyard'
    ),
)
res.json()['data']

# %%
# purchase a ship
res = requests.post(
    os.path.join(base_url, 'my/ships'),
    headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    },
    json={
        'shipType': 'SHIP_MINING_DRONE',
        'waypointSymbol': shipyards[1]['symbol'],
    }
)
res

# %%
res.json()['data']

# %%
# find nearby asteroid
res = requests.get(
    os.path.join(base_url, 'systems', hq_system, 'waypoints'),
    params={'type': 'ENGINEERED_ASTEROID'},
    headers={'Authorization': f'Bearer {token}'}
)
res

# %%
asteroid = res.json()['data'][0]

# %%
# (view all ships)
res = requests.get(
    os.path.join(base_url, 'my/ships'),
    headers={'Authorization': f'Bearer {token}'},
)
res

# %%
ships = res.json()['data']
for ship in ships:
    print(ship['symbol'], ship['frame']['symbol'], ship['mounts'])

# %%
# fly to the asteroid

# orbit the ship at the current location
res = requests.post(
    os.path.join(base_url, 'my/ships', ships[2]['symbol'], 'orbit'),
    headers={'Authorization': f'Bearer {token}'},
)
res.json()['data']

# %%
# navigate to the asteroid
res = requests.post(
    os.path.join(base_url, 'my/ships', ships[2]['symbol'], 'navigate'),
    headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    },
    json={'waypointSymbol': asteroid['symbol']},
)
res

# %%
res.json()['data']

# %%
# dock the ship
res = requests.post(
    os.path.join(base_url, 'my/ships', ships[2]['symbol'], 'dock'),
    headers={'Authorization': f'Bearer {token}'},
)
res

# %%
res.json()['data']

# %%
# refuel the ship
res = requests.post(
    os.path.join(base_url, 'my/ships', ships[2]['symbol'], 'refuel'),
    headers={'Authorization': f'Bearer {token}'},
)
res

# %%
res.json()['data']

# %%
# orbit ship again
res = requests.post(
    os.path.join(base_url, 'my/ships', ships[2]['symbol'], 'orbit'),
    headers={'Authorization': f'Bearer {token}'},
)
res.json()['data']

# %%
# extract ores & minerals
res = requests.post(
    os.path.join(base_url, 'my/ships', ships[2]['symbol'], 'extract'),
    headers={'Authorization': f'Bearer {token}'},
)
res.json()['data']

# %%
# view market data
res = requests.get(
    os.path.join(
        base_url,
        'systems',
        hq_system,
        'waypoints',
        asteroid['symbol'],
        'market'
    ),
    headers={'Authorization': f'Bearer {token}'}
)
res.json()['data']

# %%
# list ship cargo
res = requests.get(
    os.path.join(base_url, 'my/ships', ships[2]['symbol'], 'cargo'),
    headers={'Authorization': f'Bearer {token}'},
)
cargo = res.json()['data']
cargo

# %%
# sell goods

# dock the ship
res = requests.post(
    os.path.join(base_url, 'my/ships', ships[2]['symbol'], 'dock'),
    headers={'Authorization': f'Bearer {token}'},
)

# %%
# sell goods
res = requests.post(
    os.path.join(
        base_url,
        'my/ships',
        ships[2]['symbol'],
        'sell'
    ),
    headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    },
    json={
        'symbol': 'IRON_ORE',
        'units': 100
    }
)

# %%
# navigate to delivery waypoint
res = requests.get(
    os.path.join(base_url, 'my/ships', ships[2]['symbol'], 'navigate'),
    headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    },
    json={'waypointSymbol': contracts[0]['deliver'][0]['destinationSymbol']},
)
res.json()['data']

# %%
# deliver contract goods
res = requests.post(
    os.path.join(
        base_url,
        'my/contracts',
        contracts[0]['id'],
        'deliver'
    ),
    headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    },
    json={
        'shipSymbol': ships[2]['symbol'],
        'tradeSymbol': contracts[0]['deliver'][0]['tradeSymbol'],
    },
)
res.json()['data']

# %%
# fulfill contract
res = requests.post(
    os.path.join(
        base_url,
        'my/contracts',
        contracts[0]['id'],
        'fulfill'
    ),
    headers={'Authorization': f'Bearer {token}'}
)

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
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
