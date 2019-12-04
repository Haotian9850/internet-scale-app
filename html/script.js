var cities = [
    {
        "city": "samoyed",
        "population": 123,
        "state": "VA"
    },
    {
        "city": "golden retriever",
        "population": 123
    },
    {
        "city": "dog",
        "population": 123
    }
];


function findMatch(keyword, history){
    return history.filter(entry => {
        if (entry.city.includes(keyword)){
            return keyword;
        }
    })
}


function displayMatches(){
    const matchedEntries = findMatch(this.value, cities);
    console.log("matchedEntries", matchedEntries);
    const html = matchedEntries.map(place => {
        //highlight matching search phrase
        const regex = new RegExp(this.value, 'gi');
        const cityName = place.city.replace(regex, `<span class="h1">${this.value}</span>`);
        return `
            <li>
                <a href="#">
                <span class="name">${cityName}</span>
                <span class="population">${place.population}</span>
                </a>
            </li>
        `;
    }).join(''); //make it return a big string instead of an multi-element array
    suggestions.innerHTML = html; //display suggestion list
}


const searchInput = document.querySelector('.searchBar');
const suggestions = document.querySelector('.suggestions');

searchInput.addEventListener('change', displayMatches);
//keyup: when user releases a key, basically gets every input character entered
searchInput.addEventListener('keyup', displayMatches);  







