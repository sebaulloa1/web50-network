document.addEventListener('DOMContentLoaded', function() {
    // By default
    document.querySelectorAll('#like-btn').forEach(function(div) {div.addEventListener('click', like)})
    document.querySelectorAll('#edit-btn').forEach(function(div) {div.addEventListener('click', edit)})

    if (window.location.pathname === '/') {
        document.querySelector('#new-post-form').onsubmit = new_post;
    } else if (window.location.pathname.indexOf('/user/') != -1) {
        document.querySelector('#follow').addEventListener('click', follow)
    }
});

function new_post() {
    let post_content = document.querySelector('#new-post-content').value;

    // Check for empty post
    if (!post_content) {
        fetch('/new_post', {
            method: 'POST',
        })
        .then(response => {
            if (response.redirected) {
                window.location = '/login'
            } else {
                document.querySelector('.alert-danger').style.display = 'block';
                document.querySelector('.alert-danger').innerHTML = 'You must write something before posting';
                setTimeout(function() {
                document.querySelector('.alert-danger').style.display = 'none';
                }, 4000);
            }
        })
    } else {
        fetch('/new_post', {
            method: 'POST',
            body: JSON.stringify({
                post_content: post_content,
            })
        })
        .then(response => {
            if (response.redirected) {
                window.location = '/login';
            } else {
                response.json()
                .then(result => {
                // Create a whitespace that grows-y
                let white_space = document.createElement('div');
                document.querySelector('#posts-view').prepend(white_space);
                white_space.className = 'white-space';
                white_space.style.cssText = 'display:block; animation-play-state:running';
                // Create a new div for the new post
                let new_div = document.createElement('div');
                setTimeout(function() {
                    white_space.remove(); // Delete the white space
                    document.querySelector('#posts-view').prepend(new_div);
                    new_div.classList.add( 'new-post-container', 'animate__animated', 'animate__bounceInLeft')
                    new_div.innerHTML = `
                    <div class="post-container-username">
                        <a href="/profile"><b>${result.post_user}</b></a>
                        <div class="post-timestamp">${result.post_timestamp}</div>
                    </div>
                    <div class="post-content">${result.post_content}</div>
                    <div id="like-btn" class="likes-container" data-id="${result.post_id}">
                        <span class="like-btn" aria-label="Like this post." data-id="${result.post_id}}">
                            <svg data-id="${result.post_id}" class="heart" viewBox="0 0 32 29.6">
                                <path data-id="${result.post_id}" d="M23.6,0c-3.4,0-6.3,2.7-7.6,5.6C14.7,2.7,11.8,0,8.4,0C3.8,0,0,3.8,0,8.4c0,9.4,9.5,11.9,16,21.2
                                c6.1-9.3,16-12.1,16-21.2C32,3.8,28.2,0,23.6,0z"/>
                            </svg>
                        </span>
                        <label data-id="${result.post_id}" for="likes-container" id="post-likes">0</label>
                    </div>
                    `;
                }, 1000);
                document.querySelector('#new-post-content').value = '';
                // Redirect to page 1
                document.addEventListener('animationend', function() {
                    if (document.querySelector('.active').innerText.indexOf('1') === -1) {
                    document.querySelector('.page-number').click();
                    } else {location.reload()}
                });
                })
            }
        })
        
    }
    return false;
}

function follow() {
    var user_id = document.querySelector('#follow').dataset.id; // To get the visited user id
    fetch(`/follow/${user_id}`)
    .then(response => response.json())
    .then(result => {
        document.querySelector('#success').style.display = 'block'; // Display message
        document.querySelector('#success').innerHTML = result["message"];
        setTimeout(function() {
            document.querySelector('#success').style.display = 'none'
        }, 4000);
        document.querySelector('#followers').innerHTML = `${result["followers"]} Followers.`; // Add one follower to the count of the current user visited and followed
        let follow_button = document.querySelector('#follow');
        if (follow_button.innerText === 'Follow') {
            follow_button.innerText = 'Unfollow'
        } else {
            follow_button.innerText = 'Follow'
        }
    })
}

