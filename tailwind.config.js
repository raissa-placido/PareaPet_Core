/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/templates/**/*.html"],
  theme: {
    extend: {
      fontFamily: {
        nunito: ["Nunito", "sans-serif"],
        agbalumo: ["Agbalumo", "sans-serif"],
      },
    },
  },
  plugins: [],
};
