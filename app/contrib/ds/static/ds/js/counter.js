import { CountUp } from './lib/countUp.min.js';

document.addEventListener('DOMContentLoaded', function() {
  function activateCountUp(selector) {
    const element = document.querySelector(selector);
    const startNum = parseInt(element.getAttribute('data-start-num'), 10);
    const endNum = parseInt(element.getAttribute('data-end-num'), 10);

    const countUp = new CountUp(element, endNum, {
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

  activateCountUp('#counter');
});
