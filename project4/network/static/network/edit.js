// document.addEventListener('DOMContentLoaded', function() {
//     document.querySelector('#edit-post').onclick = () => edit(this.value)
// });

function edit(id) {
    console.log(id);
    var composeText = document.querySelector(`#compose-view-${id}`);
    var composeSubmit = document.querySelector(`#compose-submit-${id}`);
    var existText = document.querySelector(`#post-text-${id}`);
    var editPostButton = document.querySelector(`#edit-post-${id}`);
    composeSubmit.style.display = 'block';
    composeText.style.display = 'block';
    existText.style.display = 'none';
    editPostButton.style.display = 'none';

    composeText.value = existText.innerHTML;


    composeSubmit.onclick = () => {
        fetch(`/edit/${id}`, {
            method: 'PUT',
            body: JSON.stringify({
                post_text: composeText.value
            })
        });

        composeSubmit.style.display = 'none';
        composeText.style.display = 'none';
        existText.style.display = 'block';
        editPostButton.style.display = 'block';

        document.querySelector(`#post-text-${id}`).innerHTML = composeText.value; 
    }

};