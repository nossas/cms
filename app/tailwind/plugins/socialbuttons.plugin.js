const plugin = require('tailwindcss/plugin');
const colorFunctions = require('daisyui/src/theming/functions');

const colorProperties = (colorName, theme) => {
    const color = theme("colors." + colorName);
    const colorFocus = colorFunctions.generateDarkenColorFrom(color);
    // const colorContent = colorFunctions.generateForegroundColorFrom(color);

    return {
        'color': 'white',
        'background-color': color,
        '&:hover': {
            'background-color': theme("colors." + colorName + "-focus", "hsl(" + colorFocus + ")")
        }
    }
}

const socialbutton = plugin(({ addUtilities, theme }) => {

    addUtilities({
        '.btn-whatsapp': colorProperties('whatsapp', theme),
        '.btn-facebook': colorProperties('facebook', theme),
        '.btn-twitter': colorProperties('twitter', theme),
        '.btn-copy': colorProperties('copy', theme),
    })
})

module.exports = socialbutton