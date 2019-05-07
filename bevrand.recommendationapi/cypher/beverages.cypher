CREATE (Whiskey:BevGroup {name: "Whiskey"})
CREATE (WhiskeyRye:Beverage {name: "Rye Whiskey", type:"Alcoholic", perc:40, country:"American"})
CREATE (Bourbon:Beverage {name: "Bourbon", type:"Alcoholic", perc:40, country:"American"})
CREATE (Jamesson:Beverage {name: "Jamesson", type:"Alcoholic", perc:40, country:"Irish"})
CREATE (Bunnahabhain:Beverage {name: "Bunnahabhain", type:"Alcoholic", perc:40, country:"Scottish"})
CREATE (Lagavulin:Beverage {name: "Lagavulin", type:"Alcoholic", perc:40, country:"Scottish"})

CREATE (Beer:BevGroup {name:"Beer"})
CREATE (TripleBeer:Beverage {name: "Tripel Beer", type:"Alcoholic", perc:8})
CREATE (Ipa:Beverage {name: "IPA", type:"Alcoholic", perc:6})
CREATE (Guinnesses:Beverage {name: "Guinnesses", type:"Alcoholic", perc:6})
CREATE (FauxBeer:Beverage {name: "Non alcoholic Beer", type:"NonAlcoholic", perc:0})

CREATE (Vodka:Beverage {name:"Vodka", type:"Alcoholic", perc:40})
CREATE (Gin:Beverage {name: "Gin", type:"Alcoholic", perc:40})
CREATE (Kahlua:Beverage {name: "Kahlua", type:"Alcoholic", perc:40})
CREATE (Vermouth:Beverage {name: "Vermouth", type:"Alcoholic", perc:20})
CREATE (VermouthRosso:Beverage {name: "Vermouth Rosso", type:"Alcoholic", perc:20})
CREATE (Campari:Beverage {name: "Campari", type:"Alcoholic", perc:25})
CREATE (Soda:Beverage {name: "Soda Water", type:"NonAlcoholic", perc:0})
CREATE (Prosecco:Beverage {name: "Prosecco", type:"Alcoholic", perc:14})
CREATE (Aperol:Beverage {name: "Aperol", type:"Alcoholic", perc:25})
CREATE (Bitters:Beverage {name: "Angostura Bitters", type:"Alcoholic", perc:44})

CREATE (Champagne:Beverage {name: "Champagne", type:"Alcoholic", perc:14})
CREATE (CremeDeFramboise:Beverage {name: "Creme De Framboise", type:"Alcoholic", perc:25})
CREATE (CremeDeCacao:Beverage {name: "Creme De Cacao", type:"Alcoholic", perc:25})
CREATE (CremeDePeche:Beverage {name: "Creme De Peche", type:"Alcoholic", perc:25})
CREATE (OrangeCuracao:Beverage {name: "Orange Curacao", type:"Alcoholic", perc:25})
CREATE (VermouthSweet:Beverage {name: "Sweet Vermouth", type:"Alcoholic", perc:25})
CREATE (Tequila:Beverage {name: "Tequila", type:"Alcoholic", perc:40})
CREATE (TripelSec:Beverage {name: "Tripel Sec", type:"Alcoholic", perc:25})
CREATE (Rum:Beverage {name: "Rum", type:"Alcoholic", perc:40})
CREATE (DarkRum:Beverage {name: "Dark Rum", type:"Alcoholic", perc:40})
CREATE (Cointreau:Beverage {name: "Cointreau", type:"Alcoholic", perc:35})
CREATE (Galliano:Beverage {name: "Galliano", type:"Alcoholic", perc:40})
CREATE (Cachaca:Beverage {name: "Cachaca", type:"Alcoholic", perc:40})
CREATE (Brandy:Beverage {name: "Brandy", type:"Alcoholic", perc:40})

CREATE (Cream:Beverage {name: "Cream", type:"NonAlcoholic", perc:0})
CREATE (Coke:Beverage {name: "Coke", type:"NonAlcoholic", perc:0})
CREATE (Grenadine:Beverage {name: "Grenadine", type:"NonAlcoholic", perc:0})
CREATE (GingerBeer:Beverage {name: "Ginger Beer", type:"NonAlcoholic", perc:0})
CREATE (TomatoJuice:Beverage {name: "Tomato Juice", type:"NonAlcoholic", perc:0})
CREATE (OrangeJuice:Beverage {name: "Orange Juice", type:"NonAlcoholic", perc:0})
CREATE (CranberryJuice:Beverage {name: "Cranberry Juice", type:"NonAlcoholic", perc:0})
CREATE (Syrup:Beverage {name: "Syrup", type:"NonAlcoholic", perc:0})
CREATE
  (TripleBeer)-[:KIND_OF]->(Beer),
  (Ipa)-[:KIND_OF]->(Beer),
  (FauxBeer)-[:KIND_OF]->(Beer),
  (Guinnesses)-[:KIND_OF]->(Beer)
