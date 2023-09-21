# API
---

### DEMO

#### Request

`GET http://127.0.0.1:5000/api/alert-types`

#### Response

```json
[
    {
        "_id": {
            "$oid": "650c7e0181f1be12cc093f54"
        },
        "alert_type_id": 1,
        "description": "Suspicious activity"
    },
    {
        "_id": {
            "$oid": "650c7e0181f1be12cc093f55"
        },
        "alert_type_id": 2,
        "description": "Unusual deviation from normalcy"
    }
]
```

#### Request

`GET http://127.0.0.1:5000/api/op-steps/?alert_type_id=2`

#### Response

```json
[
    {
        "_id": {
            "$oid": "650c7e0181f1be12cc093f55"
        },
        "alert_type_id": 2,
        "description": "Unusual deviation from normalcy",
        "steps": [
            {
                "no": 1,
                "description": "Call the vessel"
            },
            {
                "no": 2,
                "description": "Inform the responsible authority"
            },
            {
                "no": 3,
                "description": "Hello"
            }
        ]
    }
]
```


#### Request

`PUT 127.0.0.1:5000/api/update-steps/?alert_type_id=2`

#### Response

```json
{
    "success": true
}
```

#### Request

`GET http://127.0.0.1:5000/api/alert-steps/?alert_id=1`

#### Response

```json
[
    {
        "_id": {
            "$oid": "650c7e0181f1be12cc093f57"
        },
        "alert_id": 1,
        "alert_type_id": 1,
        "steps": [
            {
                "no": 1,
                "description": "Call the vessel",
                "status": "Not initialized"
            },
            {
                "no": 2,
                "description": "Inform the responsible authority",
                "status": "Not initialized"
            }
        ]
    }
]
```

#### Request

`GET http://127.0.0.1:5000/api/rec-steps/?alert_id=1`

#### Response

```json
[
    {
        "_id": {
            "$oid": "650c7e0181f1be12cc093f56"
        },
        "alert_id": 1,
        "alert_type_id": 1,
        "description": "Suspicious/Unusual deviation from normalcy",
        "rec_steps": [
            {
                "no": 1,
                "description": "Call the vessel"
            },
            {
                "no": 2,
                "description": "Inform the responsible authority"
            }
        ]
    }
]
```
