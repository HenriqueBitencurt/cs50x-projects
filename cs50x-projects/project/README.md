# StudySync

#### Video Demo:(https://www.loom.com/share/9fbbf034a1db4c459aecabe8685b5bab)

#### Description:
StudySync is a comprehensive web-based academic hub and productivity suite designed specifically for students to manage their daily school life, assignments, upcoming exams, grades, and focus sessions in a single, unified platform. Developed as the final project for CS50's Introduction to Computer Science, StudySync bridges the gap between traditional planners and digital workflow tools, leveraging a clean, modern interface built with Bootstrap and JavaScript, powered by a robust Python Flask backend and a secure SQLite database.

## Architecture and File Structure

The project follows a traditional Model-View-Controller (MVC) architectural pattern adapted for Flask web applications, ensuring a clean separation of concerns between business logic, data storage, and the user interface.

### Backend and Core Logic
- **`app.py`**: The central application controller. It initializes the Flask application, configures session management, handles database connections via SQLite, and defines all route handlers (such as user authentication, dashboard rendering, task manipulation, exam tracking, and grade management).
- **`helpers.py`**: Contains utility functions and custom decorators—most notably the `login_required` decorator, which protects sensitive routes from unauthorized access by checking user sessions.

### Database
- **`project.db`**: An SQLite database file that stores all persistent relational data across the platform. It includes structured tables for users (handling secure password hashing with Werkzeug), tasks, exams, and academic grades, establishing robust foreign-key relationships to ensure data integrity per user.

### Templates (Frontend HTML)
- **`layout.html`**: The master layout template incorporating Bootstrap CSS frameworks, navigation bars, dynamic flash messages, and standard footers, ensuring a consistent design across all pages.
- **`index.html`**: The main dashboard view. It brings together high-priority tasks, upcoming exams, a summary of recent grades, and an integrated JavaScript-powered Pomodoro timer.
- **`login.html` & `register.html`**: User authentication interfaces providing secure access control with immediate client-side and server-side validation.
- **`tasks.html`**: The dynamic task management interface where users can add, view, update, and delete school assignments or personal milestones.
- **`exams.html`**: The dedicated schedule page for tracking upcoming tests, quizzes, and major evaluations sorted by chronological urgency.
- **`grades.html`**: The academic performance calculator and table view, allowing students to input grades per subject and track their overall averages automatically.

### Static Assets
- **`styles.css`**: Custom CSS stylesheets overriding and enhancing standard Bootstrap styles to establish a cohesive, modern dark/light aesthetic optimized for long study sessions.
- **`script.js`**: Client-side scripts powering interactive components, particularly the real-time countdown logic for the Pomodoro focus timer and dynamic UI feedback elements.

## Design Choices and Rationale

During the development of StudySync, several key architectural and design decisions were made to balance complexity, user experience, and technical constraints:

1. **Choice of Framework (Flask vs. Django):**
   Flask was selected over heavier alternatives like Django because it provides a lightweight, flexible micro-framework structure. This allowed for granular control over routing, session handling, and database interactions using raw SQL queries via SQLite, directly aligning with the core concepts taught throughout CS50 while keeping the application fast and efficient.

2. **Integrated Productivity Tools (The Pomodoro Timer):**
   Rather than keeping StudySync strictly as a passive CRUD (Create, Read, Update, Delete) application, integrating a live JavaScript Pomodoro timer directly into the dashboard transforms it into an active workspace. This design choice elevates the project's functional complexity and utility for actual daily study habits.

3. **Database Schema and Relational Integrity:**
   User isolation was a primary security and architectural focus. Every table (`tasks`, `exams`, `grades`) links directly to a unique `user_id` foreign key. This ensures that multi-user data segregation is strictly enforced at the database level, preventing unauthorized cross-account data exposure.

4. **Responsive Frontend with Bootstrap:**
   Bootstrap was chosen to rapidly prototype and style a professional, mobile-responsive user interface without spending excessive time writing vanilla CSS boilerplates from scratch, ensuring that the application looks polished across various screen sizes.
