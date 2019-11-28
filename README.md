# Entry Management
GitHub Repository Link : https://github.com/khatryshikha/entrymanagement.git

Entry Management System Software application is used to keep the track of the visitors that we have in office and outside. The set of APIs has been created to store visitor and host information, once the user enters the information in the form which will trigger an Email and a SMS to the host informing him of the details of the visitor. At same the provision of the checkout time link is given to the visitor via SMS as well as by Email. The link will trigger an email to the guest with the complete visiting information.


1. [API for Host Details](#1-api-to-host-details)
2. [API to Visitor Details](#2-api-to-visitor-details)
3. [API to send Checkout time SMS and Email](#3-api-to-send-checkout-time-sms-and-email)

Technologies used:
  - Python/ Django framework
  - MySQL
  - Textlocal API
  
## Move To
- [Installation Instructions](#installation-instructions)
- [API 1 - API for Host Details](#1-api-to-host-details)
- [API 2 - API to Visitor Details](#2-api-to-visitor-details)
- [API 3 - API to send Checkout time SMS and Email](#3-api-to-send-checkout-time-sms-and-email)
  
## Installation Instructions
  1. clone the project
  `git clone https://github.com/khatryshikha/entrymanagement.git`
  2. cd to project folder `cd entrymanagement` and create virtual environment
  `virtualenv -p python3 venv`
  3. activate virtual environment
  `source venv/bin/activate`
  4. install requirements
  `pip install -r requirements.txt`
  5. go to `credentials.py` enter your Email ID and password from which you what to send an Email.
  Note: To avoid the `Login credentials not working with Gmail SMTP` error go to the above provided Email ID Account by this link `https://www.google.com/settings/security/lesssecureapps` and `Enable` Access for less secure apps.
  6. Create the local database
  `python manage.py migrate`
  `python manage.py makemigrations`
  7. run the server
  `python manage.py runserver 8000`
   
## 1. API for Host Details (/host_details)
This API triggers to store a host information provided by visitor in database via form.

API - `http://127.0.0.1:8000/host_details`
(methods supported - GET, POST)

  ### API Response
  Will render you to the visitor's information form.


## 2. API to Visitor Details (/visitors)
This API triggers to store a visitors information given by visitor in database via form.

API - `http://127.0.0.1:8000/visitor_details`
(methods supported - GET, POST)

  ### API Response
 It will send an Email and SMS to respective Host regarding the visitor. At the time of checkin an Email is also triggered to the visitor providing the link, which need to be triggered at the time of checkout.
  
  ### Screenshots of Host/Visitor Emails and SMS
    Email to Host with visitors details

  <p align="center">
    <img src=https://user-images.githubusercontent.com/30694592/69783818-4ff1a280-11da-11ea-95f4-a4159daf1c75.jpg width="300">
  </p>
 

    SMS to Host with visitors details
  
  <p align="center">
    <img src=https://user-images.githubusercontent.com/30694592/69785387-f0959180-11dd-11ea-8008-13e49a716e20.jpg width="300">
  </p>


    Email to visitors details with Checkout link
  
  <p align="center">
    <img src=https://user-images.githubusercontent.com/30694592/69784010-ca222700-11da-11ea-8f56-44f3af2d2c35.jpg width="300">
  </p>

    SMS to visitors details with Checkout link

  <p align="center">
    <img src=https://user-images.githubusercontent.com/30694592/69793781-1bd4ac80-11ef-11ea-9f1c-d96915156ca6.jpg width="300">
  </p>



## 3. API to send Checkout time SMS and Email (/visitor_checkout/<stringID>)
This API will set the Checkout time of the visitor, when the visitor opens the link provided in the above Mail. At the same time it will send a thank you email with complete details of the visit to the guest.

API : `http://127.0.0.1:8000/visitor_checkout/<ID>`
(methods supported - GET, POST)

<b>Examples:</b>
  ```
  http://127.0.0.1:8000/visitor_checkout/fc88f4d4-cc29-4521-a3a4-f86cbf34cdcf
  ```

  ### API Response
  It will trigger a Email to visitor Email ID.

  ### Screenshots of Host/Visitor Emails and SMS
    Visiting details Email to visitor
  <p align="center">
    <img src=https://user-images.githubusercontent.com/30694592/69784831-bbd50a80-11dc-11ea-9f07-e648ed41d10f.jpg width="300">
  </p>


  