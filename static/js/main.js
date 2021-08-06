console.log("Main.js here")




const tagContainer = document.querySelector('.tag-container');

function createTag(label) {
    const div = document.createElement('div');
    div.setAttribute('class', 'tag');
    const span = document.createElement('span');
    span.innerHTML = label;
    const closeBtn = document.createElement('svg');
    closeBtn.setAttribute('class');
    closeBtn.innerHTML('close');

    div.appendChild(span);
    div.appendChild(closeBtn);
    return div
}

tagContainer.appendChild(createTag('testingJava'))