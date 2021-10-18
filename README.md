<h1 align="center"><a href="https://github.com/ajainuary/bolt-auction-challenge">
    <img src="https://user-images.githubusercontent.com/30972152/137773562-9c9ef85d-7b69-4f72-ba41-d448bf6e281a.jpg" alt="Logo" width="80" height="80">
  </a><br />Bolt Auction Challenge</h1>
  <p align="center">
    A Completely Asynchronous Auction Simulator
    <br />
    <a href="https://github.com/ajainuary/bolt-auction-challenge/blob/main/Bolt_Documentation_v1.1_02-04-21.pdf"><strong>Explore the docs »</strong></a>
    <br />
    ·
    <a href="https://github.com/ajainuary/bolt-auction-challenge/issues">Report Bug</a>
    ·
    <a href="https://github.com/ajainuary/bolt-auction-challenge/issues">Request Feature</a>
  </p>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#running-an-auction">Running an auction</li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

The Bolt Auction Challenge is a custom-designed fully asynchronous auction simulator that requires designing an interactive bot

### Built With

* [AIOHTTP](https://docs.aiohttp.org/en/stable/)


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

The simulator requires ```aiohttp``` package and ```Jinja2``` templating engine. In order to install the prerequisites, you can use the following command. The simulator has only been tested on Python 3.7.4

```sh
pip install -r requirements.txt
```

### Running an auction
The simulator consists of two parts, the central server and player clients. You must first start the central server by running ```bolt.py```. You can view all output at ```http://localhost:8080```

```sh
python bolt.py
```

Next, you must start the player clients that will initially register themselves with the server with a unique port number as the argument.

```sh
python player_client.py [Port Number]
```

Lastly, you need to run a script that orchestrates an auction.

```sh
python run_tournament.py [Number of Matches]
```

### Usage

#### Making a bot

A template for making your own bot is given in [my_bots/dummy.py](my_bots/dummy.py).

#### Configuring the client

In any copy of ```player_client_[n].py``` change the 3<sup>rd</sup> line to import your bot.

```python
from my_bots.team_<teamNo> import Team_<teamNo>_Bot
```

In the 7<sup>th</sup> line instantiate your bot.

```python
bot = Team_<teamNo>_Bot() #Your bot here
```

#### Running custom auctions

In order to run your own custom auction, you need to use [run_auction.py](run_auction.py). First, you need to specify which bots to run on line 11.

```python
players = ['Batman', 'Superman']  # Select the names of your bots here
```

Then, you can run the file as follows:

```sh
python run_auction.py <Duration> <Key>
```
Where ```<Key>``` is any random number.

#### Running multiple auctions

In order to run multiple auctions in the manner we would be running in the tournament, you need to use [run_tournament.py](run_tournament.py). First, you need to specify which bots to run on line 10.

```python
players = ['Batman', 'Superman']  # Select the names of your bots here
```

Then, you can run the file as follows:

```sh
python run_tournament.py <No_of_matches>
```

<!-- LICENSE -->
## License

Distributed under the MIT License. See [`LICENSE`](license.md) for more information.

## Acknowledgements

This project was built for the Introduction to Game Theory course at IIIT-H. I am grateful to the students for their feedback and patience.

## Changelog
### v1.1 25-04-21

- Various bugfixes
- Added a leaderboard view

### v0.1 19-03-21

- Auction works in logs
- Sample clients for bots added
