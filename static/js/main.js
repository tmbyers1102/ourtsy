console.log("Main.js here")
console.log('share button connected to JS');

// Share Button on Posts

const shareBtn = document.querySelector('.share-btn');
const shareOptions = document.querySelector('.share-options');


shareBtn.addEventListener('click', () => {
    shareOptions.classList.toggle('active');
})



// Share Button on Posts END




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


// share button copied animation

// const linkButton = document.querySelector('linkButton');


// share button copied animation END