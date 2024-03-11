# Copernicus-API

![GitHub](https://img.shields.io/github/license/chmaikos/Copernicus-API) ![GitHub stars](https://img.shields.io/github/stars/chmaikos/Copernicus-API?style=social) ![Docker Automated build](https://img.shields.io/docker/automated/chmaikos/copernicus-api)

- [Copernicus-API](#copernicus-api)
  - [Introduction](#introduction)
  - [Features](#features)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Setup](#setup)
  - [Usage](#usage)
  - [Endpoints](#endpoints)
    - [Lab API](#lab-api)
    - [Copernicus API](#copernicus-api-1)
    - [AIS API](#ais-api)
    - [Vessel API](#vessel-api)
  - [Contributing](#contributing)
  - [License](#license)

## Introduction

Copernicus-API is a Python-based application designed to facilitate access to the Copernicus satellite data for various applications. This API decodes, processes, and serves satellite data, including AIS (Automatic Identification System) for maritime navigation, weather forecasting, and wave and wind data processing.

## Features

- **AIS Data Decoding**: Decode AIS data for real-time maritime navigation and tracking.
- **Weather Forecasting**: Utilize satellite data for detailed and accurate weather predictions.
- **Wave and Wind Data Processing**: Analyze wave and wind data for maritime safety, surfing, and environmental monitoring.

## Installation

### Prerequisites

- Docker
- Python 3.10 or higher

### Setup

1. Clone the repository:

   ```sh
   git clone https://github.com/chmaikos/Copernicus-API.git
   ```

2. Navigate to the project directory:

   ```sh
   cd Copernicus-API
   ```

3. Build and run the Docker container:

   ```sh
   docker-compose up --build
   ```

## Usage

Once the API is up and running, you can start making HTTP requests to the available endpoints:

## Endpoints

### Lab API

- **GET `/api/lab`** - Get Living Lab Data
  - **Parameters**:
    - `date_min` (string, required): Start date for data query
    - `date_max` (string, required): End date for data query
  - **Responses**:
    - `200` Successful Response
    - `422` Validation Error
- **POST `/api/lab`** - Add Data
  - **Responses**:
    - `200` Successful Response

### Copernicus API

- **GET `/api/data`** - Get Data
  - **Parameters**:
    - `latitude` (number, required): Latitude for data query
    - `longitude` (number, required): Longitude for data query
    - `radius` (number, required): Radius for data query
    - `dateMin` (string, required): Start date for data query
    - `dateMax` (string, required): End date for data query
  - **Responses**:
    - `200` Successful Response with `CombinedDataResponse` schema
    - `422` Validation Error

- **GET `/api/weather`** - Get Weather Data
  - **Responses**:
    - `200` Successful Response with `WeatherDataResponse` schema

### AIS API

- **GET `/api/ais_cyprus_dynamic`** - Get AIS Cyprus Dynamic
  - **Parameters**:
    - `date_min` (string, required): Start date for AIS data query
    - `date_max` (string, required): End date for AIS data query
  - **Responses**:
    - `200` Successful Response
    - `422` Validation Error

- **GET `/api/ais_cyprus_static`** - Get AIS Cyprus Static
  - **Parameters**:
    - `date_min` (string, required): Start date for AIS data query
    - `date_max` (string, required): End date for AIS data query
  - **Responses**:
    - `200` Successful Response
    - `422` Validation Error

### Vessel API

- **GET `/api/threats/`** - Get Cops
  - **Responses**:
    - `200` Successful Response with `COP` schema

- **GET `/api/threat-cops/`** - Get Cops For Threat
  - **Parameters**:
    - `id` (string, required): ID of the threat
  - **Responses**:
    - `200` Successful Response with `COP` schema
    - `422` Validation Error

- **PUT `/api/update-cops/`** - Update Steps
  - **Parameters**:
    - `id` (string, required): ID of the COP
  - **RequestBody**:
    - Required, with `COP` schema
  - **Responses**:
    - `200` Successful Response with `COP` schema
    - `422` Validation Error

- **GET `/api/rops/`** - Get Rops
  - **Parameters**:
    - `msg_id` (string, required): Message ID for ROP query
  - **Responses**:
    - `200` Successful Response with `Alert` schema
    - `422` Validation Error

- **PUT `/api/update-status-and-rops/`** - Update Rops
  - **Parameters**:
    - `msg_id` (string, required): Message ID for ROP update
  - **RequestBody**:
    - Required, with `Alert` schema
  - **Responses**:
    - `200` Successful Response with `Alert` schema
    - `422` Validation Error

## Contributing

We welcome contributions to the Copernicus-API project. Please read our [Contributing Guide](CONTRIBUTING.md) for more information on how to get started.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
