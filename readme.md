# Food Service Automation

A small automation project I built while working at **Siloam Hospitals**.

## Background

Siloam Hospitals provides lunch for its employees. To receive lunch, employees need to submit a **Microsoft Form** every month.

Submitting the form manually every month felt like a bit of a waste of time — just kidding, it takes 10 seconds for each submission. 😄

Since I had some development experience, I thought it would be a fun opportunity to automate the process.

## How It Works

My first intuition was to investigate what happens when submitting the Microsoft Form.

Instead of interacting with the form manually, I inspected the API request made when submitting the form and identified the required payload.

Once I figured out the required request, I was able to reproduce the form submission programmatically and run it locally.

The next question was:

> **Where should the automation run?**

## Automation Options

I considered a few different approaches:

1. **GitHub Actions**
2. **Cron + Shell Script (Linux)**
3. **Task Scheduler (Windows)**

Initially, I implemented the automation using **GitHub Actions**. However, due to the limitations of GitHub Actions on free accounts, I decided to run the automation locally instead.

I chose **Linux through WSL (Windows Subsystem for Linux)** because I also wanted an opportunity to learn a little more about Bash scripting and Linux's `cron` scheduler.

## Running with WSL

### 1. Install WSL

First, install **Windows Subsystem for Linux (WSL)** and make sure a Linux distribution such as Ubuntu is available.

### 2. Create a Shell Script

I created a shell script called `run-food-service.sh`:

```bash
#!/bin/bash

cd ~/food-service-automation

source .venv/bin/activate

python -m src.main

deactivate
```

The script does three things:

1. Changes the working directory to the project.
2. Activates the Python virtual environment.
3. Runs the application's main module.
4. Deactivate Python virtual environment.

### 3. Make the Script Executable

Run:

```bash
chmod +x run-food-service.sh
```

### 4. Test the Script Manually

Before configuring the automation, make sure the script works:

```bash
./run-food-service.sh
```

If everything works correctly, the application should run just like it does when executing it manually.

## Schedule with Cron

Once the script works, I use Linux's `cron` to run it automatically.

Open the crontab editor:

```bash
crontab -e
```

Then add:

```cron
0 9 15 * * /home/yourname/food-service-automation/run-food-service.sh >> /home/yourname/food-service-automation/cron.log 2>&1
```

This cron expression means:

| Field   | Value | Meaning             |
| ------- | ----: | ------------------- |
| Minute  |   `0` | At minute 0         |
| Hour    |   `9` | At 9 AM             |
| Day     |  `15` | On the 15th day     |
| Month   |   `*` | Every month         |
| Weekday |   `*` | Any day of the week |

So the automation runs:

> **At 09:00 on the 15th day of every month.**

The output and errors are also redirected to `cron.log`:

```text
cron.log
```

This makes it easier to check whether the automation ran successfully.

## Project Structure

A simplified project structure looks like this:

```text
food-service-automation/
├── .venv/
├── src/
│   └── config.py
│   └── food_service.py
│   └── forms_client.py
│   └── main.py
├── requirements.txt
├── run-food-service.sh
└── cron.log
```

## Why I Built This

This project was a small personal automation experiment that allowed me to explore several things:

* Inspecting API requests
* Understanding HTTP request payloads
* Automating a web form submission
* Python virtual environments
* Bash scripting
* WSL
* Linux `cron`
* Running scheduled background tasks

The actual problem was relatively small, but it was a good opportunity to turn a repetitive monthly task into something that could run automatically.

## Disclaimer

This project was created as a personal automation experiment while I was working at Siloam Hospitals.

The implementation depends on the specific form and API behavior at the time it was created and may no longer work if the form or its backend changes.
