# Changelog - LockR  
****
## November 8 - 22, 2024
### Pasword share Implementation 

**Enhancements** to Group Management and Sharing Functionality
We’ve added exciting new features to make password sharing easier and more secure than ever. Now, you can:
**1. Invite Users to Groups:**
  - Easily invite others to your groups by entering their **username** or **email**.
**2. Seamless Sharing of Group Passwords:**
  - Once users accept the invitation, they gain view-only access to the group and its passwords. This ensures they can collaborate securely without modifying your data.
**3. Accept or Decline Invitations:**
  - Users have full control over invitations. They can accept to join the group or decline if they wish not to participate. This can be done via dedicated API endpoints or email links.
**4. Secure Permission Management:**
  - Group owners retain full control over group passwords and settings. Invited users have restricted access, ensuring they can only view the group and its contents.

**Visual updates**

<img src="https://github.com/user-attachments/assets/32c6ddf1-811f-4fb0-899c-959a2591d20c" alt="Share" width="350" height="400" />

Here is the visual demonstration of the vizial implementation.
### Dark Mode Implementation

In this update, a comprehensive dark mode was implemented for the web application. The changes include:

1. **General Styling:**
   - The application background was updated to a dark blue (#001529) with consistent light-colored text (#ffffff) for readability.
   - Smooth transitions were added for background and text color changes.

2. **Pagination:**
   - The pagination buttons and the current page indicator were styled to align with the dark mode theme.
   - Button text was made white, with a dark blue background for hover and active states.
   - The current page number displays a white outline and white text for better visibility.
  

3. **Modal Adjustments:**
   - Modals for features like password details, history, and editing were updated to have a dark blue background.
   - All modal text elements, including titles and buttons, were adjusted to white for consistency.
   - Specific components like the "eye" button for password visibility and dropdown selectors were restyled to ensure white text and proper hover effects.

4. **Switch Mode Button:**
   - A toggle switch was added to enable users to seamlessly switch between dark mode and light mode.
   - The switch ensures a smooth transition, maintaining consistent styles for all elements in both modes.

5. **Accessibility Improvements:**
   - Focus effects were enhanced with subtle outlines for key elements to maintain usability in dark mode.
   - Contrast was improved for all interactive elements like buttons and links.

6. **Customizations:**
   - Buttons such as "Show All" and modal close icons were updated to white to match the overall theme.
   - Table rows and headers were aligned with the dark theme for a seamless appearance.

This implementation ensures a visually appealing and consistent dark mode experience across all components of the web application while preserving functionality, accessibility, and user preferences.

**Visual updates**

<img width="1440" alt="Screenshot 2024-11-22 at 14 22 09" src="https://github.com/user-attachments/assets/75fec541-97ae-4547-95ab-1d844b06fe38">
<img width="1439" alt="Screenshot 2024-11-22 at 14 27 56" src="https://github.com/user-attachments/assets/7a105461-609d-49b7-890f-43f327967a2d">


This screenshots highlights the dark mode implementation, showcasing its contrast and design compared to the light mode.


<img width="524" alt="Screenshot 2024-11-22 at 14 29 58" src="https://github.com/user-attachments/assets/43977471-fabd-422b-b3bf-df91d781213e">
<img width="528" alt="Screenshot 2024-11-22 at 14 30 48" src="https://github.com/user-attachments/assets/450d6fd7-97de-4423-a647-d942cf0d4c0f">
<img width="522" alt="Screenshot 2024-11-22 at 14 31 05" src="https://github.com/user-attachments/assets/00d9c94e-d10c-47ef-813c-ce7e8a167d9e">
<img width="602" alt="Screenshot 2024-11-22 at 14 31 30" src="https://github.com/user-attachments/assets/1ab0f3e2-88a9-420b-84ae-f3a1aaa8ee48">

These screenshots demonstrate the updated modals in dark mode, featuring a dark blue background and white text for improved readability.




### Deployment implementation 
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
- **Report improvements**: [Report link](https://www.overleaf.com/project/66f295b42270ce28a2e84659)
    - **Abstract and introduction**: We updated the texts for the introduction as well as the abstract of our report.
    - **Text improvement**: We formatted the text of the report, took out words in bold inside the text, commented the diagrams and updated their placement on the page.
