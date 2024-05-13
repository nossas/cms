import { CountUp } from './lib/countUp.min.js';

document.addEventListener('DOMContentLoaded', function() {
  const counterNumber = document.getElementById("counterNumber");
  const daysLeftElement = document.getElementById("counterDate");

  // Animação numérica
  if (counterNumber.dataset.startNum || counterNumber.dataset.endNum) {
    const startNum = parseInt(counterNumber.dataset.startNum, 10);
    const endNum = parseInt(counterNumber.dataset.endNum, 10);

    const countUp = new CountUp(counterNumber, endNum, {
      startVal: startNum,
      decimalPlaces: 0,
      duration: 2,
      useEasing: true,
    });

    if (!countUp.error) {
      countUp.start();
    } else {
      console.error(countUp.error);
    }
  }

  // Contagem regressiva de dias
  if (daysLeftElement.dataset.startDate && daysLeftElement.dataset.endDate) {
    const startDate = new Date(daysLeftElement.dataset.startDate);
    const endDate = new Date(daysLeftElement.dataset.endDate);
    const diffTime = Math.abs(endDate - startDate);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    const countUp = new CountUp(daysLeftElement, diffDays, {
      startVal: 0,
      decimalPlaces: 0,
      duration: 2,
      useEasing: true,
    });

    if (!countUp.error) {
      countUp.start();
    } else {
      console.error(countUp.error);
    }
  }
});
