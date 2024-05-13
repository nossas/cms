import { CountUp } from './lib/countUp.min.js';

function initializeCounters() {
  document.querySelectorAll(".counterNumber, .counterDate").forEach(counter => {
    const startNum = parseInt(counter.dataset.startNum, 10) || 0;
    const endNum = parseInt(counter.dataset.endNum, 10) || 0;

    const startDate = new Date(counter.dataset.startDate);
    const endDate = new Date(counter.dataset.endDate);
    const diffTime = endDate - startDate;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    const countUp = new CountUp(counter, counter.classList.contains('counterNumber') ? endNum : diffDays, {
      startVal: counter.classList.contains('counterNumber') ? startNum : 0,
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
}

document.addEventListener('DOMContentLoaded', initializeCounters);
document.addEventListener('contentUpdated', initializeCounters);
