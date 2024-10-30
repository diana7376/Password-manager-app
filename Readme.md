# 🔒 **LockR** - Backend 🧮


****
<p align="center">
  <img width="300" src="https://i.imgur.com/WR8JhwQ.png" alt="Sublime's custom image"/>
</p>

****

## 📝 About The Project

**LockR** is a user-friendly WebApp that provides a secure solution for managing online passwords, designed by UTM Software Engineering students as a second-year internship project at Complexica.
##### ❓ Why LockR?
- Simplifies secure password management with features like a built-in password generator, customizable groups, and password history tracking.
- Focuses on both security and usability, helping users organize passwords efficiently without compromising data safety.
##### 📌 Key Features
- **Strong Password Generator**: Generates complex, random passwords for enhanced security.
- **Organized Storage**: Users can group passwords by categories, such as “Work” or “Personal,” for easy access.
- **Password History Tracking**: Allows users to view previous passwords after updates, helpful for verification or reverting.
##### ✨Project Highlights
- Simple registration and login, making the app accessible and intuitive.
- Full control over password items: Users can add, edit, delete, and organize passwords into groups.
- Developed with a focus on cybersecurity and ease of use, addressing real-world password management needs.

****
### 🔨 Built With
<p align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=python,django,mysql" />
  </a>
</p>

****
## 🧑‍💻 Getting Started

Follow these steps to set up the backend of **LockR** locally.

### ☝️🤓 Prerequisites

Ensure you have the following prerequisites installed before setting up LockR:

- **Python 3.x**  
    You can download it from [python.org](https://www.python.org/downloads/).
    
- **MySQL**  
    Follow the installation guide for your OS at [MySQL Installation Guide](https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/).

### ⚙️ Installation

*Follow these steps to install and configure LockR's backend:*

1. Clone the Repository
```sh
   git clone https://github.com/diana7376/Password-manager-app-backend
```
2. Install the required packages
``` sh
   python install_packages.py
```
3. Access the right directory
   ```sh
   cd locker_backend
   ```
4. Connect to your own MySQL DB in `locker_backend/settings.py`
   ```python
    DATABASES = {  
        'default': {  
            'ENGINE': 'django.db.backends.mysql',  
            'NAME': 'dbname',  
            'USER': 'username',  
            'PASSWORD': 'password',  
            'HOST': 'localhost',  
            'PORT': '3307'  
        }  
    }
   ```
   
5. Apply migrations
   ```sh
   python manage.py migrate
   ```
6. Run the server
   ```sh
   python manage.py runserver
   ```

****

## 🗺️ Roadmap

- [x] Implement the CRUD operations
- [x] Secure passwords in the DB
- [x] Implement Pagination
- [x] Implement Searching Functionality
- [x] Passwords Grouping
- [x] Auth via JWT
- [ ] Passwords Sharing

See the [project view](https://github.com/users/diana7376/projects/2) for a full list of tasks in progress, proposed features (and known issues).

****
## ⛑️ Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


