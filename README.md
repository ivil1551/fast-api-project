# FAST API Project

To access this FAST API project navigate to project path

    cd ./fast-api-project

### Create venv

    python -m venv venv

### Project Setup

    .venv/Scripts/activate
    python -m pip install --no-cache-dir -r requirements.txt

### To run FAST API

    uvicorn main:app --reload --port 8080

### To access FAST API + SWAGGER UI

Enter the below http url in browser

    http://localhost:8080/docs#/

Note**: 
        
        Create tweet and Delete tweet endpoints are secured with JWT
        
        To authorize select authorize in fast api swagger ui and enter JWT token obtained 
        from get user token API call.

# API DOCS

### Create User

###### Request Body

```json
{
  "user_name": "string"
}
```

###### Response

```json
{
  "user_id": 5,
  "created_timestamp": 1651924114.8320706
}
```

### Get JWT token

###### Query Parameter

    user_name="string"

###### Response

```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX25hbWUiOiJ0ZXN0dXNlcjciLCJ1c2VyX2lkIjo1LCJleHBpcmF0aW9uX3RpbWUiOjE2NTE5MjYwNzguOTY4NTUzNX0.ntxP9M4_cZAfAiaOfU5pub2wvmhs11Sdy_JECsPsPIE"
}
```

### Create Tweet

###### Request Body

```json
{
  "user_id": 0,
  "tweet": "string"
}
```

###### Response Body

```json
{
  "tweet_id": 2,
  "created_timestamp": 1651924804.1405776
}
```
### Read or Get tweet

###### Query Parameter

    ?user_name="string"&date="yyyy-mm-dd"

##### Response Body

```json
{
  "tweets_count": 1,
  "tweets_list": [
    {
      "tweet_id": 2,
      "tweet": "test_tweet_3",
      "created_timestamp": 1651924804
    }
  ]
}
```

### Delete Tweet

###### Request Body

```json
{
  "user_name": "string"
}
```
###### Response Body

```json
{
  "deleted_tweets_count": 1,
  "deleted_tweets_list": [
    {
      "tweet_id": 2,
      "tweet": "test_tweet_3"
    }
  ]
}
```