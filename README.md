# Gather
 Gather is a small utility for continuously aggregating internet facing data from any number of user defined endpoints in response to user defined triggers. All captured data is saved in a queryable format.

 #### Using Gather
 `gather.py [-h] -p PATTERN`

 Gather works on the premise of a pattern, a user defined template of sorts detailing what data to aggregate and from where, which triggers to aggregate in response to and where to save the results. Gather patterns are simple JSON files, taking an appearance similar to:

 ```javascript
 {
    "save": {},
    "triggers": [],
    "aggregate": []
}
 ```

 ##### Save
 The save section of a pattern describes where aggregated data should be saved. A database `type` and a `connection` property must be specified. At the moment, Postgres is the only supported database. A save block looks something like the following:

 ```javascript
 "save": {
    "type": "postgres",
    "connection": {
        "host": "localhost",
        "user": "your_user_name",
        "password": "your_password",
        "database": "your_db_name",
        "port": 5432 // Optional
    }
}
 ```

##### Triggers
Triggers define when and in response to what events data should be aggregated. Currently, only `timer`'s are supported as triggers. The `triggers` property should be an array of objects defining a trigger `type` and any properties of said trigger.

 ```javascript
 "triggers": [
    {
        "type": "timer",
        "every": 60 // Every 60 seconds
    }
]
```

#### Aggregates
Aggregates define what data is saved. Currently, all aggregated data must be provided in JSON format. Every aggregate must have a defined `type`, `key` and `url`.

**type**
- `index`: Aggregate a directory listing of sorts, can have sub-aggregates. A sort of for-loop for dynamic aggregation.
- `property`: Aggregate a single (or multiple) properties from a JSON object.

**key**
All aggregates must define a key path to aggregate on. Keys follow standard Javascript object-dot notation, but additionally support wildcards. For example, if an endpoint returned the following JSON:

```javacript
{
    "a": {
        "b": { "e": 1 },
        "c": { "e": 2 },
        "d": { "e": 3 }
    }
}
```

The following key paths are all valid:

`a.*.e`: Returns the value of all `e`'s: `[1, 2, 3]`
`a.*.*`: Returns the value of any property of any property under `a` (still all `e`'s): `[1, 2, 3]`
`*`: Returns all keys at the root: 'a' (useful for `index` aggregations`

**url**
An endpoint url, must include the protocol and must return JSON.

**Special Fields**

`index` aggregations support (and require) their own `aggregate` property. This `aggregate` property must be an array of sub-aggregates, in the same fashion as the main `aggregate` array described above.

`property` aggregations require the property `field`, to be set. `field` accepts a JSON key path in the same manner described above but the aggregated key path is uses in naming a database field for the aggregations results.

`property` aggregations support formatted URL's, using the standard Python string interpolation placeholder `{}`. This may be used during when a `property` is the sub-aggregate of an `index` aggregation. The value of the `index` aggregation will be available to the `url` property.

**Example**

```javascript
"aggregate": [
    {
        "url": "https://example.com/fruits",
        "type": "index",
        "key": "*",
        "aggregate": [
            {
                "url": "https://example.com/fruit/{}",
                "type": "property",
                "keys": [
                    "color",
                    "price.usd",
                    "price.eur"
                ],
                "field": "name"
            }
        ]
    }
]
```
