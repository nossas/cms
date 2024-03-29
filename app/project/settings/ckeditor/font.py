# Configurações para estilos de font e tamanhos
# https://github.com/ckeditor/ckeditor4/tree/master/plugins/font

# Fonts Google
# https://fonts.googleapis.com/css?family=Abel|Anton|Archivo+Narrow:400,400i,700,700i|Arvo:400,400i,700,700i|Asap:400,400i,700,700i|Baloo+Bhai|Bebas+Neue|Bitter:400,400i,700|Bree+Serif|Cabin:400,400i,700,700i|Catamaran:400,700|Crimson+Text:400,400i,700,700i|Cuprum:400,400i,700,700i|David+Libre:400,700|Dosis:400,700|Droid+Sans:400,700|Exo+2:400,400i,700,700i|Exo:400,400i,700,700i|Fira+Sans:400,400i,700,700i|Fjalla+One|Francois+One|Gidugu|Hind:400,700|Inconsolata:400,700|Indie+Flower|Josefin+Sans:400,400i,700,700i|Karla:400,400i,700,700i|Lalezar|Lato:400,400i,700,700i|Libre+Baskerville:400,400i,700|Lobster|Lora:400,400i,700,700i|Merriweather+Sans:400,400i,700,700i|Montserrat:400,700|Muli:400,400i|Noto+Serif:400,400i,700,700i|Nunito+Sans:400,700,800|Open+Sans+Condensed:300,300i,700|Open+Sans:400,400i,700,700i|Oswald:400,700|Oxygen:400,700|PT+Sans:400,400i,700,700i|PT+Serif:400,400i,700,700i|Pacifico|Playfair+Display:400,400i,700,700i|Poiret+One|Poppins:400,700|Quicksand:400,700|Raleway:400,400i,700,700i|Roboto+Condensed:400,400i,700,700i|Roboto+Mono:400,400i,700,700i|Roboto+Slab:400,700|Roboto:400,400i,700,700i|Ruslan+Display|Signika:400,700|Slabo+27px|Source+Sans+Pro:200,300,400,700|Titillium+Web:400,400i,700,700i|Ubuntu+Condensed|Ubuntu:400,400i,700,700i|Varela+Round|Yanone+Kaffeesatz:400,700&display=swap

font_family_options = [
    "Abel",
    "Anton",
    "Archivo Narrow",
    "Arvo",
    "Asap",
    "Baloo Bhai",
    "Bebas Neue Pro",
    "Bitter",
    "Bree Serif",
    "Capriola",
    "Cabin",
    "Catamaran",
    "Crimson Text",
    "Cuprum",
    "David Libre",
    "Dosis",
    "Droid Sans",
    "Exo",
    "Exo 2",
    "Fira Sans",
    "Fjalla One",
    "Francois One",
    "Gidugu",
    "Hind",
    "Inconsolata",
    "Indie Flower",
    "Josefin Sans",
    "Karla",
    "Lalezar",
    "Lato",
    "Libre Baskerville",
    "Lobster",
    "Lora",
    "Merriweather Sans",
    "Montserrat",
    "Muli",
    "Noto Serif",
    "Nunito Sans",
    "Open Sans",
    "Open Sans Condensed",
    "Oswald",
    "Oxygen",
    "PT Sans",
    "PT Serif",
    "Pacifico",
    "Playfair Display",
    "Poiret One",
    "Poppins",
    "Quicksand",
    "Raleway",
    "Roboto",
    "Roboto Condensed",
    "Roboto Mono",
    "Roboto Slab",
    "Ruslan Display",
    "Signika",
    "Slabo 27px",
    "Source Sans Pro",
    "Titillium Web",
    "Ubuntu",
    "Ubuntu Condensed",
    "Varela Round",
    "Yanone Kaffeesatz",
]


config = {
    "extraPlugins": "font",
    "font_names": ";".join(font_family_options),
    "fontSize_sizes": ";".join([
        '14/14px',
        '16/16px',
        '18/18px',
        '20/20px',
        '22/22px',
        '24/24px',
        '26/26px',
        '28/28px',
        '36/36px',
        '48/48px',
        '56/56px',
        '64/64px',
        '72/72px',
    ])
}
