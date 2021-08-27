// multi-part form start

const slidePage = document.querySelector(".slide-page");
// 1st slide -- intro, agreement
const agreeCheckBox = document.getElementById("agreementCheckBox");
const nextBtnFirst = document.querySelector(".firstNext");
// 2nd slide -- Photos
const prevBtnSec = document.querySelector(".prev-1");
const nextBtnSec = document.querySelector(".next-1");
// 3rd slide --title, price, story
const artTitle = document.getElementById("artTitle");
const artPrice = document.getElementById("artPrice");
const artStory = document.getElementById("artStory");

const prevBtnThird = document.querySelector(".prev-2");
const nextBtnThird = document.querySelector(".next-2");
// 4th slide -- tags, medium, communities, genres
const prevBtnFourth = document.querySelector(".prev-3");
const submitBtn = document.querySelector(".submit");

const progressText = document.querySelectorAll(".step p");
const progressCheck = document.querySelectorAll(".step .check");
const bullet = document.querySelectorAll(".step .bullet");
let current = 1;

// this checks to see if title, price, and story are filled for next slide button
artTitle.addEventListener('keyup', (e) =>{
  console.log(e.currentTarget.value);
  const valueTitle = e.currentTarget.value;
  artPrice.addEventListener('keyup', (e) =>{
    console.log(e.currentTarget.value);
    const valuePrice = e.currentTarget.value;
    artStory.addEventListener('keyup', (e) =>{
      console.log(e.currentTarget.value);
      const valueStory = e.currentTarget.value;
      nextBtnThird.hidden = false;
      if (valueStory === "" || valuePrice === "" || valueTitle === "") {
        nextBtnThird.hidden = true;
      }
    });
  });
});





// this checks to see if agreement box is checked to offer next slide button
agreeCheckBox.addEventListener('change', (e) =>{
  console.log(e.target.checked);
  const value = e.target.checked;
  nextBtnFirst.hidden = true;
  nextBtnFirst.disabled = true;
  if (value == true) {
    nextBtnFirst.hidden = false;
    nextBtnFirst.disabled = false;
  }
});



nextBtnFirst.addEventListener("click", function(event){
  event.preventDefault();
  slidePage.style.marginLeft = "-25%";
  bullet[current - 1].classList.add("active");
  progressCheck[current - 1].classList.add("active");
  progressText[current - 1].classList.add("active");
  current += 1;
});
nextBtnSec.addEventListener("click", function(event){
  event.preventDefault();
  slidePage.style.marginLeft = "-50%";
  bullet[current - 1].classList.add("active");
  progressCheck[current - 1].classList.add("active");
  progressText[current - 1].classList.add("active");
  current += 1;
});
nextBtnThird.addEventListener("click", function(event){
  event.preventDefault();
  slidePage.style.marginLeft = "-75%";
  bullet[current - 1].classList.add("active");
  progressCheck[current - 1].classList.add("active");
  progressText[current - 1].classList.add("active");
  current += 1;
});
submitBtn.addEventListener("click", function(){
  bullet[current - 1].classList.add("active");
  progressCheck[current - 1].classList.add("active");
  progressText[current - 1].classList.add("active");
  current += 1;
  setTimeout(function(){
    alert("Your Form Successfully Signed up");
    location.reload();
  },800);
});
prevBtnSec.addEventListener("click", function(event){
  event.preventDefault();
  slidePage.style.marginLeft = "0%";
  bullet[current - 2].classList.remove("active");
  progressCheck[current - 2].classList.remove("active");
  progressText[current - 2].classList.remove("active");
  current -= 1;
});
prevBtnThird.addEventListener("click", function(event){
  event.preventDefault();
  slidePage.style.marginLeft = "-25%";
  bullet[current - 2].classList.remove("active");
  progressCheck[current - 2].classList.remove("active");
  progressText[current - 2].classList.remove("active");
  current -= 1;
});
prevBtnFourth.addEventListener("click", function(event){
  event.preventDefault();
  slidePage.style.marginLeft = "-50%";
  bullet[current - 2].classList.remove("active");
  progressCheck[current - 2].classList.remove("active");
  progressText[current - 2].classList.remove("active");
  current -= 1;
});

// multi-part form end

// multi-image upload start

    const fileTempl = document.getElementById("file-template"),
      imageTempl = document.getElementById("image-template"),
      empty = document.getElementById("empty");
    
    // use to store pre selected files
    let FILES = {};
    
    // check if file is of type image and prepend the initialied
    // template to the target element
    function addFile(target, file) {
      const isImage = file.type.match("image.*"),
        objectURL = URL.createObjectURL(file);
    
      const clone = isImage
        ? imageTempl.content.cloneNode(true)
        : fileTempl.content.cloneNode(true);
    
      clone.querySelector("h1").textContent = file.name;
      clone.querySelector("li").id = objectURL;
      clone.querySelector(".delete").dataset.target = objectURL;
      clone.querySelector(".size").textContent =
        file.size > 1024
          ? file.size > 1048576
            ? Math.round(file.size / 1048576) + "mb"
            : Math.round(file.size / 1024) + "kb"
          : file.size + "b";
    
      isImage &&
        Object.assign(clone.querySelector("img"), {
          src: objectURL,
          alt: file.name
        });
    
      empty.classList.add("hidden");
      target.prepend(clone);
    
      FILES[objectURL] = file;
    }
    
    const gallery = document.getElementById("gallery"),
      overlay = document.getElementById("overlay");
    
    // click the hidden input of type file if the visible button is clicked
    // and capture the selected files
    const hidden = document.getElementById("hidden-input");
    document.getElementById("button").onclick = () => hidden.click();
    hidden.onchange = (e) => {
      for (const file of e.target.files) {
        addFile(gallery, file);
      }
    };
    
    // use to check if a file is being dragged
    const hasFiles = ({ dataTransfer: { types = [] } }) =>
      types.indexOf("Files") > -1;
    
    // use to drag dragenter and dragleave events.
    // this is to know if the outermost parent is dragged over
    // without issues due to drag events on its children
    let counter = 0;
    
    // reset counter and append file to gallery when file is dropped
    function dropHandler(ev) {
      ev.preventDefault();
      for (const file of ev.dataTransfer.files) {
        addFile(gallery, file);
        overlay.classList.remove("draggedover");
        counter = 0;
      }
    }
    
    // only react to actual files being dragged
    function dragEnterHandler(e) {
      e.preventDefault();
      if (!hasFiles(e)) {
        return;
      }
      ++counter && overlay.classList.add("draggedover");
    }
    
    function dragLeaveHandler(e) {
      1 > --counter && overlay.classList.remove("draggedover");
    }
    
    function dragOverHandler(e) {
      if (hasFiles(e)) {
        e.preventDefault();
      }
    }
    
    // event delegation to caputre delete events
    // fron the waste buckets in the file preview cards
    gallery.onclick = ({ target }) => {
      if (target.classList.contains("delete")) {
        const ou = target.dataset.target;
        document.getElementById(ou).remove(ou);
        gallery.children.length === 1 && empty.classList.remove("hidden");
        delete FILES[ou];
      }
    };
    
    // print all selected files
    document.getElementById("submit").onclick = () => {
      alert(`Submitted Files:\n${JSON.stringify(FILES)}`);
      console.log(FILES);
    };
    
    // clear entire selection
    document.getElementById("cancel").onclick = () => {
      while (gallery.children.length > 0) {
        gallery.lastChild.remove();
      }
      FILES = {};
      empty.classList.remove("hidden");
      gallery.append(empty);
    };
    
