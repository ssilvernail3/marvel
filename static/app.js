async function searchName(character) {
  try {
    const resp = await axios.get(`/api/search`, {
      params: { name: character }
    });

    if (resp.data.data.results.length === 0) {
      return null;
    }

    const hero = resp.data.data.results[0];
    const securePath = hero.thumbnail.path.replace('http://', 'https://');
    console.log("Hero Image URL:", `${securePath}/portrait_uncanny.${hero.thumbnail.extension}`);

    return {
      id: hero.id,
      name: hero.name,
      description: hero.description || "No description available.",
      appearances: hero.comics.available,
      series: hero.series.available,
      image: `${securePath}/portrait_uncanny.${hero.thumbnail.extension}`
    };
  } catch (err) {
    console.error("API error:", err);
    return null;
  }
}


function addHero(hero) {
  const $infoList = $('#info');
  $infoList.empty();

  const $item = $(`
    <div class="card animate__animated animate__fadeInUp">
      <img class="card-img-top" src="${hero.image}" alt="${hero.name}">
      <div class="card-body">
        <h5 class="card-title">${hero.name}</h5>
        <p class="card-text">${hero.description}</p>
        <p class="card-text"><strong>Comic Appearances:</strong> ${hero.appearances}</p>
        <p class="card-text"><strong>Series Appearances:</strong> ${hero.series}</p>
      </div>
    </div>
  `);

  $infoList.append($item);
}


$("#search-form").on("submit", async function handleSearch(evt) {
  evt.preventDefault();

  const character = $("#search-query").val().trim();
  if (!character) {
    alert("Please enter a character name.");
    return;
  }

  // 👇 Show the spinner and clear previous results
  $("#loading").show();
  $("#info").empty();

  try {
    const hero = await searchName(character);
    if (!hero) {
      alert("Character not found. Please try another name.");
      $("#loading").hide(); // hide spinner if no hero found
      return;
    }

    addHero(hero);
  } catch (err) {
    console.error(err);
    alert("Something went wrong. Please try again.");
  } finally {
    $("#loading").hide(); // ✅ Always hide the spinner
    $("#search-query").val(""); // clear search bar
  }
});



