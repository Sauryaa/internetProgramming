/* jshint esversion: 8 */
/* jshint browser: true */
'use strict';

var outputScreen;
var clearOnEntry;


/**
 * Display a digit on the `outputScreen`
 * 
 * @param {number} digit digit to add or display on the `outputScreen`
 */
function enterDigit(digit) {
    if (clearOnEntry) {
        outputScreen.textContent = digit;
        clearOnEntry = false;
    } else {
        outputScreen.textContent += digit;
    }
}


/**
 * Clear `outputScreen` and set value to 0
 */
function clear_screen() {
    outputScreen.textContent = "0";
    clearOnEntry = true;
}


/**
 * Evaluate the expression and display its result or *ERROR*
 */
function eval_expr() {
    try {
        const expression = outputScreen.textContent;
        const result = eval(expression);
        if (result == Infinity) {   // Checks for Positive Infinity
            outputScreen.textContent = Infinity;
        }
        else if (isNaN(result) || !isFinite(result)) { // Checks for Not a Number and Negative Infinity
            outputScreen.textContent = "ERROR";
        } else {
            outputScreen.textContent = result;
        }
        clearOnEntry = true;
    } catch (error) {
        outputScreen.textContent = "ERROR";
        clearOnEntry = true;
    }
}


/**
 * Display an operation on the `outputScreen`
 * 
 * @param {string} operation to add to the expression
 */
function enterOp(operation) {
    if (clearOnEntry) {
        outputScreen.textContent = "0" + operation;
    } else {
        outputScreen.textContent += operation;
    }
    clearOnEntry = false;
}


window.onload = function () {
    outputScreen = document.querySelector("#result");
    clearOnEntry = true;
};
