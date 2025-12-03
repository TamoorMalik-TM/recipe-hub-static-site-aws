📘 Recipe Hub – Cloud Project (AWS + Docker + EC2 + ALB + S3 + ASG + CloudWatch)

A production-style cloud engineering project demonstrating how to deploy a secure, scalable, containerized application on AWS using core services such as EC2, Auto Scaling, Load Balancer, S3, CloudWatch, and SNS.

This project was built entirely using WSL2 + Docker on Windows, and deployed manually to AWS (no Terraform / no CI/CD), replicating how real Cloud/DevOps engineers work.

🚀 Project Overview

Recipe Hub is a full-stack web application:

Frontend: Static website hosted on Amazon S3

Backend: Python Flask REST API running inside a Docker container on EC2

Traffic Distribution: Application Load Balancer (ALB)

High Availability: Auto Scaling Group (1–3 EC2 instances)

Monitoring: CloudWatch Metrics, Logs, Alarms

Alerting: SNS Email Notifications

This project simulates a production-grade architecture with scalable backend, monitored systems, auto-healing compute, and proper network security.

🏗️ Architecture Diagram
                         ┌───────────────────────────┐
                         │      S3 Static Website     │
                         │  (HTML / CSS / JavaScript) │
                         └───────────────┬────────────┘
                                         │
                               User loads frontend
                                         │
                                         v
                         ┌───────────────────────────┐
                         │  Application Load Balancer │
                         │         (HTTP:80)          │
                         └───────────────┬────────────┘
                                         │
                               Routes traffic to backend
                                         │
                                         v
              ┌────────────────────────────────────────────────────┐
              │              Auto Scaling Group (ASG)               │
              │  (1–3 EC2 instances based on scaling policies)     │
              │                                                    │
              │   ┌────────────────────┐      ┌────────────────────┐
              │   │    EC2 Instance   │      │    EC2 Instance   │
              │   │  Docker Container │ ...  │  Docker Container │
              │   │   Flask Backend   │      │   Flask Backend   │
              │   └────────────────────┘      └────────────────────┘
              └────────────────────────────────────────────────────┘
                                         │
                              Health checks / metrics
                                         │
                                         v
                         ┌───────────────────────────┐
                         │      CloudWatch Logs       │
                         │      CloudWatch Metrics    │
                         └───────────────┬────────────┘
                                         │
                              Alarm triggers notification
                                         │
                                         v
                         ┌───────────────────────────┐
                         │          SNS Topic         │
                         │      (Email Alerts)        │
                         └───────────────────────────┘

⚙️ Tech Stack
🖥️ Frontend

HTML5

CSS

JavaScript

Hosted on AWS S3 Static Website Hosting

🔧 Backend

Python Flask

JWT Authentication

SQLite local DB (can be replaced with RDS)

Gunicorn Production Server

Dockerized backend

Runs inside EC2 (Amazon Linux 2023)

☁️ AWS Services Used

EC2 (Docker runtime)

Elastic Load Balancer (ALB)

Auto Scaling Group

S3 Static Hosting

IAM Roles / Policies

Security Groups

CloudWatch Metrics

CloudWatch Logs

CloudWatch Alarms

SNS Email Alerts

VPC (default)

📁 Project Structure
recipe_hub_advanced/
│
├── backend/
│   ├── app.py
│   ├── db.py
│   ├── config.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
│
├── frontend/
│   ├── index.html
│   ├── recipe.html
│   ├── create.html
│   ├── login.html
│   ├── config.js
│   ├── style.css
│   ├── main.js
│   ├── recipe.js
│   ├── create.js
│   └── auth.js
│
└── README.md

🧪 Local Development (WSL2 + Docker)
Backend
cd backend
docker build -t recipehub-backend .
docker run -d -p 5000:5000 recipehub-backend


API runs at:

http://localhost:5000

Frontend
cd frontend
python3 -m http.server 8000


Frontend runs at:

http://localhost:8000

☁️ AWS Deployment Steps
1. Deploy Frontend to S3

Create S3 bucket

Enable static website hosting

Upload all frontend files

Update config.js with ALB DNS name

Make bucket objects publicly readable

2. Deploy Backend on EC2 with Docker

Launch EC2 (Amazon Linux 2023)

Install Docker

Use SCP to upload backend files

Build & run Docker container

Expose port 5000

3. Create Application Load Balancer

Create Target Group (port 5000)

Register EC2 instance

Create ALB (HTTP port 80)

Connect Target Group to ALB

Update EC2 security group to allow only ALB

4. Create Auto Scaling Group

Create AMI from working EC2 instance

Create Launch Template using AMI

Configure User Data to auto-start Docker container

Create ASG (min 1, max 3 instances)

Attach ASG to ALB Target Group

5. Setup CloudWatch Monitoring
Alarms created:

ALB 5XX count > 0

EC2 CPU > 70%

SNS Alerts:

Email notification for failures

Real-time alerts for CPU spikes and backend errors

🔒 Security
Network Security Groups

ALB SG: Allow HTTP from public

EC2 SG: Allow port 5000 only from ALB SG

IAM

EC2 Role:

CloudWatchLogsFullAccess (for logging)

Minimal permissions principle

📊 Monitoring & Logging
CloudWatch:

EC2 CPU Utilization

ALB Request Count

ALB Target Health

4XX & 5XX errors

Log streams for backend application logs

SNS:

Sends email alerts for:

Backend errors

High CPU usage

Failed health checks

🎯 What This Project Demonstrates

This project shows real-world skills in:

Deploying containerized applications to AWS

Load balancing & auto scaling

Monitoring and alerting

Hosting static websites

Designing secure VPC architectures

Using Docker in a professional environment

Linux-based development using WSL2

Perfect for roles:

Cloud Engineer

AWS Engineer

DevOps Engineer (Junior/Mid)

📬 Contact

If you'd like to discuss this project or opportunities:

Email: Tamoorawan1122@gmmail.com
LinkedIn: www.linkedin.com/in/tamoor-ilyas-66ab67223
