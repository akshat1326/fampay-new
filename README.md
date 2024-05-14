# YouTube Trending API


## Contents
- [Getting Started](#getting-started)
- [Running locally](#running-locally)
  - [Using Docker](#using-docker)
- [API endpoints](#api-endpoints)
    - [1. /videos](#1-videos)
    - [2. /search](#2-search)

## Getting Started
Start by cloning the repository using: `git clone https://github.com/akshat1326/fampay-new.git` followed by `cd fampay-new`.
## Running locally
#### NOTE: Multiple Google API keys can be specified to avoid quota exceed errors. To do this, specify them in config/api_keys.py
### Using Docker
Use `docker-compose` to test the app locally. 
```bash
docker-compose up
```
Run localhost:8080 to check the dashboard

<img width="1470" alt="Screenshot 2024-03-30 at 5 00 02 PM" src="https://github.com/akshat1326/fampay-new/assets/63421485/cad797c8-d9ce-43c0-bffb-a4f4ef1bcd94">


<img width="1470" alt="Screenshot 2024-03-30 at 5 00 11 PM" src="https://github.com/akshat1326/fampay-new/assets/63421485/8b5f771c-02c0-400d-b752-f389bde72009">



## API endpoints
#### 1. `/videos`
```
URL: /videos?page={}&per_page={}
Request type: GET
Data parameters: page
Data parameters: per_page
```

NOTE: The `page` parameter is optional and defaults to page 1.

#### 2. `/search`
```
URL: /search?query={}&page={}&per_page={}
Request type: GET
Data parameters: query
Data parameters: page
Data parameters: per_page
```
