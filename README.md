This is a beginner level, simple Django-based blog application which uses CRUD operations , that allows users to register, log in, and create and manage articles. The application includes features for user authentication, article management, author management, and OTP-based password recovery via SMTP email.
---------------------------------------------------------------------------------------------------------------------------------------------------------------
Features
1. User Authentication:
    Users can register, log in, and log out.
   
2. Author and Article Management:
Authors can be added and listed.
CRUD operations for articles, including adding, editing, and deleting articles.
Articles are paginated, with 3 articles displayed per page.

3. OTP-based Password Recovery:
Users can request a password reset.
OTP (One-Time Password) is sent via email through SMTP for login authentication.

4. SMTP Email Integration:
Email functionality is set up using Django's SMTP configuration.
Mailtrap is used for email testing and sending OTPs securely.
