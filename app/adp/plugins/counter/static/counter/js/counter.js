import { CountUp } from './lib/countUp.min.js';

document.querySelectorAll("[data-counter]").forEach(counter => {
  const startNum = parseInt(counter.dataset.counterStart, 10);
  const endNum = parseInt(counter.dataset.counterEnd, 10);

  const countUp = new CountUp(counter, endNum, {
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
});
