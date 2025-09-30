/* jshint esversion: 8 */
/* jshint browser: true */
"use strict;";

var team = ["Aardvark", "Beaver", "Cheetah", "Dolphin", "Elephant", "Flamingo", "Giraffe", "Hippo"];
var priority = ["Low", "Normal", "Important", "Critical"];

/**
 * Add a new task to the list
 * 
 * Validate form, collect input values, and add call `addRow` to add a new row to the table
 */
function addTask() {
    let title = document.getElementById("title").value.trim();
    let assignedTo = document.getElementById("assignedTo").value;
    let priority = document.getElementById("priority").value;
    let dueDate = document.getElementById("dueDate").value;
    
    let titleValid = title !== "";
    let dueDateValid = dueDate !== "";
    
    let titleHelp = document.querySelector("#taskTitleText > p");
    let dueDateHelp = document.querySelector("#taskDueDate > p");
    
    if (titleValid) {
        titleHelp.className = "help";
    } else {
        titleHelp.className = "help is-danger";
    }
    
    if (dueDateValid) {
        dueDateHelp.className = "help";
    } else {
        dueDateHelp.className = "help is-danger";
    }
    
    if (titleValid && dueDateValid) {
        let vals = [title, assignedTo, priority, dueDate];
        addRow(vals, document.querySelector("#taskList tbody"));
        
        document.getElementById("title").value = "";
        document.getElementById("dueDate").value = "";
    }
}

/**
 * Add a new row to the table
 * 
 * @param {string[]} valueList list of task attributes
 * @param {Object} parent DOM node to append to
 */
function addRow(valueList, parent) {
    // TODO: Implement this function
    let row = document.createElement("tr");
    
    let priority = valueList[2].toLowerCase();
    row.className = priority;
    
    let checkboxCell = document.createElement("td");
    let cb = document.createElement("input");
    cb.type = "checkbox";
    cb.onclick = removeRow;
    checkboxCell.appendChild(cb);
    row.appendChild(checkboxCell);
    
    let titleCell = document.createElement("td");
    titleCell.textContent = valueList[0];
    row.appendChild(titleCell);
    
    let assignedCell = document.createElement("td");
    assignedCell.textContent = valueList[1];
    row.appendChild(assignedCell);
    
    let priorityCell = document.createElement("td");
    priorityCell.textContent = valueList[2];
    row.appendChild(priorityCell);
    
    let dueDateCell = document.createElement("td");
    dueDateCell.textContent = valueList[3];
    row.appendChild(dueDateCell);

    parent.appendChild(row);
}

/**
 * Remove a table row corresponding to the selected checkbox
 * 
 */
function removeRow() {
    // TODO: Implement this function
    setTimeout(() => {
        let row = this.closest("tr");
        if (row) {
            row.remove();
        }
    }, 3000);
}

/**
 * Remove all table rows
 * 
 */
function selectAll() {
    let checkboxes = document.querySelectorAll("#taskList tbody input[type='checkbox']");
    
    checkboxes.forEach(checkbox => {
        checkbox.checked = true;
        removeRow.call(checkbox);
    });
}

/**
 * Add options to the specified element
 * 
 * @param {string} selectId `select` element to populate
 * @param {string[]} sList array of options
 */
function populateSelect(selectId, sList) {
    // TODO: Implement this function
    let sel = document.getElementById(selectId);
    for (let i = 0; i < sList.length; i++) {
        let option = document.createElement("option");
        option.value = sList[i];
        option.text = sList[i];
        sel.appendChild(option);
    }
}

window.onload = function () {
    populateSelect("assignedTo", team);
    populateSelect("priority", priority);
};
