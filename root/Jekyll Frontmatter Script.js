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