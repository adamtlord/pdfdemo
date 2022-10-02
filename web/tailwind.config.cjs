/** @type {import('tailwindcss').Config} */
const defaultTheme = require('tailwindcss/defaultTheme')

module.exports = {
  content: [
    './index.html'
  ],
  theme: {
    extend: {
      colors: {
        evergreen: '#185e67'
      },
      fontFamily: {
        'sans': ['Lato', ...defaultTheme.fontFamily.sans],
        'serif': ['Libre Baskerville', ...defaultTheme.fontFamily.serif],
      },
    }
  },
  plugins: [
    require('@tailwindcss/forms')
  ]
}