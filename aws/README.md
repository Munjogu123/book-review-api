# 📘 AWS Infrastructure with Terraform

This directory (aws/) contains Terraform configurations used to build and manage the AWS infrastructure for the Book Review API project.
The goal is to automate deployment of a secure, two-tier architecture consisting of a web server (Nginx) and a database server (PostgreSQL) using infrastructure as code (IaC).

## Architecture Overview

                           ┌──────────────────────────┐
                           │        Internet          │
                           └────────────┬─────────────┘
                                        │
                           ┌────────────▼─────────────┐
                           │   Internet Gateway (IGW) │
                           └────────────┬─────────────┘
                                        │
                           ┌────────────▼─────────────┐
                           │      Public Subnet       │
                           │  Web Server (Nginx EC2)  │
                           │  SG: HTTP, HTTPS, SSH    │
                           └────────────┬─────────────┘
                                        │
                           ┌────────────▼─────────────┐
                           │       NAT Gateway        │
                           └────────────┬─────────────┘
                                        │
                           ┌────────────▼─────────────┐
                           │      Private Subnet      │
                           │ DB Server (PostgreSQL)   │
                           │ SG: Postgres, SSH        │
                           └──────────────────────────┘

- VPC — Provides a private network for all resources.
- Public subnet — Hosts the web server (Nginx).
- Private subnet — Hosts the database server (PostgreSQL).
- NAT Gateway — Allows outbound internet access from the private subnet.
- Internet Gateway (IGW) — Enables external access to public subnet instances.
- Security Groups — Control inbound/outbound traffic for both servers.
- EC2 Instances — One running Nginx (webserver), one running PostgreSQL (dbserver).

## Prerequisites

Before you begin, ensure you have the following installed on your local machine:

1. Terraform (version 1.9.0 or later)
2. AWS CLI (configured with your AWS credentials)

## Deployment Steps

### 1. Initialize Terraform

```bash
cd aws
terraform init
```

### 2. Validate Configuration

```bash
terraform validate
```

### 3. Plan the Infrastructure

```bash
terraform plan -out=tfplan
```

### 4. Apply the Plan

```bash
terraform apply tfplan
```

## 💻 Web Server Setup

Script: `webserver.sh`

Executed automatically on the EC2 instance upon launch.

The script:

- Installs Nginx
- Starts and enables it on boot
- Accessible over HTTP (port 80) and HTTPS (port 443)

## 🗄️ Database Server Setup

Script: `dbserver.sh`

Executed automatically on the private EC2 instance.

The script:

- Installs PostgreSQL
- Configures it to start on boot
- Accessible only from the webserver security group on port 5432

## Accessing the EC2 instances

Using the keyfile stated in the main.tf file, open your terminal and execute the following command:

```bash
ssh-add fredssh.pem
ssh -A ubuntu@<your-public-ip>
```

To access the private EC2 instance, you will have to ssh into the public instance first as done above. Then write the following command in the public instance:

```bash
ssh ubuntu@<your-private-ip>
```

## Configuring the Database Server

Inside the private instance, we will configure two files:

- postgresql.conf
- pg_hba.conf

Let's start with the `postgresql.conf` file

```bash
sudo vi /etc/postgresql/16/main/postgresql.conf
```

This will open the configuration file. Find and change the following line:

```
listen_addresses = '*'
```

We will then add a few lines at the bottom of our `pg_hba.conf` file

```bash
sudo vi /etc/postgresql/16/main/pg_hba.conf
```

Add the following line to allow connection from our webserver:

```
host    all             all             10.0.0.0/24            md5
```

After these changes, we need to restart our postgres

```bash
sudo systemctl restart postgresql
```


## Configuring the Web Server

Exit out of the private server back to our web server to configure nginx as a reverse proxy.

### 1. Unlink the default file created by nginx on startup

```bash
sudo unlink /etc/nginx/sites-enabled/default
```

### 2. Create a new file with our configs for the fastapi app

```bash
sudo vi /etc/nginx/sites-available/fastapi_app
```

Inside the text editor, include the following lines:

```nginx
server {
    listen 80;   
    server_name <public-ip-of-the-instance>;    
    location / {        
        proxy_pass http://127.0.0.1:8000;    
    }
}
```

We need to link our new file

```bash
sudo ln -s /etc/nginx/sites-available/fastapi_app /etc/nginx/sites-enabled/
```

We need to test our configurations then reload nginx

```bash
sudo nginx -t
sudo systemctl reload nginx
```

## Cloning our FastApi App

Inside the web server terminal, run:

```bash
git clone https://github.com/Munjogu123/book-review-api.git
```

Navigate to the book-review-api directory:

```bash
cd book-review-api
```

Install the dependencies in the `requirements.txt`.

With the dependencies installed, navigate to the api directory and run our FastApi App.

```bash
cd api
python3 -m uvicorn main:app
```

This will run the app and if we go to our browser and type `http://<public-instance-ip>/users` we are able to see our app.

To perform tests on our API more conveniently, we can use the swagger docs at `http://<public-instance-ip>/docs`.

## 🧹 Clean Up Resources

Once done with the resources we can destroy them to avoid incurring additional costs.

Back in our local terminal inside the aws directory, run the following command:

```bash
terraform destroy
```

Type yes when prompted to confirm.
