const url = 'http://localhost:8001'

let containers = [];
let runButtons = [];
let addButtons = [];
let removeButtons = [];
let codeBlocks = [];
let outputBlock = document.querySelector('.output');
updateButtons();

function updateButtons() {
  containers = document.querySelectorAll('.container');
  runButtons = document.querySelectorAll('.run');
  addButtons = document.querySelectorAll('.add-cell');
  removeButtons = document.querySelectorAll('.remove-cell');
  codeBlocks = document.querySelectorAll('.cell');

  for (let i = 0; i < runButtons.length; i++) {
    runButtons[i].onclick = () => runButtonClick(i);
    addButtons[i].onclick = () => addButtonClick(i);
    removeButtons[i].onclick = () => removeButtonClick(i);
  }
}

function runButtonClick(i) {
  fetch(`${url}/run`, {
    method: 'POST', 
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ code: codeBlocks[i].value })
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    outputBlock.value = data.stdout;
  })
  .catch((error) => {
    console.error('error:', error);
  });
}

function addButtonClick(i) {
  let newElement = `
    <div class="container">
      <textarea class="cell" rows="5" cols="80"></textarea>
      <button class="run">run</button>
      <button class="add-cell">add cell</button>
      <button class="remove-cell">remove cell</button>
    </div>
  `;
  containers[i].insertAdjacentHTML('afterend', newElement);
  updateButtons();
}

function removeButtonClick(i) {
  containers[i].remove();
  updateButtons();
}

document.querySelector('.upload-file').addEventListener('submit', async (e) => {
  e.preventDefault();
  const formData = new FormData(e.target); 
  try {
    let response = await fetch(`${url}/upload`, {
      method: 'POST',
      body: formData
    });

    if (response.ok) {
      let result = await response.json();
      alert(result.filename);
    }
  } catch (error) {}
});



