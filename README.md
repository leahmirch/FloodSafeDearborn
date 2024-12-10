# Flood-Safe Dearborn

The FloodSafeDearborn project is providing real-time flooding information in an interactive method for residents of Dearborn, Michigan. Dearborn, like many parts of Metro Detroit, has areas with low elevations, which ultimately can lead to water accumulation during heavy rains. For example, the Rouge River, which runs through the city of Dearborn, can overflow during significant rain events, further contributing to flooding. In addition to this, Dearborn has an aging sewer and drainage system and like many older cities in the U.S, has combined sewer systems where stormwater and sewage are handled by the same pipes. This means that, during heavy rainfall, the system itself can become overwhelmed, causing flooding in streets, homes, and basements. This is precisely why FloodSafeDearborn is needed to assist in the protection of the Dearborn area and its residents.

With all of this information in mind, FloodSafeDearborn focuses on the accessibility of real-time data regarding active flooding in Dearborn communities. The project itself will be broken down more specifically in the implementation plan, however it is important to mention a few key features the project will have, such as: interactive flooding maps showing flood hotspots, a notification system to alert users of flooding near their address, and data analytics for emergency routes due to flooding. With the ability to to interact with flooding maps in order to view and alert other community members of flooding in the area, FloodSafeDearborn aims to enhance access to resources and mitigate risks involved with flooding in the urban community. In addition to the technical attributes of the project, there will additionally be accessibility to professional resources such as the Wayne County Drain Commissioner, and resources for homeowners on flood preparedness. This project offers a significant advantage by empowering residents to protect their homes and themselves through staying informed and updated at all times.

## Features

- **Interactive Flood Map**: Displays real-time flood data on an interactive map to help residents identify flood-prone areas and take necessary precautions.
- **Notification System**: Allows users to set up alerts for flooding near their location, enabling timely evacuation or preparations.
- **Data Analytics for Emergency Routes**: Provides information on safe routes during flood events, helping users avoid flooded areas.
- **Flood Preparedness Resources**: Offers resources and links to professional organizations, such as the Wayne County Drain Commissioner, and homeowner tips for flood preparedness.
- **Customizable User Experience**: Users can personalize their settings for receiving alerts and accessing resources.

## How to Use

### Instructions to Run the Converted Project

