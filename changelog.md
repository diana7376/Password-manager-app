# Changelog - LockR  
****
## November 18, 2024

Happy to announce that our application is finally live on [this temporary domain]([LockR](https://petite-danella-lockr-b5f8b6cb.koyeb.app/about)) where you can try out the latest stable version of **LockR**! 🎉

This was possible with the help of tools such as:
- **Docker** - for containerizing both the React frontend and the Django backend, ensuring the app runs consistently on different environments
- **Nginx** - as a reverse proxy to route the incoming HTTP requests to the appropriate  backend services, and for handling the static files of the frontend
- **React-Scripts** - to build the static files of our React frontend
- **Koyeb** - in order to deploy and manage our application on a serverless hosting and cost-effective platform

Don't forget to check out both the [Backend](https://github.com/diana7376/Password-manager-app-backend) and the [Frontend](https://github.com/diana7376/Password-manager-app-frontend) repos' description or `readme.md` for the changes in the local setup steps.
****
## October 3 - November 7, 2024  

- We added the `readme.md` in both the [Frontend](https://github.com/diana7376/Password-manager-app-frontend) and the [Backend](https://github.com/diana7376/Password-manager-app-backend) repositories to help you better understand our project.  
- Reviewed the app's main functions to make sure everything works smoothly. This prepares us for any final fixes before deployment.  
  - Tested back-end elements and their connection to the database  
  - Tested front-end to ensured that all endpoints work at a good pase.  
- Started research on setting up the app on its own domain (website).  
- **New Feature Ideas**:  
    - **Group Passwords**: We are thinking about adding shared passwords for group accounts, so teams can use one login to access shared info.  
    - **Custom User Roles**: Started planning for user roles, allowing admins to set up different access levels for team members.  
    - **Dark mode:** We started implementing the design for the black mode of our application.  
    - **Forgot password**: We found the need to add a forgot password feature, in case the user forgets the password for our app.  
- Looked into using external servers for secure features, especially one-time passwords (OTPs) for safer logins.  
- Started research on how to make the front-end more readable, looked up how to reuse different elements that repeat on the app, how to improve modularity, readability and ease of use.  
- **Front-End Refactor (TBA)**: Planning a complete overhaul of the front-end code to improve structure and readability.  
- **Report improvements:**  
    - **Abstract and introduction**: We updated the texts for the introduction as well as the abstract of our report.  
    - **Text improvement**: We formatted the text of the report, took out words in bold inside the text, commented the diagrams and updated their placement on the page.