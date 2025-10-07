'use strict';

class Controller {
    constructor(model, view) {
        this.model = model;
        this.view = view;
        
        this.view.bindAddNote(this.handleAddNote.bind(this));
        this.view.bindDeleteNote(this.handleDeleteNote.bind(this));
        
        this.renderNotes();
    }

    handleAddNote() {
        if (!this.view.validateForm()) {
            return;
        }

        const { title, text, color } = this.view.getFormData();

        this.model.addNote(title, text, color);

        this.view.clearForm();

        this.renderNotes();
    }

    handleDeleteNote(noteId) {
        this.model.removeNote(noteId);
        this.renderNotes();
    }

    renderNotes() {
        const notesGrouped = this.model.getNotesGroupedByColor();
        this.view.renderNotes(notesGrouped);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const model = new Model();
    const view = new View();
    const controller = new Controller(model, view);
});
