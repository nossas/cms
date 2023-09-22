const plugin = require('tailwindcss/plugin')
const defaultTheme = require('tailwindcss/defaultTheme')
const colors = require('tailwindcss/colors')
const [baseFontSize, { lineHeight: baseLineHeight }] = defaultTheme.fontSize.base


function resolveColor(color, opacityVariableName) {
    return color.replace('<alpha-value>', `var(${opacityVariableName}, 1)`)
}


const button = plugin.withOptions(function (options = { strategy: undefined }) {
    return function ({ addBase, addComponents, theme }) {
        const strategy = options.strategy === undefined ? ['base', 'class'] : [options.strategy]

        const rules = [
            {
                base: [
                    "button"
                ],
                class: [
                    '.btn'
                ],
                styles: {
                    appearance: 'none',
                    border: 'none',
                    'font-size': baseFontSize,
                    'height': defaultTheme.spacing['6'],
                    'line-height': baseLineHeight,
                    'background-color': 'var(--color-primary)',
                    'color': 'var(--color-primary-content)',
                    '&:hover': {
                        'background-color': 'var(--color-primary-hover)',
                    },
                    '&:active:focus': {
                        'background-color': 'var(--color-primary-focus)',
                    },
                    '&-xs': {
                        'font-size': defaultTheme.fontSize.xs[0],
                        'height': defaultTheme.spacing['4'],
                    },
                    '&-sm': {
                        'font-size': defaultTheme.fontSize.sm[0],
                        'height': defaultTheme.spacing['5'],
                    },
                    '&-wide': {
                        'min-width': defaultTheme.spacing['64'],
                    }
                }
            },
            {
                class: ['.btn-secondary'],
                styles: {
                    'background-color': 'var(--color-secondary)',
                    'color': 'var(--color-secondary-content)',
                    '&:hover': {
                        'background-color': 'var(--color-secondary-hover)',
                    },
                    '&:active:focus': {
                        'background-color': 'var(--color-secondary-focus)',
                    }
                }
            },
            {
                class: ['.btn-outline'],
                styles: {
                    'background-color': 'transparent',
                    'border': '1px solid',
                    'border-color': 'var(--color-primary)',
                    'color': 'var(--color-primary)',
                    '&:hover': {
                        'background-color': 'transparent',
                        'color': 'var(--color-primary-hover)',
                        'border-color': 'var(--color-primary-hover)',
                    },
                    '&:active:focus': {
                        'background-color': 'transparent',
                        'color': 'var(--color-primary-focus)',
                        'border-color': 'var(--color-primary-focus)',
                    }
                }
            },
            {
                class: ['.btn-outline.btn-secondary'],
                styles: {
                    'border-color': 'var(--color-secondary)',
                    'color': 'var(--color-secondary)',
                    '&:hover': {
                        'border-color': 'var(--color-secondary-hover)',
                        'color': 'var(--color-secondary-hover)',
                    },
                    '&:active:focus': {
                        'border-color': 'var(--color-secondary-focus)',
                        'color': 'var(--color-secondary-focus)',
                    }
                }
            },
        ]

        const getStrategyRules = (strategy) =>
            rules
                .map((rule) => {
                    if (rule[strategy] === null) return null

                    return { [rule[strategy]]: rule.styles }
                })
                .filter(Boolean)

        if (strategy.includes('base')) {
            addBase(getStrategyRules('base'))
        }

        if (strategy.includes('class')) {
            addComponents(getStrategyRules('class'))
        }
    }
})

module.exports = button