/*///////////////////////////////////////////////////////////////
                            STORIES
//////////////////////////////////////////////////////////////*/

// convert story data to html
const story2Html = story => {
    return `
        <div>
            <img src="${ story.user.thumb_url }" class="pic" alt="profile pic for ${ story.user.username }" />
            <p>${ story.user.username }</p>
        </div>
    `;
};

// fetch data from stories endpoint and display as html
const displayStories = () => {
    fetch('/api/stories')
        .then(response => response.json())
        .then(stories => {
            const html = stories.map(story2Html).join('\n');
            document.querySelector('.stories').innerHTML = html;
        })
};

/*///////////////////////////////////////////////////////////////
                            POSTS
//////////////////////////////////////////////////////////////*/

// 1. Get the post data from the API endpoint (/api/posts?limit=10)
// 2. When that data arrives, we're going to build a bunch of HTML cards (i.e. big long string)
// 3. Update container and put html on the inside of it.
const likeUnlike = ev => {
    console.log('like button clicked')
};

const displayPosts = () => {
    fetch('/api/posts')
        .then(response => response.json())
        .then(posts => {
            const html = posts.map(post2Html).join('\n');
            document.querySelector('#posts').innerHTML = html;
        })
};

// convert story data to html
const post2Html = post => {
    return `
        <section class="card">
            <div class="header">
                <h3>${ post.user.username }</h3>
                <i class="fa fa-dots"></i>
            </div>
            <img src="${ post.image_url }" alt="Image posted by ${ post.user.username }" width="300" height="300">
            <div class="info">
                <div class="buttons">
                    <div>
                        <button onclick="likeUnlike(event)">
                            <i class="fa${ post.current_user_like_id ? 's' : 'r'} fa-heart"></i>
                        </button>
                        <i class="far fa-comment"></i>
                        <i class="far fa-paper-plane"></i>
                    </div>
                    <div>
                        <i class="fa${ post.current_user_bookmark_id ? 's' : 'r'} fa-bookmark"></i>
                    </div>
                </div>
                <p class="likes"><strong>${ post.likes.length } like${ post.likes.length != 1 ? 's' : '' }</strong></p>
                <div class="caption">
                    <p>
                        <strong>${ post.user.username }</strong> 
                        ${ post.caption }
                    </p>
                </div>
                <div class="comments">
                    ${ displayComments(post.comments, post.id) }
                </div>
            </div>
        </section>
    `;
};

// close modal after hitting button
const destroyModal = ev => {
    document.querySelector('#modal-container').innerHTML = "";
};

// display modal view of a post after clicking view comments
const showPostDetail = ev => {
    const postId = ev.currentTarget.dataset.postId;
    fetch(`/api/posts/${postId}`)
        .then(response => response.json())
        .then(post => {
            const html = `
                <div class="modal-bg">
                    <button onClick="destroyModal(event)">Close</button>
                    <div class="modal">
                        <img src="${post.image_url}">
                    </div>
                </div>`;
            document.querySelector('#modal-container').innerHTML = html;
            
        })
};
// display comments of a post
const displayComments = (comments, postId) => {
    // if more than one comment, show a button and the last comment below button
    // otherwise show a single comment if it exists
    // also possible to show 0 comments
    let html = '';
    if (comments.length > 1) {
        html += `
            <button class="link" data-post-id="${postId}" onclick="showPostDetail(event)">view all ${comments.length} comments</button>
            `;
    }
    if (comments && comments.length > 0) {
        const lastComment = comments[comments.length - 1]
        html += `
            <p>
                <strong>${ lastComment.user.username }</strong>
                ${lastComment.text}
            </p>
            <div class="timestamp">${lastComment.display_time}</div>
            `
    }
    html += `
        <div class="add-comment">
            <div class="input-holder">
                <input type="text" aria-label="Add a comment" placeholder="Add a comment...">
            </div>
            <button class="link">Post</button>
        </div>
    `
    return html
};

/*///////////////////////////////////////////////////////////////
                    SUGGESTIONS ASIDE
//////////////////////////////////////////////////////////////*/

// convert profile to html information
const profile2Html = user => {
    return `
        <img src="${ user.thumb_url }" class="pic" alt="profile pic for ${ user.username }" />
        <p><strong>${ user.username }</strong></p>
    `;
};

// display profile information
const displayProfile = () => {
    fetch('/api/profile')
        .then(response => response.json())
        .then(profile => {
            // console.log('profile is' + profile)
            // const html = profile.map(profile2Html).join('\n');
            const html = profile2Html(profile);
            document.querySelector('.pic').innerHTML = html;
    })
};

// converts suggestions to Html
const suggestions2Html = user => {
    return `
        <section>
            <img src="${ user.thumb_url }" class="pic" alt="profile pic for ${ user.username }" />
            <div>
                <p>${ user.username }</p>
                <p>suggested for you</p> 
            </div>
            <div>
                <button 
                    class="link following"
                    id = "follow-${user.id}"
                    data-username="${user.username}"
                    data-user-id="${user.id}"
                    aria-checked="false"
                    aria-label="Follow ${user.username}"
                    onclick="toggleFollow(event)">follow
                </button>
            </div>
        </section>
    `;
};

// displays suggestions
const displaySuggestions = () => {
    fetch('/api/suggestions')
        .then(response => response.json())
        .then(suggestedUsers => {
            const html = suggestedUsers.map(suggestions2Html).join('\n');
            document.querySelector('.suggestions').innerHTML = html;
        })
};
/*///////////////////////////////////////////////////////////////
                        Loading Page
//////////////////////////////////////////////////////////////*/
const initPage = () => {
    displayStories();
    displayPosts();
    displayProfile();
    displaySuggestions();
};

// invoke init page to display stories:
initPage();