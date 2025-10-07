'use strict';

class View {
    constructor() {
        this.notesContainer = document.getElementById('notes-container');
        this.titleInput = document.getElementById('title');
        this.textInput = document.getElementById('text');
        this.colorSelect = document.getElementById('color');
        this.addNoteButton = document.getElementById('addNote');
        this.fieldTitle = document.getElementById('fieldTitle');
        this.fieldText = document.getElementById('fieldText');
    }

    clearForm() {
        this.titleInput.value = '';
        this.textInput.value = '';
        this.colorSelect.value = 'is-primary';
    }

    showFieldError(fieldId) {
        const field = document.getElementById(fieldId);
        const errorMessage = field.querySelector('.help');
        errorMessage.classList.remove('is-hidden');
    }

    hideFieldError(fieldId) {
        const field = document.getElementById(fieldId);
        const errorMessage = field.querySelector('.help');
        errorMessage.classList.add('is-hidden');
    }

    hideAllErrors() {
        this.hideFieldError('fieldTitle');
        this.hideFieldError('fieldText');
    }

    getFormData() {
        return {
            title: this.titleInput.value.trim(),
            text: this.textInput.value.trim(),
            color: this.colorSelect.value
        };
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleString();
    }

    createNoteHTML(note) {
        const dateStr = this.formatDate(note.date);
        return `
            <article class="message ${note.color} note" data-note-id="${note.id}">
                <div class="message-header">
                    <p>${this.escapeHtml(note.title)}</p>
                    <div class="note-date">${dateStr}</div>
                </div>
                <div class="message-body">
                    <p>${this.escapeHtml(note.text)}</p>
                    <button class="button is-small is-light deleteNote" data-note-id="${note.id}">
                        Delete
                    </button>
                </div>
            </article>
        `;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    getColorDisplayName(colorClass) {
        const colorMap = {
            'is-primary': 'Primary (Blue)',
            'is-link': 'Link (Purple)',
            'is-info': 'Info (Cyan)',
            'is-success': 'Success (Green)',
            'is-warning': 'Warning (Yellow)',
            'is-danger': 'Danger (Red)'
        };
        return colorMap[colorClass] || colorClass;
    }

    renderNotes(notesGrouped) {
        this.notesContainer.innerHTML = '';

        if (Object.keys(notesGrouped).length === 0) {
            this.notesContainer.innerHTML = '<p class="has-text-grey">There are no notes added yet. Add your first note from above!!</p>';
            return;
        }

        const sortedColors = Object.keys(notesGrouped).sort();
        
        sortedColors.forEach(color => {
            const colorGroup = document.createElement('div');
            colorGroup.className = 'color-group';
            
            const groupTitle = document.createElement('h3');
            groupTitle.className = 'subtitle is-4';
            groupTitle.textContent = this.getColorDisplayName(color);
            colorGroup.appendChild(groupTitle);

            const notesInGroup = notesGrouped[color];
            notesInGroup.forEach(note => {
                const noteElement = document.createElement('div');
                noteElement.innerHTML = this.createNoteHTML(note);
                colorGroup.appendChild(noteElement.firstElementChild);
            });

            this.notesContainer.appendChild(colorGroup);
        });
    }

    bindAddNote(handler) {
        this.addNoteButton.addEventListener('click', handler);
    }

    bindDeleteNote(handler) {
        this.notesContainer.addEventListener('click', (e) => {
            if (e.target.classList.contains('deleteNote')) {
                const noteId = parseFloat(e.target.getAttribute('data-note-id'));
                handler(noteId);
            }
        });
    }

    validateForm() {
        const { title, text } = this.getFormData();
        let isValid = true;

        this.hideAllErrors();

        if (!title) {
            this.showFieldError('fieldTitle');
            isValid = false;
        }

        if (!text) {
            this.showFieldError('fieldText');
            isValid = false;
        }

        return isValid;
    }
}