function edit(event) {
    post_div = event.target.parentNode;
    if_cancel = post_div.innerHTML;
    post_content = post_div.querySelector('.post-content').innerHTML;
    post_user = post_div.querySelector('b').innerText;
    post_timestamp = post_div.querySelector('.post-timestamp').innerText;
    post_id = event.target.dataset.id;
    post_div.innerHTML = `
        <form id="edit-form">
            <div class="post-container-username">
                <b>${post_user}</b>
                <div class="post-timestamp">${post_timestamp}</div>
            </div>
            <textarea id="edit-content">${post_content}</textarea>
            <input type="submit" class="btn" value="Edit">
            <button class="btn" id="cancel">Cancel</button>
        </form>
    `;
    document.querySelector('#cancel').addEventListener('click', function() {
        post_div.innerHTML = if_cancel;
        document.querySelector('#edit-btn').addEventListener('click', edit);
    })
    document.querySelector('#edit-form').onsubmit = function() {
        edit_content = document.querySelector('#edit-content').value
        if (!edit_content) {
            document.querySelector('.alert-danger').style.display = 'block';
            document.querySelector('.alert-danger').innerHTML = 'You must write something before posting';
            setTimeout(function() {
                document.querySelector('.alert-danger').style.display = 'none';
            }, 4000);
        } else {
            fetch(`/edit/${post_id}`, {
                method: 'POST',
                body: JSON.stringify({
                    edit_content: edit_content
                })
            })
            .then(response => {
                if (response.status === 200) {
                    response.json()
                    .then(result => {
                        post_div.innerHTML = `
                            <div class="post-container-username">
                                <a href="/profile"><b>${result.user}</b></a>
                                <div class="post-timestamp">${result.timestamp}</div>
                            </div>
                            <div class="post-content">${edit_content}</div>
                            <div id="like-btn" class="likes-container">
                                <span class="like-btn" aria-label="Like this post." data-id="${result.post_id}">
                                    <svg data-id="${result.post_id}" ${result.liked_by_user? `class="heart liked"`: `class="heart"`} viewBox="0 0 32 29.6">
                                        <path data-id="${result.post_id}" d="M23.6,0c-3.4,0-6.3,2.7-7.6,5.6C14.7,2.7,11.8,0,8.4,0C3.8,0,0,3.8,0,8.4c0,9.4,9.5,11.9,16,21.2
                                        c6.1-9.3,16-12.1,16-21.2C32,3.8,28.2,0,23.6,0z"/>
                                    </svg>
                                </span>
                                <label data-id="${result.post_id}" for="likes-container" id="post-likes">${result.likes}</label>
                                
                            </div>
                            <button data-id="${result.post_id}" id="edit-btn" class="btn">Edit</button>
                        `;
                        document.querySelector('#success').style.display = 'block'; // Display message
                        document.querySelector('#success').innerHTML = result["message"];
                        setTimeout(function() {
                            document.querySelector('#success').style.display = 'none'
                        }, 4000);
                        document.querySelectorAll('#like-btn').forEach(function(div) {div.addEventListener('click', like)});
                        document.querySelectorAll('#edit-btn').forEach(function(div) {div.addEventListener('click', edit)});
                    })
                }
            })
            
        }
        return false;
    }

} 

function like(event) {
    let post_id = event.target.dataset.id;
    fetch(`/like/${post_id}`)
    .then(response => {
        if (response.redirected) {
            window.location = '/login';
        } else {
            response.json()
            .then(result => {
                // Update like buttons inner text
                post_div = document.querySelector(`#post_${post_id}`)
                if (post_div.querySelector('.heart').classList.contains('liked')) {
                    post_div.querySelector('.heart').classList = 'heart'
                } else {
                    post_div.querySelector('.heart').classList = 'heart liked';
                    document.querySelector('#success').style.display = 'block'; // Display message
                    document.querySelector('#success').innerHTML = result["message"] 
                    setTimeout(function() {
                        document.querySelector('#success').style.display = 'none'
                    }, 4000);
                }
                // Update total likes
                post_div.querySelector('#post-likes').innerText = result["total_likes"]
            })        
        }
    })
}
    

