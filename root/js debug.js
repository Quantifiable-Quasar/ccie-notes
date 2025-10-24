// This is a test script to debug runOnNoteCreation
const newNote = api.originEntity;

// Log to the console that the script has started
api.log(`SCRIPT: runOnNoteCreation triggered for note: ${newNote.title}`);
api.log(`SCRIPT: Note type is: ${newNote.type}`);
api.log(`SCRIPT: Note content is: '${newNote.getContent()}'`);

// Check for default new note content, which is usually <p></p>
if (newNote.type === 'text' && newNote.getContent().trim() === '<p></p>') {
    api.log(`SCRIPT: Condition MET. Attempting to set content...`);
    
    try {
        newNote.setContent("<h1>Test was successful</h1>");
        api.log(`SCRIPT: setContent successful.`);
    } catch (e) {
        api.log(`SCRIPT ERROR: ${e.message}`);
    }

} else {
    api.log(`SCRIPT: Condition NOT MET. Note was not a blank text note.`);
}


const newNote = api.originEntity;

if (newNote.type === 'text') {
    const now = api.dayjs().format("YYYY-MM-DD HH:mm:ss Z");
    const frontmatter = `<pre>---
        layout: post
        title: ${newNote.title}
        date: ${now}
        categories: []
        tags: []
        ---
        </pre>`;
    newNote.setContent(frontmatter);
    }