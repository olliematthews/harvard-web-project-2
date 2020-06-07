console.log('executing');


// If hide button is clicked, delete the post.
document.addEventListener('click', event => {
    const element = event.target;
    if (element.classList.contains('remove')) {
            console.log(element.parentElement.dataset.user);
            update_users(element.parentElement.dataset.user);
        };
});

// When page is loaded, automatically add yourself to channel.
document.addEventListener('DOMContentLoaded', event => {
            update_users('No User');
});


// If add button is clicked, add the member
document.addEventListener('click', event => {
    const element = event.target;
    if (element.classList.contains('add_user')) {
            console.log(element.dataset.user);
            update_users(element.dataset.user);
        };
    });

function update_users(user) {
  const request = new XMLHttpRequest();
  request.open('POST', '/get_users');
  request.onload = () => {
      const data = JSON.parse(request.responseText);
      console.log(data);
      const dname = data['dname'];
      const users = data['users'];
      console.log(dname);
      users.forEach(add_post, dname);
  };

  // Add start and end points to request data.
  const data = new FormData();
  data.append('user', user);

  // Send request.
  request.send(data);
}

// function remove(element) {
//   const user = element.dataset.user;
//   update_users(user);
// };

// Add a new post with given contents to DOM.
const post_template = Handlebars.compile(document.querySelector('#post').innerHTML);

function add_post(contents) {
    console.log(this);
    console.log(new String(contents));
    console.log(new String(contents) === this);
    if (!(new String(contents) === this)){
      console.log('yes');
      // Create new post.
      const post = post_template({'contents': contents});

      // Add post to DOM.
      document.querySelector('#participants').innerHTML += post;
    };
};
