<div id="follow-button" style="float:right">
    {% if not profile and not is_following %}
        <button id="follow" type="button" class="btn btn-outline-primary">{% if not is_following %}Follow{% else %}Unfollow{% endif %}</button>
    {% elif not profile and is_following %}
        <button id="unfollow" type="button" class="btn btn-primary">Unfollow</button>
    {% endif %}
    </div>


    function follow() {
    var user_id = location.pathname.slice(6,); // To get the visited user id
    console.log(user_id)
    fetch('/follow/' + user_id, {
        method: 'PUT',
        body: JSON.stringify({
            user_id: user_id,
            is_following: false,
        })
    })
    .then(response => response.json())
    .then(result => {
        document.querySelector('#success').style.display = 'block'; // Display message
        document.querySelector('#success').innerHTML = result["message"];
        setTimeout(function() {
            document.querySelector('#success').style.display = 'none'
        }, 4000);
        document.querySelector('#followers').innerHTML = `You have ${result["followers"]} followers.`; // Add one follower to the count of the current user visited and followed
        let follow_button = document.querySelector('#follow-button');
        follow_button.innerHTML = `
        <button id="follow" type="button" class="btn btn-primary">Unfollow</button>
        `;
        follow_button.addEventListener('click', unfollow)
    })
}

@csrf_exempt
def follow(request, id):
    current_user = User.objects.get(pk=request.user.id)
    data = json.loads(request.body)
    print(data['user_id'])
    user_tofollow = User.objects.get(pk=data['user_id'])
    if not data['is_following']:
        new_follow = Follow(follow_user=current_user, follow_following=user_tofollow)
        new_follow.save()
        follow_counter = Follow.objects.filter(follow_following=user_tofollow).count()
        return JsonResponse({
            'message': 'User followed succesfully.',
            'followers': follow_counter,
        }, status=200)

    else: # Unfollow
        unfollow = Follow.objects.filter(follow_user=current_user, follow_following=user_tofollow).delete()
        follow_counter = Follow.objects.filter(follow_following=user_tofollow).count()
        return JsonResponse({
            'message': 'User unfollowed.',
            'followers': follow_counter,
        }, status=200)


        post_div.innerHTML = `
                            <div><a href="/profile"><b>${result.user}</b></a></div>
                            <div class="post-content">${edit_content}</div>
                            <div>${result.timestamp}</div>
                            <div id="post-likes">${result.likes}</div>
                            <button data-id="${result.post_id}" id="like-btn" class="btn">${result.liked_by_user? 'Liked': 'Like'}</button>
                            <button data-id="${result.post_id}" id="edit-btn" class="btn">Edit</button>
                        `;


<div id="posts-view">
        {% for post in posts %}
        <div class="post-container" id="post_{{ post.id }}">
            <div><b>{{ post.post_user }}</b></div>
            <div class="post-content">{{ post.post_content }}</div>
            <div>{{ post.post_timestamp }}</div>
            <div id="post-likes">{{ post.post_likes }}</div>
            <button data-id="{{ post.id }}" id="like-btn" class="btn btn-primary">{% if post.liked_by_user %}Liked{% else %}Like{% endif %}</button>
            {% if editable %}
            <button data-id="{{ post.id }}" id="edit-btn" class="btn btn-primary">Edit</button>
            {% endif %}
        </div>
        {% empty %}
            <div><b>You have made no posts yet.</b></div>
        {% endfor %}
    </div>