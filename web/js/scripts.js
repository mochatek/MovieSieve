let movie_cache = {};

eel.expose(update_progress);
function update_progress(completion_percentage) {
  $("#completion")
    .css("width", `${completion_percentage}%`)
    .attr("aria-valuenow", completion_percentage);
}

function refresh(success) {
  if (success) {
    window.location.reload();
  }
}

function choose_movie(movie) {
  $("#movie_form")[0].reset();
  $("input[name=movie]").val(movie);
  $("#movie_form")[0].style.display = "";
}

function add_movie(form, event) {
  event.preventDefault();
  const values = [
    form.movie.value,
    form.certificate.value,
    form.release.value,
    form.runtime.value,
    form.director.value,
    form.writer.value,
    form.actors.value,
    form.plot.value,
    form.language.value,
    form.country.value,
    form.awards.value,
    form.imdb.value,
    form.genre.value,
    form.poster.value,
  ].map((val) => val.trim());

  // If all values are given
  if (!values.includes("")) {
    const [
      movie,
      Rated,
      Released,
      Runtime,
      Director,
      Writer,
      Actors,
      Plot,
      Language,
      Country,
      Awards,
      imdbRating,
      Genre,
      poster,
    ] = values;

    const data = {
      Rated,
      Released,
      Runtime,
      Director,
      Writer,
      Actors,
      Plot,
      Language,
      Country,
      Awards,
      imdbRating,
      Genre,
    };
    eel.add_movie(movie, data, poster)(refresh);
  }
}

function setup_filter(genres) {
  let genre_list = "";

  Array.from(genres)
    .sort()
    .forEach((genre) => {
      genre_list += `<option value="${genre}">${genre}</option>`;
    });

  $("#genre_filter").append(genre_list);

  $("#genre_filter").prop("disabled", false);

  // Add listener to genre for filtering movies
  $("#genre_filter").on("change", function () {
    const selected_genre = this.value;
    let movies_count = 0;

    // If all genres are chosen, display all movies
    if (selected_genre == "all") {
      for (movie of $("#movies").children()) {
        movie.style.display = "";
        movies_count += 1;
      }

      // ELse filter movies based on selected genre
    } else {
      for (movie of $("#movies").children()) {
        if (movie.getAttribute("data-genre").includes(selected_genre)) {
          movie.style.display = "";
          movies_count += 1;
        } else {
          movie.style.display = "none";
        }
      }
    }

    // Update movies count in status
    $("#status").text(`Movies Count: ${movies_count}`);
  });
}

function setup_logs(errors) {
  if (errors.length) {
    $("#logs_info")
      .html(`Sorry, Unable to gather details for the following movies:
      Please try again after verifying the movie name and confirming filename format to be <mark>Movie (Year)</mark>.
      If the issue persists, then add the movie manually by clicking <mark>Fix</mark>.`);

    let movies = "";
    errors.forEach((movie) => {
      movies += `<p class="alert alert-danger p-1 mt-1 mb-0">❌ ${movie} <span style="float:right" class="badge badge-sm badge-success" onclick="choose_movie('${movie}')">Fix</span></p>`;
    });

    $("#logs_list").html(movies);
  } else {
    $("#logs_info").html(`Voila! Gathered details for all the movies.`);
    $("#logs_list").html(
      `<p class="alert alert-success p-1 mt-1 mb-0">✔️ No errors.</p>`
    );
  }

  $("#logs_btn").prop("disabled", false);
  $("#logs_modal").modal("show");
}

function list_movies({ movies, errors }) {
  let movie_list = "";
  const genre_list = new Set();

  movies.forEach((movie) => {
    const [name, genre] = movie;

    // Add movie to the list of movies
    movie_list += `<button type="button" data-genre="${genre}" class="list-group-item list-group-item-action" onclick="get_movie_data('${name}')">
        <div class="row">
            <div class="col-sm-1 folder"><i class="fa fa-lg fa-folder"></i></div>
            <div class="col-sm-10">${name}</div>
        </div>
    </button>`;

    // Add to cache
    movie_cache[name] = { genre, data: null };

    // Add genres to Genre list
    genre
      .split(",")
      .map((g) => g.trim())
      .forEach((gen) => genre_list.add(gen));
  });

  // Add movies to the UI
  $("#movies").append(movie_list);

  // Setup the genre filter
  setup_filter(genre_list);

  // Manage logs based on error
  setup_logs(errors);

  //   Update statuses
  $("#status").toggleClass("alert-danger alert-success");
  $("#status").text(`Movies Count: ${movies.length}`);
  $("div#info").html(
    '<p class="alert alert-primary">Select Movie to Preview Details.</p>'
  );

  // Remove progress
  $("#progress").remove();
}

function show_movie_data([movie, data, cached]) {
  // If not cached, then update the cache
  if (!cached) {
    movie_cache[movie].data = JSON.stringify(data);
  }

  const {
    Rated,
    Released,
    Runtime,
    Director,
    Writer,
    Actors,
    Plot,
    Language,
    Country,
    Awards,
    imdbRating,
    Genre,
  } = data;

  let [Title, Year] = movie.split("(");
  Year = Year.replace(")", "");

  $("div#info").html(`
    <div class="heading bg-blue">
        <h3>${Title} &nbsp;
            <span id="year">( ${Year} )</span>
            <span id="imdb"><i class="fa fa-imdb"></i> ${imdbRating}</span>
        </h3>
        <ul class="list-group list-group-horizontal-sm" style="font-size:small">
            <li class="list-group-item">${Rated}</li>
            <li class="list-group-item">${Genre}</li>
            <li class="list-group-item">${Runtime}</li>
            <li class="list-group-item">${Released}</li>
            <li class="list-group-item">${Country}</li>
            <li class="list-group-item">${Language}</li>
        </ul>
    </div>
    <div class="content">
        <img src="posters/${movie}.jpg" alt="Poster">
        <div class="details">
            <div>
                <p>Director</p>
                <p>${Director}</p>
            </div>
            <div>
                <p>Writer</p>
                <p>${Writer}</p>
            </div>
            <div>
                <p>Actors</p>
                <p>${Actors}</p>
            </div>
            <div>
                <p>Awards</p>
                <p>${Awards}</p>
            </div>
        </div>
    </div>
    <div class="summary">
        <p>${Plot}</p>
    </div>`);
}

function get_movie_data(movie) {
  // Check in cache
  if (movie_cache[movie].data) {
    show_movie_data([movie, JSON.parse(movie_cache[movie].data), true]);

    // If not in cache, then get it from server
  } else {
    eel.get_movie_data(movie)(show_movie_data);
  }
}

async function browse_movie_folder(event) {
  event.preventDefault();

  const movie_path = await eel.browse_movie_folder()();

  // If any movie folder was selected
  if (movie_path) {
    $("#browse_btn").prop("disabled", true);
    $("#status").toggleClass("alert-success alert-danger");
    $("#status").html(
      '<span class="spinner-border mr-2" style="width:1rem; height: 1rem;" role="status"></span>Retrieving Movies. Please be Patient.'
    );
    $("#info").html(`<div class="progress">
      <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" style="width: 100%"></div>
    </div>`);

    eel.get_movies(movie_path)(list_movies);
  }
}

function show_user_manual(event) {
  event.preventDefault();
  $("#user_manual").modal("show");
}

// Show user manual on first access of the app
document.onload = (function () {
  if (!localStorage.getItem("mochasieve")) {
    localStorage.setItem("mochasieve", true);
    $("#user_manual").modal("show");
  }
})();
