const plugin = require('tailwindcss/plugin')
const colors = require('../colors');
const { borderRadius } = require('../utilities');


const button = plugin.withOptions(function (options) {
    return function ({ addBase, addComponents, theme }) {
        // Define text implements
        addComponents({
            '.btn': {
                'display': 'flex',
                'align-items': 'center',
                'justify-content': 'center',
                'height': theme("spacing.md"),
                'background-color': theme("colors.primary.bg", colors.primary.bg),
                'color': theme("colors.primary.content", colors.primary.content),
                'padding': '15px 25px',
                'border-radius': theme("borderRadius.base", borderRadius.base),
                'font-weight': theme("fontWeight.bold"),
                'text-transform': 'uppercase',

                '&-sm': {
                    'font-size': theme("fontSize.sm"),
                    'height': theme("spacing.sm"),
                },
                '&-xs': {
                    'font-size': theme("fontSize.xs"),
                    'height': theme("spacing.xs"),
                },
                '&-wide': {
                    'min-width': '330px',
                },

                '&:hover': {
                    'background-color': theme("colors.primary.hover", colors.primary.hover),
                },
                '&:active:focus': {
                    'background-color': theme("colors.primary.focus", colors.primary.focus),
                },

                '&-secondary': {
                    'background-color': theme("colors.secondary.bg", colors.secondary.bg),

                    '&:hover': {
                        'background-color': theme("colors.secondary.hover", colors.secondary.hover),
                    },
                    '&:active:focus': {
                        'background-color': theme("colors.secondary.focus", colors.secondary.focus),
                    }
                },

                '&-outline': {
                    'background-color': `${theme("colors.transparent", colors.transparent)} !important`,
                    'border': `1px solid ${theme("colors.primary.bg", colors.primary.bg)}`,
                    'color': theme("colors.primary.bg", colors.primary.bg),

                    '&:hover': {
                        'color': theme("colors.primary.hover", colors.primary.hover),
                        'border-color': theme("colors.primary.hover", colors.primary.hover),
                    },
                    '&:active:focus': {
                        'color': theme("colors.primary.focus", colors.primary.focus),
                        'border-color': theme("colors.primary.focus", colors.primary.focus),
                    },

                    "&.btn-secondary": {
                        '&:hover': {
                            'border-color': theme("colors.secondary.hover", colors.secondary.hover),
                        },
                        '&:active:focus': {
                            'border-color': theme("colors.secondary.focus", colors.secondary.focus),
                        }
                    }
                },
            }
        })
    }
})

module.exports = button