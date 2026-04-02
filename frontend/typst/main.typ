#set page(
  fill:black,
  width: auto,
  height: auto,
  margin: 1pt
)
#let symbols = (
  heart: "♥",
  spade: "♠",
  diamond: "♦",
  club: "♣",
)
#let grey = rgb("#77797d").lighten(5%)
#let colors = ( //gpt wrote this part btw,i dont wanna type in a buncha colors
  sage:     rgb("#8a9a5b"), // A soft, earthy green
  dusty-blue: rgb("#5d8aa8"), // A calm, greyish blue
  terracotta: rgb("#c04000").lighten(35%),
  slate:    rgb("#708090"), // A balanced blue-grey
  lavender: rgb("#967bb6"), // A soft, pale purple
)

#let symbol_list = symbols.values()
#let colors_list = colors.values()

#let place_symbols(sym,rand_color) = {
    let inner_symbol = text(stroke:0.1pt,size:15pt,fill:rand_color)[#sym]
    align(top+left,inner_symbol)
    align(bottom+right,rotate(180deg,inner_symbol))
}
#let card_margin(symbols:sym,rand_color) ={
    rect(
      radius:5%,
      width:45pt,
      height:70pt,
      stroke:(paint:grey,thickness:0.7pt)
      )[#place_symbols(symbols,rand_color)]
    }
#grid(
  columns:(20),
  gutter: 5pt,
  ..range(220).flatten().map(i => card_margin(symbols:symbol_list.at(calc.rem(int(i*2+i/3), 4)),colors_list.at(calc.rem(int(i/1.5),5))))
)
