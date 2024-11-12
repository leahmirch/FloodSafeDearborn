# Flood-Safe Dearborn

The FloodSafeDearborn project is providing real-time flooding information in an interactive method for residents of Dearborn, Michigan. Dearborn, like many parts of Metro Detroit, has areas with low elevations, which ultimately can lead to water accumulation during heavy rains. For example, the Rouge River, which runs through the city of Dearborn, can overflow during significant rain events, further contributing to flooding. In addition to this, Dearborn has an aging sewer and drainage system and like many older cities in the U.S, has combined sewer systems where stormwater and sewage are handled by the same pipes. This means that, during heavy rainfall, the system itself can become overwhelmed, causing flooding in streets, homes, and basements. This is precisely why FloodSafeDearborn is needed to assist in the protection of the Dearborn area and its residents.

With all of this information in mind, FloodSafeDearborn focuses on the accessibility of real-time data regarding active flooding in Dearborn communities. The project itself will be broken down more specifically in the implementation plan, however it is important to mention a few key features the project will have, such as: interactive flooding maps showing flood hotspots, a notification system to alert users of flooding near their address, and data analytics for emergency routes due to flooding. With the ability to to interact with flooding maps in order to view and alert other community members of flooding in the area, FloodSafeDearborn aims to enhance access to resources and mitigate risks involved with flooding in the urban community. In addition to the technical attributes of the project, there will additionally be accessibility to professional resources such as the Wayne County Drain Commissioner, and resources for homeowners on flood preparedness. This project offers a significant advantage by empowering residents to protect their homes and themselves through staying informed and updated at all times.

## Features

need to add *****

## How to Use

1. **Setup**: Ensure you have XAMPP or any local server with PHP support, as well as SQLite enabled.

2. **Database Setup**:
   - This project uses SQLite, which automatically creates a `user_db.sqlite` file in the project folder upon first connection.
   - The `db.php` file handles database connection and ensures the necessary `users` table is created if it doesn't exist.

3. **Running the Project**:
   - Place the project files in your server’s root directory (e.g., `htdocs` folder in XAMPP).
   - Start the server and open the browser at `http://localhost/project_folder_name`.

4. **User Registration**:
   - Go to the `register.php` page to create a new account.
   - Fill in the username, email, password, upload an optional profile image, and write a self-introduction in the rich text editor.
   - Submit the form to register.

5. **Login**:
   - Go to `login.php` to log in with your registered username and password.
   - Upon successful login, you’ll be redirected to your homepage (`home.php`).

6. **Profile Update**:
   - On your homepage, click "Edit Profile" to navigate to `profile.php`.
   - Here, you can update your password, change your profile image, and edit your self-introduction using the rich text editor.

7. **Logout**:
   - Click "Logout" on the homepage to log out of your account.

## Notes

- **Convert PHP to Python / HTML / CSS**
- **Add History Section for README**
