# Group 1's DevOps Project: Automatic Book Borrowing System

## Overview

The *Automatic Book Borrowing System* is designed to encourage and increase book
borrowing from public libraries by providing an automated reservation, collection,
and return system.

The system integrates:
- A **frontend application** (mobile app / web app), and
- A **Raspberry Pi–based physical kiosk** for book collection and returns.

Firebase is used as the central database to store:
- User profiles
- Book information
- Reservation and borrowing records

![Icon](https://i.postimg.cc/3wT6TRd5/20250207-192745.jpg)

# **Features List**

## For Library Users

The *Automatic Book Borrowing System* allows library users to conveniently reserve,
collect, and return books using both an online application and a physical kiosk.

Through the mobile application or website, users can:
1. Register and log in to their account.
2. View available books across different library branches.
3. Reserve books online before visiting the library.
4. View their borrowed and reserved books with loan details.
5. Extend the loan period once, subject to system rules.

At the physical kiosk, users can:
1. Authenticate by scanning their NRIC or SP Student Card.
2. Collect reserved books if eligibility checks are met.
3. Return books by scanning the ISBN barcode.
4. Pay outstanding fines using the RFID card reader.




## Borrowing Rules & Penalties

The system enforces the following borrowing rules:
- A user may borrow a maximum of **10 books** at any time.
- Each book has a standard loan period of **18 days**.
- Each loan may be extended **once** for an additional **7 days**.

Penalty handling:
- Late returns incur a fine of **$0.15 per book per day**.
- Reserved books not collected within **5 days** are automatically cancelled.
- Users must clear all outstanding fines via RFID payment before collecting new books.




## For Library Staff / Admin

The *Automatic Book Borrowing System* provides an admin panel for authorized staff
to manage library data and monitor system operations.

Through the admin panel, staff can:
1. Create, update (overwrite), and delete book records.
2. Track individual book details such as loan status, reservation status, borrower ID, dates, and location.
3. View overall library data, including the number of books on loan, reserved, and available.
4. Search users to view their borrowed and reserved books and outstanding fine amounts.
5. View system logs for monitoring, troubleshooting, and error diagnosis.
   
To access the admin panel, enter the following in a browser:

http://<Raspberry_Pi_IP_Address>:5000

Requirements:
- The staff device must be connected to the same WiFi network as the Raspberry Pi.


## System Workflow

1. User reserves a book online using the application.
2. Reservation details are stored in Firebase.
3. User visits the library and authenticates at the kiosk.
4. The kiosk verifies eligibility and reservation status.
5. The book is dispensed to the user.
6. Returned books are scanned and recorded in the system.
<img width="572" height="689" alt="Screenshot 2026-01-26 140254" src="https://github.com/user-attachments/assets/011c83e7-f75d-47e6-a13b-52e0a72e329b" />




## System Architecture

The system consists of three main components:
1. A frontend application for users to reserve and manage books.
2. A Firebase database that stores user profiles, book data, and loan records.
3. A Raspberry Pi–based kiosk that handles book collection, returns, and fine payments.

These components communicate to ensure real-time synchronization
between online reservations and physical book handling.

## Logging & Diagnostics

Raspberry Pi logs are available for error diagnosis and troubleshooting.
They help staff identify issues such as scanning failures, payment errors, and unexpected system crashes.

## Non-Functional Requirements

### Database Cost Efficiency

The system minimizes unnecessary database reads by ensuring the Raspberry Pi
only accesses the database when required.

The system operates in two power modes:
- **Idle Mode**: Routine database calls are stopped when there is no user interaction.
- **Active Mode**: Database access resumes when user interaction is detected.

This approach reduces unnecessary database usage and helps lower cloud
infrastructure costs.
## Running the Website

The website runs on a Raspberry Pi using Docker.
A prebuilt Docker image is used for deployment.

```bash
# Pull the Docker image
docker pull poryusp/proj-img:latest

# Run the container on Raspberry Pi
docker run -it --rm --name proj-test \
  --privileged \
  --network host \
  -v /run/udev:/run/udev:ro \
  -v /run/dbus:/run/dbus \
  -v /dev:/dev \
  --device /dev/i2c-1 \
  --device /dev/spidev0.0 \
  --device /dev/spidev0.1 \
  -v "$PWD/serviceAccoutKey.json:/Project/serviceAccoutKey.json:ro" \
  proj-img
```

## Flutter app

- User registration and login
- Online book reservation
- View borrowed and reserved books
- Loan extension functionality
<img width="499" height="617" alt="Screenshot 2026-01-26 140245" src="https://github.com/user-attachments/assets/7bb43c60-f04d-4a4d-a7dc-77b2c31e9afd" />


## Firebase

- Store user authentication data
- Store book and availability records
- Track reservations, loans, and fines
- Sync data between app and kiosk

## Rasberry Pi
<img width="548" height="492" alt="Screenshot 2026-01-26 140346" src="https://github.com/user-attachments/assets/ece0e9a6-3e62-4b8f-8066-535d94cb94e0" />



The Raspberry Pi acts as a self-service kiosk located in the library.

It supports:
- User authentication via card scanning.
- Book collection after eligibility checks.
- Book return through barcode scanning.
- Fine payment verification using RFID.
- Automated dispensing using motors and hardware peripherals.
  <img width="537" height="579" alt="Screenshot 2026-01-26 140229" src="https://github.com/user-attachments/assets/582f609a-1f65-4322-9ce1-0f2c56eec1cc" />

  
## Other Useful Infomation

- Max 10 books per user
- 18-day loan period
- One-time 7-day extension
- $0.15 fine per late day per book

## Other code repositories and Docker

[App Github Repository](https://github.com/Por-Yu-SP/devops_app)<br>
[Docker Hub Repository](https://hub.docker.com/repository/docker/poryusp/proj-img/general)


## Contributions 

| Name     | Contributions |
|----------|---------------|
| **Srikar** | - README<br>- Buzzer<br>- LED<br>- SRS document<br>- LCD display<br>- Associated system test cases<br>- Generated presentation plan<br>- Research on required packages and potential improvements<br>- Cameraman for demo video |
| **Vrishank** | - All RFID functionality<br>- General bug fixes<br>- SRS document<br>- Hardware testing<br>- Brainstorming<br>- General support<br>- Associated system test cases |
| **Thiha** | - Flask server<br>- HTML<br>- All JavaScript code<br>- Data transfer between HTML and `app.py` (both directions)<br>- CSS<br>- Humidity sensor<br>- Servo motor<br>- Related unit tests<br>- Associated system test cases<br>- All SRS graphs<br>- General support<br>- Various related bug fixes |
| **Por Yu** | - Overall code flow and structure<br>- All database functionality<br>- Related unit tests<br>- PiCamera and associated functions<br>- Raspberry Pi log creation<br>- Non-functional requirements<br>- Automatic reservation clearing<br>- Partial LCD implementation<br>- Threading-related components<br>- Bug fixes<br>- Dockerfile creation<br>- Container build<br>- Docker Hub maintenance<br>- All application functionality<br>- SRS document<br>- GitHub upkeep |


