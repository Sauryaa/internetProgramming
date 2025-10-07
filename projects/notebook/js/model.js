'use strict';

class Model {
    constructor() {
        this.notes = [];
        this.loadNotes();
    }

    loadNotes() {
        try {
            const storedNotes = localStorage.getItem('notebook-notes');
            if (storedNotes) {
                this.notes = JSON.parse(storedNotes);
            }
        } catch (error) {
            console.error('Error loading notes from localStorage:', error);
            this.notes = [];
        }
    }

    saveNotes() {
        try {
            localStorage.setItem('notebook-notes', JSON.stringify(this.notes));
        } catch (error) {
            console.error('Error saving notes to localStorage:', error);
        }
    }

    addNote(title, text, color) {
        const note = {
            id: Date.now() + Math.random(),
            title: title,
            text: text,
            color: color,
            date: new Date().toISOString()
        };
        
        this.notes.push(note);
        this.saveNotes();
        return note;
    }

    removeNote(id) {
        this.notes = this.notes.filter(note => note.id !== id);
        this.saveNotes();
    }

    getAllNotes() {
        return this.notes;
    }

    getNotesGroupedByColor() {
        const grouped = {};
        
        this.notes.forEach(note => {
            if (!grouped[note.color]) {
                grouped[note.color] = [];
            }
            grouped[note.color].push(note);
        });

        Object.keys(grouped).forEach(color => {
            grouped[color].sort((a, b) => new Date(b.date) - new Date(a.date));
        });

        return grouped;
    }
}
