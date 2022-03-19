async function searchName(character) {
    const resp = await axios.get(`https://gateway.marvel.com/v1/public/characters?name=${character}&ts=1&apikey=9fc66a02b7eaad221022d19aee14503d&hash=14bc49d69eac6d1dd823e2e75394321a`)
    console.log(resp);


    let hero = resp.data.data.results[0]; 
    let name = hero.name;
    let description = hero.description
    let id = hero.id
    let appearances = hero.comics.available
    let series = hero.series.available
    let image = hero.thumbnail.path
  
    console.log(hero.thumbnail.path);

   
  
    let comics = hero.comics.items

   
    // for (let comic in comics) {
    //     console.log(comic.items)
    // };

    // comics.forEach(comic => {
    //     for (let name in comic) {
    //         // console.log(`${name}: ${comic[name]}`);
    //         // console.log(comic.name);
    //         console.log(comic.name);
    //         newLi = document.createElement('li');
    //         newText = document.createTextNode(comic.name);
    //         newLi.appendChild(newText);
    //         newLi.classList.add(`${hero.id}`)
    //         const $comicList = $('#comics');

            
    //        $comicList.append(newLi);
    //     };
        
    
        
    // });

    
    

    return {
        id: hero.id,
        name: hero.name,
        description: hero.description,
        appearances: hero.comics.available,
        image: hero.thumbnail.path,
        series: hero.series.available
        
        
        
    

    };

    return hero; 


};

// function addComics(comics) {
//     const $comicList = $('#comics');
//     $comicList.empty();

//     comics.forEach(comic => {
//         for (let name in comic) {
//             // console.log(`${name}: ${comic[name]}`);
//             // console.log(comic.name);
//             console.log(comic.name);
//             let $item = $(
//                 `<div id="comics">
//                     <ul>
//                         <li>${comic.name}</li>
//                     </ul>
//                 </div>`
//             );
//             // console.log(comic.name);
//             // newLi = document.createElement('li');
//             // newText = document.createTextNode(comic.name);
//             // newLi.appendChild(newText);
//             // const $comicList = $('#comics');

            
            
//         };
//     $comicList.append($item);
    

//     });
// };


function addHero(hero) {

    const $infoList = $('#info');
    $infoList.empty();

    let $item = $(
        `<div class="card text-center border-dark hero" style="width: 25rem;" id="result">
            <form action="/favorite" class="hero-form">
                <img class="card-img-top" src="${hero.image}/landscape_large.jpg"></img>
                <input type="hidden" name="image" value="${hero.image}"/>
                <div class="card-body">
                    <h5 class="card-title">${hero.name}</h5>
                    <input type="hidden" name="name" value="${hero.name}"/>
                    <p class="card-text">${hero.description}</p>
                    <input type="hidden" name="description" value="${hero.description}"/>
                    <p class="card-text">Number of Comic Book Appearances: ${hero.appearances}</p>
                    <input type="hidden" name="appearances" value="${hero.appearances}"/>
                    <p class="card-text">Number of Comic Series Appearances: ${hero.series}</p>
                    <input type="hidden" name="series" value="${hero.series}"/>
                </div>
            </form>
        </div>`
    );

  
    $infoList.append($item); 
};


$("#search-form").on("submit", async function handleSearch(evt) {
    evt.preventDefault();

    let character = $("#search-query").val();
    if (!character) return;

    let hero = await searchName(character);

    const $comicList = $('#comics');

    addHero(hero);

    const searchBar = document.getElementById('search-query')

    searchBar.value = '';

    // const comicLis = document.querySelectorAll("div.comics > li");
    // console.log(comicLis);
    
    
    // console.log(comics);
    // if (li.className != hero.id) {
    //     li.remove(); 
    // };
    
});


// const $comicList = $('#comics');
// $comicList.empty();