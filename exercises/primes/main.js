"use strict";

/**
 * Greet user by name
 *
 * @param {string} name visitor's name
 * @param {string} selector element t```o use for display
 */
function greet(name, selector) {
  const element = document.querySelector(selector);
  if (!element) return;
  const params = new URLSearchParams(window.location.search);
  const who = (name && String(name).trim()) || params.get("name") || "student";
  element.textContent = `Hello, ${who}`;
}

/**
 * Check if a number is prime
 *
 * @param {number} number number to check
 * @return {boolean} result of the check
 */
function isPrime(number) {
  if (!Number.isInteger(number) || number < 2) return false;
  if (number === 2) return true;
  if (number % 2 === 0) return false;
  const limit = Math.floor(Math.sqrt(number));
  for (let d = 3; d <= limit; d += 2) {
    if (number % d === 0) return false;
  }
  return true;
}

/**
 * Print whether a number is prime
 *
 * @param {number} number number to check
 * @param {string} selector element to use for display
 */
function printNumberInfo(number, selector) {
  const el = document.querySelector(selector);
  if (!el) return;

  const params = new URLSearchParams(window.location.search);

  let raw = (number !== undefined && number !== null && String(number).trim() !== "")
    ? number
    : params.get("number");

  let n = Number(raw);
  if (!Number.isFinite(n) || n <= 0) n = 330;

  el.textContent = isPrime(n) ? `${n} is a prime number` : `${n} is not a prime number`;
}

/**
 * Generate an array of prime numbers
 *
 * @param {number} number number of primes to generate
 * @return {number[]} an array of `number` prime numbers
 */
function getNPrimes(number) {
  const howMany = Math.max(0, Number(number) || 0);
  const primes = [];
  let candidate = 2;
  while (primes.length < howMany) {
    if (isPrime(candidate)) primes.push(candidate);
    candidate += (candidate === 2) ? 1 : 2;
  }
  return primes;
}

/**
 * Print a table of prime numbers
 *
 * @param {number} number number of primes to display
 * @param {string} selector element to use for display
 */
function printNPrimes(number, selector) {
  const tableBody = document.querySelector(`${selector} tbody`);
  if (!tableBody) return;

  const params = new URLSearchParams(window.location.search);
  
  let raw = (number !== undefined && number !== null && String(number).trim() !== "")
    ? number
    : params.get("number");

  let n = Number(raw);
  if (!Number.isFinite(n) || n <= 0) n = 330;

  tableBody.innerHTML = '';

  const primes = getNPrimes(n);
  let row = null;
  primes.forEach((prime, i) => {
    if (i % 10 === 0) {
      row = document.createElement('tr');
      tableBody.appendChild(row);
    }
    const cell = document.createElement('td');
    cell.textContent = String(prime);
    row.appendChild(cell);
  });
}

/**
 * Display warning about missing URL query parameters
 *
 * @param {Object} urlParams URL parameters
 * @param {string} selector element to use for display
 */
function displayWarnings(urlParams, selector) {
  // TODO: Implement this function
}

window.onload = function () {
  // TODO: Initialize the following variables
  let urlParams = "";
  let name = "";
  let number = "";
  this.displayWarnings(urlParams, "#warnings");
  greet(name, "#greeting");
  printNumberInfo(number, "#numberInfo");
  printNPrimes(number, "table#nPrimes");
};

document.addEventListener("DOMContentLoaded", () => {
  (document.querySelectorAll(".notification .delete") || []).forEach(
    ($delete) => {
      const $notification = $delete.parentNode;

      $delete.addEventListener("click", () => {
        $notification.parentNode.removeChild($notification);
      });
    }
  );
});

module.exports.isPrime = isPrime;
module.exports.getNPrimes = getNPrimes;
