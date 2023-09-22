const plugin = require('tailwindcss/plugin')
const colors = require('../colors');


const typography = plugin.withOptions(function (options) {
    return function ({ addBase, addComponents, theme }) {
        // Define text implements
        addBase({
            h1: {
                "font-size": theme("fontSize.2xl"),
                "font-weight": theme("fontWeight.bold")
            },
            h2: {
                "font-size": theme("fontSize.xl"),
                "font-weight": theme("fontWeight.bold")
            },
            h3: {
                "font-size": theme("fontSize.lg"),
                "font-weight": theme("fontWeight.bold")
            },
            h4: {
                "font-size": theme("fontSize.base")
            },
            h5: {
                "font-size": theme("fontSize.sm"),
                "font-weight": theme("fontWeight.bold")
            }
        })

        addComponents({
            '.text': {
                '&-primary': {
                    'color': theme("colors.primary.bg", colors.primary.bg)
                },
                '&-secondary': {
                    'color': theme("colors.secondary.bg", colors.secondary.bg)
                }
            }
        })
    }
})

module.exports = typography