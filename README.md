# Automated Network Download Analyzer

## Overview

This project implements an automated network monitoring system that measures download performance from multiple global servers over time.
The system downloads a standardized 100MB test file from different servers and analyzes:

Network latency
TCP handshake time
Throughput (download speed)
Transfer stability

The collected data is stored in MongoDB Atlas and visualized through a Python dashboard.
The goal of the project is to analyze network congestion patterns and throughput trends over a 24-hour period.

## Core Idea

The system acts as a network probe that repeatedly downloads files from global servers and records performance metrics.
By analyzing the collected data over time, the system can identify:

Peak congestion periods
Best performing servers
Throughput variations during the day
Network stability patterns

## System Architecture

<img width="331" height="455" alt="image" src="https://github.com/user-attachments/assets/a7520541-cde2-4a27-aade-8a56df7331e4" />

## Features

Automated network download testing
Multiple fallback servers
TCP latency measurement
TCP handshake measurement
Throughput calculation
Transfer variance analysis

## Metrics Collected

Each measurement stores:

timestamp
server_name
server_ip
latency_ms
tcp_handshake_ms
download_time_sec
throughput_Mbps
transfer_variance

## Project Structure

<img width="573" height="346" alt="image" src="https://github.com/user-attachments/assets/349e0530-044b-40b2-abb8-fa8ea785de1c" />

## Installation

->Clone the repository:

git clone https://github.com/YOUR_USERNAME/network-download-analyzer.git

cd network-download-analyzer

->Install Dependancies:

pip install -r requirements.txt

## MongoDB Setup

This project requires a MongoDB Atlas database.
Replace the placeholder connection string in: 

->azure_downloader/config.py

->local_analyzer/data_fetcher.py

<img width="1031" height="325" alt="image" src="https://github.com/user-attachments/assets/cbbef21a-f606-4856-9484-610ee9ab29ce" />

## 24-Hour Network Analysis

To run continuous measurements, schedule the probe using cron.
Example cron job:
=> 0 * * * * python runner.py

This runs the probe every hour.

After 24 hours the dashboard will display:
hourly throughput trends
latency patterns
server performance comparisons
congestion analysis

## What Your Dashboard Report Shows

->The final report includes:

throughput trends over time
latency variation
server comparision
hourly network traffic patterns
stability analysis
This allows identification of network congestion and performance patterns.
Interactive dashboard visualization

<img width="335" height="287" alt="image" src="https://github.com/user-attachments/assets/e955744a-3c1a-466c-8534-332c3a9efb9e" />

<img width="374" height="208" alt="image" src="https://github.com/user-attachments/assets/8c2d359f-67c1-4174-8ce2-087f1063082a" />

