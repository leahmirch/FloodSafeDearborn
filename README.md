# FloodSafeDearborn

**FloodSafeDearborn** provides **real-time flooding information** and resources to the residents of **Dearborn, Michigan**, helping them stay informed, safe, and prepared during flood events. Dearborn's low elevations, overflow-prone Rouge River, and aging combined sewer systems make it highly vulnerable to flooding, especially during heavy rains. This platform addresses these challenges by offering interactive tools, alerts, and preparedness resources to mitigate flood risks in the community.

## Features  

- **Interactive Flood Map**  
  Displays real-time and historical flooding data on an **interactive map**, highlighting active flood hotspots and allowing users to report new events. Events are categorized by water levels, severity, closed roads, traffic conditions, and flood risks, with dynamic icons and descriptions for clarity.

- **Flood Alerts and Notifications**  
  Users can configure **personalized notifications** via email to receive alerts about floods, road closures, rising water levels, and other critical updates near their location.  

- **User Event Reporting**  
  Community members can seamlessly submit **flood event reports** using an intuitive form. Location input is simplified through address search (powered by **Mapbox**) and current location access. Reports appear dynamically on the interactive map for all users.  

- **Flood Preparedness Resources**  
  Access resources, including homeowner flood preparedness guides, evacuation routes, safety tips, and professional contacts like the **Wayne County Drain Commissioner**.

- **User Account Management**  
  Users can **register**, log in, and manage their profiles, including updating email, passwords, and profile pictures. Notifications and flood event settings can be customized for a tailored user experience.

- **Data Visualization and Historical Trends**  
  The platform offers statistical analysis and **interactive charts** using Plotly to visualize flooding trends, severity levels, and high-risk areas over time, providing valuable insights for residents and emergency planners.

- **Admin Tools**  
  Administrators can manage flood event reports and user accounts efficiently, ensuring data accuracy and platform integrity.

## Why FloodSafeDearborn?  

- Empowers residents to stay informed about flood risks.  
- Enhances community preparedness with real-time alerts and reliable flood reporting tools.  
- Provides data-driven insights for safer emergency responses and flood mitigation.  
- Offers essential resources for residents and local authorities to protect homes and infrastructure.  

## How to Use

### Instructions to Run the Project

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
Run the Flask application from the `backend` folder.

```bash
python backend/app.py
```

#### **5. Access the Application**
Open a web browser and go to the following URLs:
By default, the Flask server will start on `http://127.0.0.1:5000`.

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
├── procfile
├── requirements.txt   
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
- Bethany Slone & Leah Mirch: Configured oauth2 emailing service with floodsafedearborn@gmail.com email
- Leah Mirch: Finalized oauth2 emailing service with floodsafedearborn@gmail.com email, tested with different authorized emails and events
- Sukeina Ammar: Updated statistical data page graphs with accurate data and text
#### 12/16/24
- Sukeina Ammar: Added procfile and requirements.txt files

## Notes
No notes at the time.
