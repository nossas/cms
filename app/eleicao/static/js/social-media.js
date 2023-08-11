// static/js/add_social_media.js

document.addEventListener('DOMContentLoaded', function() {
  const addButton = document.getElementById('add-social-media');
  const formContainer = document.querySelector('.social_media_fields');

  let socialMediaCounter = 2;

  addButton.addEventListener('click', function() {
    const newSocialMediaField = `
      <div class="flex gap-4 items-center">
        <div>
          <div class="max-w-xs">
          <label>Rede social</label>
           <select>
           ${fieldLabelTag('Rede Social')}
           <option value="" disabled selected>Selecione</option>
            <option>Twitter</option>
            <option>Instagram</option>
            <option>Facebook</option>
            <option>Outro</option>
           </select>
          </div>
        </div>
        <div class="gap-1 font-bold max-w-sm">
          <label>URL da Rede Social</label>
          ${fieldInputTag('social_media_link', socialMediaCounter)}
        </div>
      </div>
    `;

    const newFieldContainer = document.createElement('div');
    newFieldContainer.innerHTML = newSocialMediaField;
    if(formContainer.children.length <= 3){
      formContainer.appendChild(newFieldContainer);
    }
    socialMediaCounter++;
  });
});

function fieldLabelTag(fieldName, counter) {
  return `<label for="${fieldName}_${counter}">Social Media ${counter}</label>`;
}

function fieldInputTag(fieldName, counter) {
  return `<input type="text" name="${fieldName}_${counter}" id="${fieldName}_${counter}">`;
}
