const addHistoryToBeverage = (beverageArray, redisHistory) => {
  return beverageArray.map(beverage => {
    let matchedBeverage;
    //If statement needed, because find can't be used on empty arrays
    if(redisHistory.length != 0){
      matchedBeverage = redisHistory.find(history => {
        return history.drink === beverage;
      });
    }
    const rolled = matchedBeverage ? matchedBeverage.rolled : 0;
    return { drink: beverage, rolled: rolled};
  });
}

const mergeHistoryWithBeverage = (beverageObjectArray, redisHistory) => {
  const beverageArray = beverageObjectArray.map(elem => {
    return elem.drink;
  });
  return addHistoryToBeverage(beverageArray, redisHistory);
}

module.exports = {
  addHistoryToBeverage: addHistoryToBeverage,
  mergeHistoryWithBeverage: mergeHistoryWithBeverage
}