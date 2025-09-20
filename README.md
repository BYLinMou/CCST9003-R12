# Sun Bus - Smart Seat Recommendation System

This project is a web-based Smart Seat Recommendation System for bus passengers. It helps users find the best seat based on their sunlight preference and allows qualified users to reserve seats with possible fee waivers.

## Features

- **Smart Seat Recommendation:** Suggests the best seat (left/right) based on sunlight exposure for your selected route and time.
- **User Authentication:** Login system with user data stored in `userData.json`.
- **Seat Reservation:** Qualified users can reserve seats and may receive a fee waiver.
- **Search History:** Logged-in users can view their past search and reservation history.
- **Profile Management:** Users can view their profile, upload qualification documents, and log out.
- **Responsive Design:** Mobile-friendly interface with bottom navigation.

## Project Structure

- `index.html` - Home page
- `search.html` - Search for bus routes and seat recommendations
- `results.html` - Displays seat recommendation results
- `reserve.html` - Seat reservation page (login required)
- `reserve_success.html` - Reservation confirmation
- `profile.html` - User profile and qualification upload
- `history.html` - Search and reservation history (login required)
- `anonymous.html` - Shown to users not logged in
- `login.html` - Login page
- `login.js` - Authentication logic
- `userData.json` - Sample user data and qualifications
- `style.css` - Main stylesheet
- `user.jpeg`, `user.png` - Sample user profile images

## Getting Started

You can try out the app directly online:

- **Live Demo:** [https://bylinmou.github.io/CCST9003-R12/](https://bylinmou.github.io/CCST9003-R12/)

Or run it locally:
1. Clone or download this repository.
2. Open `index.html` in your browser to start using the app.

## Test Accounts

You can use the following test accounts to log in and try out the app:

- **Email:** qualified@test.com / **Password:** test123 (qualified for fee waiver)
- **Email:** unqualified@test.com / **Password:** test456

## Notes

- This project is a prototype and uses static files for demonstration.
- User data and authentication are handled on the client side for demo purposes only.
- No backend server is required.

## License

This project is for educational purposes.
