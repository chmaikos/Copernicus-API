# CoperDBAPI

![CoperDBAPI](https://github.com/ArtemisStefanidou/APIs/blob/main/photos/Screenshot%202023-07-24%20at%203.33.34%20PM.png)

- [CoperDBAPI](#coperdbapi)
    - [Example Usage](#example-usage)
    - [ProducerWave](#producerwave)
    - [ProducerWind](#producerwind)
    - [API](#api)
      - [Request](#request)
      - [Response](#response)

---

### Example Usage

In the same folder with docker-compose.yml

```sh
docker-compose up --build
```

To ensure there are no orphan containers, you can use

```sh
docker-compose up --build --remove-orphans
```

![Sublime's custom image](https://github.com/ArtemisStefanidou/APIs/blob/main/photos/Screenshot%202023-07-24%20at%205.32.18%20PM.png)

### ProducerWave

The first time it will pull data from Copernicus is when the docker compose is first uploaded. After that, it will retrieve data every 3 hours. Duplicates do not exist because the time range for pulling data from Copernicus is: `current_time - 3 hours + 1 second`

Copernicus updates information every 3 hours starting at 00:00. If the program starts at 05:00 o'clock, that means that the first time it retrieves data is at: `5 - (5%3) = 2` --> 02:00 o'clock.

We obtain the information as a .nc file from Copernicus, refactor it into JSON, and push it into the Kafka topic `wave_topic` and into MongoDB in a collection named `waveData` with the following format:

```json
{
  "time": "Fri, 26 Jan 2024 01:00:00 GMT",
  "latitude": 35,
  "longitude": 18.916666666666657,
  "vhm0": 0.25999999046325684,
  "vmdr": 322.69000244140625,
  "vtm10": 3.4600000381469727
}
```

The information is analyzed below:

| Variable | Description                  | Unit |
|----------|------------------------------|------|
| vhm0     | Significant Wave Height      |meters|
| vmdr     | Wave Direction               |      |
| vtm10    | Wave Period Mean Value       |      |

![CoperDBAPI](https://github.com/ArtemisStefanidou/APIs/blob/main/photos/Screenshot%202023-07-25%20at%208.24.36%20AM.png)

The horizontal resolution is: `0.083° x 0.083°`

---

### ProducerWind

The first time it will pull data from Copernicus is when the docker compose is first uploaded. After that, it will retrieve data every day. The earliest data that we can get from Copernicus is from 6 days ago. The available time values are as follows:

```json
'time': [
  '00:00', '01:00', '02:00', '03:00', '04:00', '05:00',
  '06:00', '07:00', '08:00', '09:00', '10:00', '11:00',
  '12:00', '13:00', '14:00', '15:00', '16:00', '17:00',
  '18:00', '19:00', '20:00', '21:00', '22:00', '23:00',
]
```

We obtain the information as a .nc file from Copernicus, refactor it into JSON, and push it into the Kafka topic `wind_topic` and into MongoDB in a collection named `windData` with the following format:

```json
{
  "time": "Fri, 26 Jan 2024 01:00:00 GMT",
  "latitude": 50.150001525878906,
  "longitude": -27.1200008392334,
  "u10": -4.6063704822533245,
  "v10": -0.529921079222938,
  "speed": 4.636751596751709,
  "direction": 83.43748990096958
}
```
We add some extra features at the .nc file from Copernicus, refactor it into JSON, and push it into the Kafka topic `weather_topic` and into MongoDB in a collection named `weatherData` with the following format:

```json
    {
                "humidity": 96.38448804707079,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "pressure": 102227.77759296843,
                "sea_temp": 279.388671875,
                "temperature": 273.9269860137408,
                "time": "Wed, 31 Jan 2024 00:00:00 GMT",
                "total_cloud_cover": 59.96673923146837,
                "total_rain_water": -1.3552527156068805e-20,
                "total_snow_water": 0.0008333513378112866,
                "wind_direction": 359.40557106573124,
                "wind_speed": 5.3438242696397555
    }
```
The information is analyzed below:

| Variable           | Description                                                                                                         |  Unit  |
|--------------------|---------------------------------------------------------------------------------------------------------------------|--------|
| u10                | East Wind Component                                                                                                 |  m/s   |
| v10                | North Wind Component                                                                                                |  m/s   |
| direction / wind_direction | The Direction Of The Wind                                                                                   |   ˚    |
| speed / wind_speed | Combination of the above two components                                                                             |  m/s   |
| temperature        | The temperature of air at 2m above the surface of land, sea or in-land waters                                       |   K    |
| sea_temp           | The temperature of the sea                                                                                          |   K    |
| humidity           | A Combination of temperature, dewpoint temperature and pressure                                                     |   %    |
| sea_temp           | This parameter is the temperature of sea water near the surface                                                     |   K    |
| pressure           | Pressure                                                                                                            |   Pa   |
| total_cloud_cover  | This parameter is the proportion of a grid box covered by cloud                                                     |   %    |
| total_rain_water   | Water in droplets of raindrop size in a column extending from the surface of the Earth to the top of the atmosphere | kg/m^2 |
| total_snow_water   | Snow in a column extending from the surface of the Earth to the top of the atmosphere                               | kg/m^2 |

Speed information:

![CoperDBAPI](https://github.com/ArtemisStefanidou/APIs/blob/main/photos/Screenshot%202023-07-25%20at%208.25.32%20AM.png)

![CoperDBAPI](https://github.com/ArtemisStefanidou/APIs/blob/main/photos/Screenshot%202023-07-25%20at%208.25.44%20AM.png)

The horizontal resolution is: `0.25° x 0.25°`

---

### API

#### Request

`GET /data?dateMin=2023-07-19T04:00:00&dateMax=2023-07-19T07:00:00&latitude=35&longitude=18&radius=20`

Users must provide 5 variables: `dateMin`, `dateMax`, `latitude`, `longitude`, `radius`.

![CoperDBAPI](https://github.com/ArtemisStefanidou/APIs/blob/main/photos/Screenshot%202023-07-25%20at%2011.53.06%20AM.png)

#### Response

If the user provides a date older or newer than those in the collections, an empty list is returned.

When a valid date is provided, we check if data exists for the specified latitude and longitude. If data exists, information from both collections is returned.

```json
[
  {
    "waveData": [
      {
        "time": "Fri, 26 Jan 2024 01:00:00 GMT",
        "latitude": 35,
        "longitude": 18.916666666666657,
        "vhm0": 0.25999999046325684,
        "vmdr": 322.69000244140625,
        "vtm10": 3.4600000381469727
      },
      {...}
    ]
  },
  {
    "windData": [
      {
        "time": "Fri, 26 Jan 2024 01:00:00 GMT",
        "latitude": 35,
        "longitude": 18.916666666666657,
        "vhm0": 0.25999999046325684,
        "vmdr": 322.69000244140625,
        "vtm10": 3.4600000381469727
      },
      {...}
    ]
  }
]
```

If not, an empty list is returned.
