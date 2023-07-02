// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyAeypkxXo-T8B-6WPDU1X-onaHq4q-PWuM",
  authDomain: "elms-nguyenanhtrong.firebaseapp.com",
  projectId: "elms-nguyenanhtrong",
  storageBucket: "elms-nguyenanhtrong.appspot.com",
  messagingSenderId: "1030761985140",
  appId: "1:1030761985140:web:e03f665dba71ffc67f0d21",
  measurementId: "G-GH5G9QKWBD"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);