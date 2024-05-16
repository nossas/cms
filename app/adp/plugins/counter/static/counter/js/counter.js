import { CountUp } from './lib/countUp.min.js';

document.querySelectorAll("[data-counter]").forEach(counter => {
  const initialNumber = parseInt(counter.dataset.counterInitial, 10);
  const targetNumber = parseInt(counter.dataset.counterTarget, 10);

  const countUp = new CountUp(counter, targetNumber, {
    startVal: initialNumber,
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
