/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        cyber: {
          bg: "#050816",
          panel: "#0b1224",
          accent: "#00e5ff",
          danger: "#ff4d6d",
          safe: "#2dd4bf"
        }
      },
      boxShadow: {
        glow: "0 0 20px rgba(0, 229, 255, 0.25)"
      }
    }
  },
  plugins: []
};