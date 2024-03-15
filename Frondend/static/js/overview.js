document.addEventListener('DOMContentLoaded', function() {
    fetch('/user/')
    .then(response => response.text())
    .then(data => {
        document.getElementById('userName').innerText = data;
    });
});


function applyFilters() {
    var searchInput = document.getElementById("searchInput").value.toLowerCase();
    var eventContainers = document.querySelectorAll(".col-lg-3");

    eventContainers.forEach(function (container) {
        var title = container.querySelector("h2").textContent.toLowerCase();
        if (title.includes(searchInput)) {
            container.style.display = "block";
        } else {
            container.style.display = "none";
        }
    });
}


document.addEventListener("DOMContentLoaded", function () {
    const buttonIcons = document.querySelectorAll(".buttonIcon");
    buttonIcons.forEach(buttonIcon => {
        buttonIcon.addEventListener("click", function () {
            document.getElementById("overlay").style.display = "flex";
            document.getElementById("popup").style.display = "block";
        });
    });
});

function addNewComment() {
    if (document.getElementById("newComment")) {
        return; 
    }
    else{
        removeNewCommentButton();
        var popupComments = document.querySelector('.col-md-12.col-lg-10.col-xl-12'); 
        var newCommentDiv = document.createElement("div");
        newCommentDiv.classList.add("newComment");
        newCommentDiv.innerHTML = `
               <div class="card-footer py-3 border-0" style="background-color: #f8f9fa;" id="newComment">
            <div class="d-flex flex-start w-100">
              <img class="rounded-circle shadow-1-strong me-3"
                src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/img%20(19).webp" alt="avatar" width="40"
                height="40" />
              <div class="form-outline w-100">
                <textarea class="form-control" id="textAreaExample" rows="4"
                  style="background: #fff;"></textarea>
                <label class="form-label" for="textAreaExample">Nachricht</label>
              </div>
            </div>
            <div class="float-end mt-4 pt-1">
              <button type="button" class="btn btn-primary btn-sm" onclick="postComment()">Posten</button>
              <button type="button" class="btn btn-outline-primary btn-sm" onclick="cancelComment()">Abbrechen</button>
            </div>
          </div>`;
        popupComments.appendChild(newCommentDiv);     
    }
}

function postComment() {
    var textAreaValue = document.getElementById("textAreaExample").value.trim(); 
    if (textAreaValue === "") {
        alert("Bitte geben Sie einen Kommentar ein. Kommentar darf nicht leer sein!"); 
    }
    else{
    var textAreaValue = document.getElementById("textAreaExample").value;
    var popupComments = document.querySelector('.col-md-12.col-lg-10.col-xl-12');
    var newCommentDiv = document.createElement("div");
    newCommentDiv.classList.add("card");
    newCommentDiv.innerHTML = `
        <div class="col-md-12 col-lg-10 col-xl-12">
                                        <div class="card">
                                            <div class="card-body">
                                                <div class="d-flex flex-start align-items-center">
                                                    <img class="rounded-circle shadow-1-strong me-3"
                                                        src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/img%20(19).webp"
                                                        alt="avatar" width="60" height="60" />
                                                    <div>
                                                        <h6 class="fw-bold text-primary mb-1">Lily Coleman</h6>
                                                    </div>
                                                </div>
    
                                                <p class="mt-3 mb-4 pb-2">
                                                    ${textAreaValue}
                                                </p>
                                            </div>
                                        </div>`;
    popupComments.appendChild(newCommentDiv);
    cancelComment();
    addNewCommentButton();
    }

}

function removeNewCommentButton() {
    var newCommentButton = document.getElementById("newCommentButton");
    if (newCommentButton) {
        newCommentButton.parentNode.removeChild(newCommentButton);
    }
}

function addNewCommentButton() {
    if (!document.getElementById("newCommentButton")) {
        var popupComments = document.querySelector('.col-md-12.col-lg-10.col-xl-12');
        var newCommentButton = document.createElement("button");
        newCommentButton.classList.add("btn", "btn-primary", "mt-2", "float-end");
        newCommentButton.textContent = "neues Kommentar";
        newCommentButton.onclick = addNewComment;
        newCommentButton.id = "newCommentButton";
        popupComments.appendChild(newCommentButton);
    }
}

function cancelComment() {
    var newComment = document.getElementById("newComment");
    if (newComment) {
        newComment.parentNode.removeChild(newComment);
    }
    addNewCommentButton();
}


function closePopup() {
    document.getElementById("overlay").style.display = "none";
    document.getElementById("popup").style.display = "none";
}