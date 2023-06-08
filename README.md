# OneDrive API

---

### Summary:

```
This API provides file download operation from OneDrive.
```

### Pre-Requirements:

```
Register an app on portal.azure.com (from the Azure AD menu)

Set callback url (http://localhost:8000/onedrive/callback)

Add permissions [User.Read, Files.Read.All, offline_access]

Get your client_id and client_secret keys and write to env file
```

### Requirements:

```
docker
docker-compose
```

### How to Run:

```
cp config/.env.example config/.env
docker-compose up --build -d
```

### Docs:

```
localhost:8000/docs
```

### Endpoints:

```http request
GET  /onedrive/auth/{user_id}        # onedrive auth
GET  /onedrive/callback              # callback url
GET  /onedrive/account/{user_id}     # get account info
GET  /onedrive/list/{user_id}        # get file list
GET  /onedrive/download/{user_id}    # download all files

GET  /                               # health check
```

---
