function searchMovie(){

    let movie = document.getElementById("movie").value.trim();

    if(!movie){
        document.getElementById("result").innerHTML = "Please enter a movie name";
        return;
    }

    document.getElementById("result").innerHTML = "Loading...";

    fetch(`/search?movie=${movie}`)
    .then(res => res.json())
    .then(data => {

        if(data.error){
            document.getElementById("result").innerHTML = data.error;
        }
        else{
            document.getElementById("result").innerHTML = `
                <div class="movie">
                    <h2>${data.title}</h2>
                    <img src="${data.poster}">
                    <p>Year: ${data.year}</p>
                    <p>Rating: ⭐ ${data.rating}</p>
                </div>
            `;
        }

    })
    .catch(() => {
        document.getElementById("result").innerHTML = "Server error. Please try again.";
    });
}

/* Press Enter to Search */
document.getElementById("movie").addEventListener("keypress", function(e){
    if(e.key === "Enter"){
        searchMovie();
    }
});
