"use strict";

document.addEventListener('DOMContentLoaded', function() {
    const getQuestionsBtn = document.getElementById('getQuestionsBtn');
    const categorySelect = document.getElementById('categorySelect');
    const numberInput = document.getElementById('numberInput');
    const numberHelp = document.getElementById('numberHelp');
    const questionsDiv = document.getElementById('questionsDiv');

    getQuestionsBtn.addEventListener('click', handleGetQuestions);

   
    async function handleGetQuestions() {
        const category = categorySelect.value;
        const number = parseInt(numberInput.value);

        questionsDiv.innerHTML = '';
        
        if (!validateInput(number)) {
            return;
        }

        try {
            const questions = await getQuestions(category, number);
            displayQuestions(questionsDiv, questions);
        } catch (error) {
            console.error('Error fetching questions:', error);
            questionsDiv.innerHTML = '<div class="notification is-danger">Error fetching questions. Please try again.</div>';
        }
    }

    /**
     * Validate user input
     * @param {number} number - The number of questions requested
     * @returns {boolean} - Whether the input is valid
     */
    function validateInput(number) {
        numberHelp.textContent = '';
        numberHelp.className = 'help';

        if (!numberInput.value) {
            numberHelp.textContent = 'This field is required';
            numberHelp.className = 'help is-warning';
            return false;
        }

        if (number < 1 || number > 10 || isNaN(number)) {
            numberHelp.textContent = 'Enter a number between 1 and 10';
            numberHelp.className = 'help is-warning';
            return false;
        }

        return true;
    }
});

/**
 * Retrieve questions in the chosen category
 * @param {string} category - The category of questions to retrieve
 * @param {number} number - The number of questions to retrieve
 * @returns {Array} - Array of question objects
 */
async function getQuestions(category, number) {
    const questions = await getData(number, category);
    return questions.results;
}

/**
 * Use fetch to retrieve data from Open Trivia DB
 * 
 * @param {number} chosenNumber - Number of questions to retrieve
 * @param {string} chosenCategory - Category of questions
 * @returns {Object} - JSON response from the API
 */
async function getData(chosenNumber, chosenCategory) {
    const BASE_URL = "https://opentdb.com/api.php?";
    
    const categoryMap = {
        "Science: Computers": 18,
        "Mythology": 20,
        "Geography": 22,
        "History": 23
    };

    const categoryId = categoryMap[chosenCategory];
    const url = `${BASE_URL}amount=${chosenNumber}&category=${categoryId}&type=multiple`;
    
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
        throw error;
    }
}

/**
 * Display the results as Bulma cards
 * 
 * @param {HTMLElement} questionSection - The container element for questions
 * @param {Array} questionPool - Array of question objects
 */
function displayQuestions(questionSection, questionPool) {
    questionPool.forEach((question, index) => {
        const card = createQuestionCard(question, index);
        questionSection.appendChild(card);
    });
}

/**
 * Create a single question card
 * 
 * @param {Object} question - The question object
 * @param {number} index - The index of the question
 * @returns {HTMLElement} - The card element
 */
function createQuestionCard(question, index) {
    const card = document.createElement('div');
    card.className = `card ${question.difficulty}`;
    
    const cardHeader = document.createElement('header');
    cardHeader.className = 'card-header';
    
    const cardHeaderTitle = document.createElement('p');
    cardHeaderTitle.className = 'card-header-title';
    cardHeaderTitle.textContent = decodeHtmlEntities(question.question);
    cardHeader.appendChild(cardHeaderTitle);
    
    const cardContent = document.createElement('div');
    cardContent.className = 'card-content';
    
    const answersList = document.createElement('ol');
    answersList.type = '1';
    
    const allAnswers = [...question.incorrect_answers, question.correct_answer];
    shuffleArray(allAnswers);
    
    allAnswers.forEach(answer => {
        const listItem = document.createElement('li');
        listItem.textContent = decodeHtmlEntities(answer);
        listItem.dataset.answer = answer;
        answersList.appendChild(listItem);
    });
    
    cardContent.appendChild(answersList);
    
    const cardFooter = document.createElement('footer');
    cardFooter.className = 'card-footer';
    
    const categoryP = document.createElement('p');
    categoryP.className = 'card-footer-item';
    categoryP.textContent = question.category;
    cardFooter.appendChild(categoryP);
    
    const difficultyP = document.createElement('p');
    difficultyP.className = 'card-footer-item';
    difficultyP.textContent = question.difficulty.charAt(0).toUpperCase() + question.difficulty.slice(1);
    cardFooter.appendChild(difficultyP);
    
    const revealButtonP = document.createElement('p');
    revealButtonP.className = 'card-footer-item';
    
    const revealButton = document.createElement('button');
    revealButton.className = 'button is-small';
    revealButton.textContent = 'Reveal';
    revealButton.addEventListener('click', () => revealAnswer(card, question.correct_answer));
    
    revealButtonP.appendChild(revealButton);
    cardFooter.appendChild(revealButtonP);
    
    card.appendChild(cardHeader);
    card.appendChild(cardContent);
    card.appendChild(cardFooter);
    
    return card;
}

/**
 * Reveal the correct answer by highlighting it
 * 
 * @param {HTMLElement} card - The card element
 * @param {string} correctAnswer - The correct answer text
 */
function revealAnswer(card, correctAnswer) {
    const answers = card.querySelectorAll('li');
    answers.forEach(answer => {
        if (answer.dataset.answer === correctAnswer) {
            answer.classList.add('correct_answer');
        }
    });
}

/**
 * Decode HTML entities in text
 * 
 * @param {string} text - Text that may contain HTML entities
 * @returns {string} - Decoded text
 */
function decodeHtmlEntities(text) {
    const textarea = document.createElement('textarea');
    textarea.innerHTML = text;
    return textarea.value;
}

/**
 * Shuffle array in place using Fisher-Yates algorithm
 * 
 * @param {Array} array - Array to shuffle
 */
function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}