#### **1. Install Python**
Ensure you have Python 3.7 or later installed on your system. You can download it from [python.org](https://www.python.org/).


#### **2. Install Required Libraries**
Open a terminal or command prompt, navigate to the project directory, and install the required Python libraries:

```bash
pip install flask werkzeug
```

#### **3. Set Up the Database**
The project uses an SQLite database. The setup script will automatically create the `user_db.sqlite` file and the necessary `users` table.

To manually initialize or verify the database:

1. Ensure the `backend/database.py` script has the `setup_database()` function correctly defined.
2. Run the script to create the database:
   ```bash
   python backend/database.py
   ```

This will create a `user_db.sqlite` file in the project directory with a table called `users`.

#### **4. Start the Flask Application**
Run the Flask application from the `backend` folder. Navigate to the `backend/` directory in your terminal and execute:

```bash
python backend/app.py
```

By default, the Flask server will start on `http://127.0.0.1:5000`.

#### **5. Access the Application**
Open a web browser and go to the following URLs:
- **Registration Page**: `http://127.0.0.1:5000/register`
- **Login Page**: `http://127.0.0.1:5000/login`
- **Home Page** (after login): `http://127.0.0.1:5000/home`

#### **6. Folder Structure**
Ensure your project folder structure looks like this:

```
FloodSafeDearborn/
├── backend/
│   ├── mapp/    
│   │   ├── app.js
│   │   ├── flood-data.js
│   │   └── map.js
│   ├── app.py              
│   ├── auth.py             
│   └── database.py         
├── frontend/
│   ├── templates/          
│   │   ├── about.html
│   │   ├── admin_manage_events.html
│   │   ├── admin_manage_users.html
│   │   ├── contact.html
│   │   ├── evemt_details.html
│   │   ├── home.html
│   │   ├── index.html
│   │   ├── interactive_chart.html
│   │   ├── layout.html
│   │   ├── listings.html
│   │   ├── login.html
│   │   ├── manage_account.html
│   │   ├── notification_settings.html
│   │   ├── register.html
│   │   ├── resources.html
│   │   ├── safety_tips.html
│   │   ├── search_results.html
│   │   ├── statistical_data.html
│   │   ├── submit_event.html
│   │   └── user_history.html
│   └── static/
│       ├── css/
│       │   ├── address.css
│       │   ├── filter.css
│       │   ├── index.css
│       │   ├── map.css
│       │   └── styles.css
│       ├── data/
│       │   ├── page_content.json
│       │   └── dearborn-boundary.json
│       ├── uploads/
│       └── img/        
└── floodsafe_db.sqlite # SQLite database (created after setup or run "python backend/database.py")
```

#### **7. Debugging**
To debug the application, you can use Flask's built-in debug mode. Start the server with:

```bash
FLASK_ENV=development python backend/app.py
```

## History Documentation
#### 10/29/24 
- Leah Mirch: Initial Flood Safe Dearborn commit
#### 11/05/24 
- Leah Mirch: Updated starting version
#### 11/10/24 
- Paul Murariu: Uploaded frontend templates from Figma
#### 11/15/24 
- Leah Mirch: Converted PHP to Python / HTML / CSS
- Leah Mirch: Worked on Index page, and styling for register / login / logout
#### 11/16/24 
- Leah Mirch: Added search bar, adjusted header, created content for resources, contact, about and safety tips pages
#### 11/20/24 
- Sukeina Ammar: Created interactive flood map, uploaded code
- Leah Mirch: Integrated interactive flood map code, updated home.html and layout.html
#### 12/01/24
- Leah Mirch: Created submit_event.html for user event reporting, updated the database schema to include events and tables for each event type (water_levels, flood_severity, closed_roads, flood_reports, traffic_conditions), implemented auto-search address functionality using Mapbox Geocoder, enhanced the flood map to display event types with correct symbols and detailed descriptions in human-readable format, formatted dates as MM/DD/YYYY with a 12-hour time format, added a Dearborn boundary outline (dearborn-boundary.json), created a toggle section to filter events on the map, and updated project styling (map.css, styles.css, address.css, filter.css)
#### 12/04/24
- Leah Mirch: Added access to user's current location for event reporting, and updated main layout navigation bar to have more interactive user profile / login / registration, and added new navigation bar for when a user is logged in for pages: manage account, notification settings, statistical data, and user history
#### 12/05/24
- Leah Mirch: Created manage account page, allowing users to upate email and password. Integrated profile picture upload in "Manage Account," allowing users to upload PNG, JPG, or JPEG images, dynamically displayed in the navigation bar and fallback to base-pfp.png when unset or logged out. Updated flash message styling to apply correct CSS styles and ensured proper spacing. Fixed navigation bar profile picture behavior to update dynamically for logged-in users. Added favicon functionality using logo.png for the webpage tab. Implemented dynamic session updates for user details to reflect changes instantly
- Leah Mirch: Implemented and optimized TF-IDF-based search functionality, allowing users to query content across multiple pages with relevance-based results. Updated search results to display detailed descriptions, improved relevance labels, and excluded irrelevant pages (e.g., the notification settings). Enhanced usability with user-friendly page names in search results and recommendations
- Leah Mirch: Added listing pages with pagination to enable users to navigate event data efficiently (event_details.html & listings.html). Implemented fixes for user profile picture errors, ensuring new users are assigned a default image (img/base-pfp.png) during registration and allowing profile pictures to update correctly upon upload, with paths stored and displayed consistently across the application
#### 12/08/24
- Leah Mirch: Added admin controls to manage events and manage users. Admins can now edit event details, including address, duration, date/time, and specific details based on the event type, ensuring accuracy across all records. Additionally, admins have the ability to delete events. Admins can edit user's details like change their email, username, password, and reset their profile picture if needed. The admin can also promote a user to an admin role. Additionally, admins can delete user's accounts
- Leah Mirch: Added contact, privacy policy and terms of service links
- Leah Mirch: Added historic flood events onto the map with location and dates. Also added the option to toggle them on and off like other events
#### 12/09/24
- Sukeina Ammar: Created statistical page with interactive diagrams, uploaded code
- Leah Mirch: Integrated statistical page with interactive diagrams into code base
- Bethany Slone: Created notification settings page, uploaded code
- Leah Mirch: Integrated temporary notification settings logging into code base
#### 12/10/24
- Bethany Slone & Leah Mirch: Configured and finalized oauth2 emailing service with floodsafedearborn@gmail.com email

## Notes
1. Additional Submission Requirements
- design 10 test cases to verify that the functionality is correctly implemented
- deliverables:
    - report: no more than 5 pages in PDF format, using screenshots to describe what has been implemented
    - time card: an excel file detailing the hours each team member has worked on specific tasks