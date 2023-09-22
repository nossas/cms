/** @type {import('tailwindcss').Config} */

module.exports = {
  content: [
    /**
     * HTML. Paths to Django template files that will contain Tailwind CSS classes.
     */

    /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
    // 'templates/**/*.html',

    /*
     * Main templates directory of the project (BASE_DIR/templates).
     * Adjust the following line to match your project structure.
     */
    // '../../templates/**/*.html',

    /*
     * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
     * Adjust the following line to match your project structure.
     */
    '!../admin_styled',
    'templates/storybook/*.html',

    /**
     * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
     * patterns match your project structure.
     */
    /* JS 1: Ignore any JavaScript in node_modules folder. */
    // '!../../**/node_modules',
    /* JS 2: Process all JavaScript files in the project. */
    // '../**/static/**/*.js',

    /**
     * Python: If you use Tailwind CSS classes in Python, uncomment the following line
     * and make sure the pattern below matches your project structure.
     */
    // '../**/*.py'
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Nunito Sans', 'sans-serif'],
        serif: ['Helvetica Neue', 'sans-serif'],
      },
      colors: {
        primary: 'var(--color-primary)',
        secondary: 'var(--color-secondary)',
        'primary-hover': 'var(--color-primary-hover)',
      }
    },
  },
  plugins: [
    require("daisyui"),
    require("./button.plugins")({
      strategy: "class",
    }),
  ]
}

