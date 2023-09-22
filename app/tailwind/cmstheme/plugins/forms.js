const plugin = require('tailwindcss/plugin')
const colors = require('../colors')
const { borderRadius } = require('../utilities');


const forms = plugin.withOptions(function (options) {
    return function ({ addBase, addComponents, theme }) {
        addComponents({
            '.form-control': {
                'display': 'flex',
                'flex-direction': 'column',
                'margin-bottom': theme("spacing.2"),

                '&.error': {
                    '& > .input': {
                        'outline': 'none',
                        'border-color': theme("colors.error", colors.error),
                    },
                    '& > .help-text': {
                        color: theme("colors.error", colors.error)
                    }
                },
            },
            '.label': {
                'font-size': theme("fontSize.sm"),
                'font-weight': theme("fontWeight.bold"),
                'color': theme("colors.gray.400", colors.gray['400']),
            },
            '.help-text': {
                'font-size': theme("fontSize.sm")
            },
            '.input': {
                'font-size': theme("fontSize.sm"),
                'border-color': theme("colors.gray.100", colors.gray['100']),
                'background-color': theme("colors.gray.50", colors.gray['50']),
                'border-radius': theme("borderRadius.base", borderRadius.base),

                '&:focus': {
                    'box-shadow': 'none',
                    'outline': 'none',
                    'border-color': theme("colors.secondary.bg", colors.secondary.bg)
                }
            },
            '::placeholder': {
                'font-size': theme("fontSize.sm"),
                'color': theme("colors.gray.400", colors.gray['400'])
            }
        })
    }
})

module.exports = forms