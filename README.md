# Ambient-Intelligence

This project aims to develop an application that uses **Ambient Intelligence** to provide real-time information about buses arriving at the Instituto Superior Técnico (IST) station. The application is designed to be mobile-friendly, ensuring an optimized user experience.

## Features

- **Image Recognition**: Uses the `EasyOCR` library to identify bus numbers from images captured at the station.
- **WhatsApp Notifications**: Automatically sends alerts to subscribed users when their desired bus is about to arrive.
- **Contact Management**: Web interface to add, view, and manage contacts and their bus preferences.
- **Administration Panel**: Admin page to view all contacts and their associated bus preferences.

## Technologies Used

- **Python**: Core language for application development.
- **Flask**: Web framework for building the user interface and handling routes.
- **EasyOCR**: Library for optical character recognition on images.
- **PyWhatKit**: Used to automate WhatsApp message sending.
- **SQLite**: Lightweight database to store user information and bus preferences.
- **HTML/CSS**: For building responsive web interfaces.

## Project Structure

- `app.py`: Main Flask application script that defines routes and handles the web interface.
- `main.py`: Script for processing images, detecting numbers, and sending notifications.
- `templates/`: Contains HTML files for the web interface.
  - `index.html`: Main page for managing contacts.
  - `admin.html`: Admin page to view database entries.
- `static/`: Folder for static files such as CSS and images.
- `contactos.db`: SQLite database storing contacts and their bus preferences.

## Setup and Execution

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/MartimJales/Ambient-Intelligence.git
   ```
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Application**:
   - Start the Flask app:
     ```bash
     python app.py
     ```
   - Run the image processing script:
     ```bash
     python main.py
     ```
4. **Access the Web Interface**:
   - Main page: `http://localhost:5000/`
   - Admin page: `http://localhost:5000/admin/`

## Usage

- **Add Contacts**: Use the main page to input name, phone number, and select bus numbers for which you want to receive alerts.
- **Receive Notifications**: The system continuously monitors incoming images. When a bus number is detected and matches a user's preferences, a WhatsApp message is sent.
- **Admin View**: View all registered contacts and their bus preferences on the admin page.

## Contributions

Contributions are welcome! Feel free to open issues or submit pull requests with improvements or bug fixes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

*Note: This project was developed as part of a study on Ambient Intelligence and its real-world applications.*

