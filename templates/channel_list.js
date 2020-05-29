
// // If hide button is clicked, delete the post.
// document.addEventListener('click', event => {
//     const element = event.target;
//     if (element.className === 'hide') {
//         element.parentElement.style.animationPlayState = 'running';
//         element.parentElement.addEventListener('animationend', () =>  {
//             element.parentElement.remove();
//         });
//     }
// });

// If add button is clicked, add the member
document.addEventListener('click', event => {
    const element = event.target;
    if (element.className === 'add_user') {
            send(element.dataset.user);
        });
    }
});

function send(user) {
  const request = new XMLHttpRequest();
  request.open('POST', '/get_users');
  request.onload = () => {
      const data = JSON.parse(request.responseText);
      data.forEach(add_post);
  };

  // Add start and end points to request data.
  const data = new FormData();
  data.append('user', user);

  // Send request.
  request.send(data);
}


// Add a new post with given contents to DOM.
const post_template = Handlebars.compile(document.querySelector('#post').innerHTML);

function add_post(contents) {

    // Create new post.
    const post = post_template({'contents': contents});

    // Add post to DOM.
    document.querySelector('#posts').innerHTML += post;
}
