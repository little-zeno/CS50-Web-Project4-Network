function edit(id) {
    console.log(id);
    const composeText = document.querySelector(`#compose-view-${id}`);
    const composeSubmit = document.querySelector(`#compose-submit-${id}`);
    const existText = document.querySelector(`#post-text-${id}`);
    const editPostButton = document.querySelector(`#edit-post-${id}`);
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

        existText.innerHTML = composeText.value; 
    }

};



function like(id) {
    console.log(id);
    const likeButton = document.querySelector(`#like-button-${id}`);
    const likeSvg = document.querySelector(`#like-svg-${id}`);
    const likeCount = document.querySelector(`#like-count-${id}`);

    console.log(likeButton.value);
    


    fetch(`/like/${id}`, {
        method : 'POST',
        body: JSON.stringify({
            likes: likeButton.value
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result.count);
        likeCount.innerHTML = `${result.count}Like(s)`;
    });

    if (likeSvg.style.fill == 'red') {
        likeSvg.style.fill = "black";
    } else {
        likeSvg.style.fill = "red";
    }
};

