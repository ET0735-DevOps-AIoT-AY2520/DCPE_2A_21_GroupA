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

Authorized staff are responsible for maintaining the system and library records.

Staff-related functions include:
- Managing book records and availability in the database.
- Monitoring user borrowing and reservation activity.
- Ensuring kiosk hardware is operational.
- Overseeing fine collection and reservation cancellations

## Flutter app

## Firebase

## Rasberry Pi

## Other Useful Infomation



