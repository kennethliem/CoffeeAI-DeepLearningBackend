# CoffeeAI - Discover and savor your coffee with ease.

![image](https://user-images.githubusercontent.com/69246482/224530445-6aff5c5b-b5cd-469d-92b8-2bfd4fceda35.png)

## App Description

Our coffee bean detection website is a platform designed to assist coffee enthusiasts in identifying different types of coffee beans. Our team has worked tirelessly to create a website that is both informative and user-friendly. We understand the importance of knowing the exact type of coffee beans used in coffee-making, and have made it our mission to provide accurate and detailed information about each type of coffee bean. Through our website, users can learn about the origins, taste profiles for each type of coffee bean.

### Note

<b>For now, this application can only be used for: </b>

- Arabica Gayo
- Robusta Gayo

<b>In the future we will update so that it can be used for other coffee beans type.</b>

### Homepage Screenshots

![AppScreenshots](https://user-images.githubusercontent.com/69246482/224529673-b68d91b4-c21b-4674-b109-7884e7445f8a.png)

### Admin Dashboard Screenshots

![AdminScreenshot](https://github.com/kennethliem/CoffeeAI/assets/69246482/8f2807db-0fb8-41c9-b7c9-f2f8222fa93f)

## Endpoint List

### Check Engine Status

- Endpoint : `/api/check/`
- HTTP Method : `GET`

- Request Body :

```json
{
  "key": "secretKey"
}
```

- Respone Body (Success):

```json
{
  "error": false,
  "message": "Engine Ready",
  "status": "Online"
}
```

### Disable Engine

- Endpoint : `/api/check/disable`
- HTTP Method : `POST`

- Request Body :

```json
{
  "key": "secretKey"
}
```

- Respone Body (Success):

```json
{
  "error": false,
  "message": "Engine turned off",
  "status": null
}
```

### Enable Engine

- Endpoint : `/api/check/enable`
- HTTP Method : `POST`

- Request Body :

```json
{
  "key": "secretKey"
}
```

- Respone Body (Success):

```json
{
  "error": false,
  "message": "Engine turned on",
  "status": null
}
```

### Detection

- Endpoint : `/api/detection`
- HTTP Method : `POST`

- Request Body :

  - `image` as `file`

- Respone Body (Success):

```json
{
  "coffeeType": "Robusta Gayo",
  "error": false,
  "message": "Success"
}
```

- Respone Body (Fail):

```json
{
  "coffeeType": null,
  "error": true,
  "message": "Can't get Image"
}
```

or

```json
{
  "coffeeType": null,
  "error": true,
  "message": "Not Detected"
}
```

### Retrain

- Endpoint : `/api/retrain`
- HTTP Method : `POST`

- Request Body :

  - `dataset` as `file`

- Respone Body (Success):

```json
{
  "error": false,
  "message": "Retrain requested successfuly"
}
```

- Respone Body (Fail):

```json
{
  "error": true,
  "message": "Can't get Datasets file"
}
```