CREATE
  (Bourbon)-[:KIND_OF]->(Whiskey),
  (WhiskeyRye)-[:KIND_OF]->(Whiskey),
  (Jamesson)-[:KIND_OF]->(Whiskey),
  (Lagavulin)-[:KIND_OF]->(Whiskey),
  (Bunnahabhain)-[:KIND_OF]->(Whiskey)
CREATE (VodkaMartini:Cocktail {name:"Vodka Martini", alcohol:"High"})
CREATE
  (Vodka)-[:PART_OF]->(VodkaMartini),
  (Vermouth)-[:PART_OF]->(VodkaMartini)
CREATE (GinMartini:Cocktail {name:"Gin Martini", alcohol:"High"})
CREATE
  (Gin)-[:PART_OF]->(GinMartini),
  (Vermouth)-[:PART_OF]->(GinMartini)
CREATE (Vesper:Cocktail {name:"Vesper", alcohol:"High"})
CREATE
  (Gin)-[:PART_OF]->(Vesper),
  (Vodka)-[:PART_OF]->(Vesper),
  (Vermouth)-[:PART_OF]->(Vesper)

CREATE (RaspberryMartini:Cocktail {name:"Raspberry Martini", alcohol:"High"})
CREATE
  (Vodka)-[:PART_OF]->(RaspberryMartini),
  (CremeDeFramboise)-[:PART_OF]->(RaspberryMartini),
  (Bitters)-[:PART_OF]->(RaspberryMartini)

CREATE (Cosmopolitan:Cocktail {name:"Cosmopolitan", alcohol:"High"})
CREATE
  (Vodka)-[:PART_OF]->(Cosmopolitan),
  (TripelSec)-[:PART_OF]->(Cosmopolitan),
  (CranberryJuice)-[:PART_OF]->(Cosmopolitan)

CREATE (Daiquiri:Cocktail {name:"Daiquiri", alcohol:"High"})
CREATE
  (Rum)-[:PART_OF]->(Daiquiri),
  (Syrup)-[:PART_OF]->(Daiquiri)

CREATE (Sidecar:Cocktail {name:"Sidecar", alcohol:"High"})
CREATE
  (Brandy)-[:PART_OF]->(Sidecar),
  (Cointreau)-[:PART_OF]->(Sidecar)

CREATE (RobRoy:Cocktail {name:"Rob Roy", alcohol:"High"})
CREATE
  (WhiskeyRye)-[:PART_OF]->(RobRoy),
  (Vermouth)-[:PART_OF]->(RobRoy),
  (VermouthSweet)-[:PART_OF]->(RobRoy),
  (Bitters)-[:PART_OF]->(RobRoy)

CREATE (Margarita:Cocktail {name:"Margarita", alcohol:"High"})
CREATE
  (Tequila)-[:PART_OF]->(Margarita),
  (TripelSec)-[:PART_OF]->(Margarita)

CREATE (HornyToad:Cocktail {name:"Horny Toad", alcohol:"High"})
CREATE
  (Tequila)-[:PART_OF]->(HornyToad),
  (Cointreau)-[:PART_OF]->(HornyToad)

CREATE (Bellini:Cocktail {name:"Bellini", alcohol:"High"})
CREATE
  (CremeDePeche)-[:PART_OF]->(Bellini),
  (Bitters)-[:PART_OF]->(Bellini),
  (Champagne)-[:PART_OF]->(Bellini)

CREATE (Mimosa:Cocktail {name:"Mimosa", alcohol:"High"})
CREATE
  (Champagne)-[:PART_OF]->(Mimosa),
  (OrangeJuice)-[:PART_OF]->(Mimosa)

CREATE (BlackVelvet:Cocktail {name:"Black Velvet", alcohol:"High"})
CREATE
  (Guinnesses)-[:PART_OF]->(BlackVelvet),
  (Champagne)-[:PART_OF]->(BlackVelvet)

CREATE (VodkaCollins:Cocktail {name:"Vodka Collins", alcohol:"High"})
CREATE
  (Vodka)-[:PART_OF]->(VodkaCollins),
  (Syrup)-[:PART_OF]->(VodkaCollins),
  (Soda)-[:PART_OF]->(VodkaCollins)

CREATE (Caipirinha:Cocktail {name:"Caipirinha", alcohol:"Medium"})
CREATE
  (Cachaca)-[:PART_OF]->(Caipirinha),
  (Syrup)-[:PART_OF]->(Caipirinha)

CREATE (Mojito:Cocktail {name:"Mojito", alcohol:"Medium"})
CREATE
  (Rum)-[:PART_OF]->(Mojito),
  (Syrup)-[:PART_OF]->(Mojito),
  (Soda)-[:PART_OF]->(Mojito)

CREATE (MintJulep:Cocktail {name:"Mint Julep", alcohol:"Medium"})
CREATE
  (Bourbon)-[:PART_OF]->(Mojito)

