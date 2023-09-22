const defaultTheme = require('tailwindcss/defaultTheme')

module.exports = {
    theme: {
        fontFamily: {
            sans: ["Helvetica Neue", "sans-serif"],
        },
        fontSize: {
            'xs': '13px',
            'sm': '16px',
            'base': '18px',
            'lg': '21px',
            'xl': '36px',
            '2xl': '60px',
        },
        spacing: {
            ...defaultTheme.spacing,
            "xs": "36px",
            "sm": "40px",
            "md": "50px",
            "lg": "64px",
        },
        extend: {
            colors: {
                primary: {
                    bg: 'var(--colors-primary-bg)',
                    content: 'var(--colors-primary-content)',
                    hover: 'var(--colors-primary-hover)',
                    focus: 'var(--colors-primary-focus)'
                },
                secondary: {
                    bg: 'var(--colors-secondary-bg)',
                    content: 'var(--colors-secondary-content)',
                    hover: 'var(--colors-secondary-hover)',
                    focus: 'var(--colors-secondary-focus)',
                }
            },
        }
    },
    plugins: [
        require('@tailwindcss/typography'),
        require('@tailwindcss/forms'),
        require('@tailwindcss/aspect-ratio'),
        require('@tailwindcss/container-queries'),
        require("./plugins/typography"),
        require("./plugins/button"),
        require("./plugins/forms"),
    ]
}