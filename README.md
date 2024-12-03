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
│   ├── figma/    
│   │   ├── homepage.zip
│   │   ├── interactive_map.zip
│   │   └── user_dashboard.zip
│   ├── templates/          
│   │   ├── about.html
│   │   ├── contact.html
│   │   ├── home.html
│   │   ├── layout.html
│   │   ├── index.html
│   │   ├── layout.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── resources.html
│   │   ├── safety_tips.html
│   │   ├── search_results.html
│   │   └── submit_event.html
│   └── static/
│       ├── css/
│       │   ├── address.css
│       │   ├── filter.css
│       │   ├── index.css
│       │   ├── map.css
│       │   └── styles.css
│       ├── data/
│       │   └── dearborn-boundary.json
│       └── img/        
└── floodsafe_db.sqlite          # SQLite database (created after setup)
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

## Notes
- web crawl past flood history (high flood risk areas as colored circles) to appear on map (with start/end dates)
- access current location for event reports
- allow for customizable user profile (prior reports that user has made, notification settings via email)
- create a statistical data section
- create links to contact us, privacy policy, and terms of service in footer section
- create admin account and control panel

submission requirements:
- design 10 test cases to verify that the functionality is correctly implemented
- complete backend implementation: functionality for user system, admin panel, listing pages with pagination, and detailed information pages
- additional points:
   - implement TF-IDF-based search and recommendation
   - incorporate a caching system (either local or cloud-based) for website

 - deliverables:
    - report: no more than 5 pages in PDF format, using screenshots to describe what has been implemented
    - time card: an excel file detailing the hours each team member has worked on specific tasks