CREATE (DarkAndStormy:Cocktail {name:"Dark And Stormy", alcohol:"Medium"})
CREATE
  (DarkRum)-[:PART_OF]->(DarkAndStormy),
  (GingerBeer)-[:PART_OF]->(DarkAndStormy)

CREATE (CubaLibre:Cocktail {name:"Cube Libre", alcohol:"Medium"})
CREATE
  (Rum)-[:PART_OF]->(CubaLibre),
  (Coke)-[:PART_OF]->(CubaLibre)

CREATE (MoscowMule:Cocktail {name:"Moscow Mule", alcohol:"Medium"})
CREATE
  (Vodka)-[:PART_OF]->(MoscowMule),
  (GingerBeer)-[:PART_OF]->(MoscowMule)

CREATE (MaiTai:Cocktail {name:"Mai Tai", alcohol:"High"})
CREATE
  (DarkRum)-[:PART_OF]->(MaiTai),
  (OrangeCuracao)-[:PART_OF]->(MaiTai),
  (Brandy)-[:PART_OF]->(MaiTai),
  (Bitters)-[:PART_OF]->(MaiTai),
  (Syrup)-[:PART_OF]->(MaiTai)

CREATE (TequilaSunrise:Cocktail {name:"Tequila Sunrise", alcohol:"Medium"})
CREATE
  (Tequila)-[:PART_OF]->(TequilaSunrise),
  (OrangeJuice)-[:PART_OF]->(TequilaSunrise),
  (Grenadine)-[:PART_OF]->(TequilaSunrise)

CREATE (HarveyWallbanger:Cocktail {name:"Harvey Wallbanger", alcohol:"Medium"})
CREATE
  (Galliano)-[:PART_OF]->(HarveyWallbanger),
  (OrangeJuice)-[:PART_OF]->(HarveyWallbanger),
  (Vodka)-[:PART_OF]->(HarveyWallbanger)

CREATE (BrandyAlexander:Cocktail {name:"Brandy Alexander", alcohol:"High"})
CREATE
  (Brandy)-[:PART_OF]->(BrandyAlexander),
  (CremeDeCacao)-[:PART_OF]->(BrandyAlexander),
  (Cream)-[:PART_OF]->(BrandyAlexander)

CREATE (BloodyMary:Cocktail {name:"Bloody Mary", alcohol:"Medium"})
CREATE
  (Vodka)-[:PART_OF]->(BloodyMary),
  (TomatoJuice)-[:PART_OF]->(BloodyMary)

CREATE (LongIslandIcedTea:Cocktail {name:"Long Island Iced Tea", alcohol:"High"})
CREATE
  (Vodka)-[:PART_OF]->(LongIslandIcedTea),
  (Rum)-[:PART_OF]->(LongIslandIcedTea),
  (Gin)-[:PART_OF]->(LongIslandIcedTea),
  (Tequila)-[:PART_OF]->(LongIslandIcedTea),
  (TripelSec)-[:PART_OF]->(LongIslandIcedTea),
  (Syrup)-[:PART_OF]->(LongIslandIcedTea),
  (Coke)-[:PART_OF]->(LongIslandIcedTea)

CREATE (WhiteRussian:Cocktail {name:"White Russian", alcohol:"High"})
CREATE
  (Vodka)-[:PART_OF]->(WhiteRussian),
  (Kahlua)-[:PART_OF]->(WhiteRussian),  
  (Cream)-[:PART_OF]->(WhiteRussian)

CREATE (Negroni:Cocktail {name:"Negroni", alcohol:"High"})
CREATE
  (Gin)-[:PART_OF]->(Negroni),
  (Campari)-[:PART_OF]->(Negroni),  
  (VermouthRosso)-[:PART_OF]->(Negroni)

CREATE (Spritz:Cocktail {name:"Spritz Veneziano", alcohol:"Medium"})
CREATE
  (Aperol)-[:PART_OF]->(Spritz),
  (Prosecco)-[:PART_OF]->(Spritz),  
  (Soda)-[:PART_OF]->(Spritz)

CREATE (SpritzCampari:Cocktail {name:"Spritz Veneziano con Campari", alcohol:"Medium"})
CREATE
  (Campari)-[:PART_OF]->(SpritzCampari),
  (Prosecco)-[:PART_OF]->(SpritzCampari),  
  (Soda)-[:PART_OF]->(SpritzCampari)

CREATE (Manhattan:Cocktail {name:"Manhattan", alcohol:"High"})
CREATE
  (WhiskeyRye)-[:PART_OF]->(Manhattan),
  (VermouthRosso)-[:PART_OF]->(Manhattan),  
  (Bitters)-[:PART_OF]->(Manhattan)

CREATE (OldFashioned:Cocktail {name:"Old Fashioned", alcohol:"Medium"})
CREATE
  (Bourbon)-[:PART_OF]->(OldFashioned),  
  (Bitters)-[:PART_OF]->(OldFashioned);