'Automated Student Attendance System'

A comprehensive web-based attendance management system built with Python, Flask, and SQLite that helps educational institutions track student attendance and automatically verify if students meet attendance requirements.

##  Project Objective

Create a simple yet effective system that:
- Manages student records
- Tracks daily attendance
- Calculates attendance percentages
- Checks if students meet minimum attendance requirements using rule-based logic

##  Features

### Core Functionality
- Student Management: Add, view, and manage student records with unique roll numbers
- Daily Attendance Marking: Mark students as Present, Absent, or Late
- Attendance Reports: Generate comprehensive attendance reports with percentages
- Rule-based Verification: Check if students meet customizable attendance requirements (default: 75%)
- Individual Student History: View detailed attendance history for each student

### Technical Features
- Database Storage: SQLite database for persistent data storage
- Responsive UI: Bootstrap-based responsive design that works on all devices
- Real-time Calculations: Automatic attendance percentage calculations
- **Data Validation: Prevents duplicate attendance entries for the same date
- User-friendly Interface**: Clean, intuitive navigation with flash messages

## Technologies Used

| Technology |                   Purpose |
|
| Python 3.7+       |  Backend programming language |
| Flask 2.3.3       |  Web framework for routing and templating |
| SQLite            | Lightweight database for data storage |
| Flask-SQLAlchemy  | ORM for database operations |
| Bootstrap 5       | Frontend framework for responsive design |
| HTML/CSS          | Frontend markup and styling |

##  Prerequisites

Before running this project, ensure you have the following installed:

- **Python 3.7 or higher** - [Download Python](https://www.python.org/downloads/)
- **pip** (Python package installer) - Usually comes with Python
- **Git** (optional) - For cloning the repository

##  Installation & Setup

### Step 1: Clone or Download the Project

```bash
# Clone the repository
git clone https://github.com/yourusername/attendance-system.git

# Or create a new directory
mkdir attendance-system
cd attendance-system